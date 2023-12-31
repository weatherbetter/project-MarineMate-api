# from .serializers import AccidentSerializer,AccidentMonthSerializer

from django.db.models import Count, F, Max
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

# drf
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Accident,
    Beach,
    BeachInfra,
    BeachScore,
    JellyfishScore,
    LifesavingEquipment,
    MaxTemperature,
    RainfallScore,
    SafetyInfra,
    WaveHeight,
    WindDirection,
    WindSpeed,
)
from .serializers import (
    BeachInfraSerializer,
    BeachScoreSerializer,
    EquipmentSerializer,
    JellyfishScoreSerializer,
    MaxTemperatureSerializer,
    RainfallScoreSerializer,
    WaveHeightSerializer,
    WindDirectionSerializer,
    WindSpeedSerializer,
)


def index(request: HttpRequest):
    response = {"message": "Hi world it is updated!"}
    return JsonResponse(response)


@api_view(http_method_names=["GET"])
def accidentApi(request: Request):
    if "location" in request.GET:
        # 원인별 수난사고
        queryset = (
            Accident.objects.filter(place="바다", location=request.GET["location"])
            .values("cause")
            .annotate(cause_count=Count("cause"))
            .order_by("-cause_count")
            .values("cause", "cause_count")
        )
        causes = [item["cause"] for item in queryset]
        cause_counts = [item["cause_count"] for item in queryset]

        # 월별 수난사고 빈도
        queryset = (
            Accident.objects.filter(place="바다", location=request.GET["location"])
            .values("month")
            .annotate(month_count=Count("month"))
            .values("month", "month_count")
        )
        month = [item["month"] for item in queryset]
        month_counts = [item["month_count"] for item in queryset]

        # 시군구별 수난사고 빈도 - 상위 10개
        queryset = (
            Accident.objects.filter(place="바다", location=request.GET["location"])
            .values("sigungu")
            .annotate(sigungu_count=Count("sigungu"))
            .order_by("-sigungu_count")
            .values("sigungu", "sigungu_count")[:10]
        )
        sigungu = [item["sigungu"] for item in queryset]
        sigungu_counts = [item["sigungu_count"] for item in queryset]

        # 장소별 수난사고 빈도 - 상위 5개
        queryset = (
            Accident.objects.filter(location=request.GET["location"])
            .values("place")
            .annotate(place_count=Count("place"))
            .order_by("-place_count")
            .values("place", "place_count")[:5]
        )
        place = [item["place"] for item in queryset]
        place_counts = [item["place_count"] for item in queryset]

        response = {
            "causes": causes,
            "cause_counts": cause_counts,
            "month": month,
            "month_counts": month_counts,
            "sigungu": sigungu,
            "sigungu_counts": sigungu_counts,
            "place": place,
            "place_counts": place_counts,
        }
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "need location parameter"},
            status=status.HTTP_404_NOT_FOUND,
        )


# -----인명구조장비함 api-----#
@api_view(["GET"])
def equipmentApi(request):
    totalequipment = LifesavingEquipment.objects.all()  # 모델로 만들어진 객체를 모두 가져오기
    serializer = EquipmentSerializer(totalequipment, many=True)  # 다양한 내용들에 대해 내부적으로도 직렬화
    return Response(serializer.data)


# -----인프라 api-----#


class BeachInfraAPIView(APIView):
    def get(self, request, beach_id):
        try:
            beach_infra = BeachInfra.objects.get(beach_id=beach_id)

            beach_infra_serializer = BeachInfraSerializer(beach_infra)

            return Response(
                {
                    "beach_infra": beach_infra_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except BeachInfra.DoesNotExist:
            return Response(
                {"error": "BeachInfra data not found for the given beach_id."},
                status=status.HTTP_404_NOT_FOUND,
            )


# -----추천점수 api-----#


@api_view(http_method_names=["GET"])
def beach_scores_api(request, beach_id):
    try:
        # 해수욕장 점수 정보 가져오기
        beach_score = BeachScore.objects.get(beach_id=beach_id)
        beach_score_serializer = BeachScoreSerializer(beach_score)

        response = {
            "beach_score": beach_score_serializer.data,
        }

        try:
            # 해당 해수욕장의 위치(location) 가져오기
            beach = Beach.objects.get(id=beach_id)
            location = beach.location

            # 해당 위치(location)의 해파리 점수 가져오기
            try:
                # 여러 개의 해파리 점수 데이터가 있는 경우, 가장 최근 데이터를 가져옵니다.
                jellyfish_score = JellyfishScore.objects.filter(location=location).latest("date")
                jellyfish_score_serializer = JellyfishScoreSerializer(jellyfish_score)
                response["jellyfish_score"] = jellyfish_score_serializer.data
            except JellyfishScore.DoesNotExist:
                # 해당 위치(location)에 대한 해파리 점수 데이터가 없을 경우 빈 딕셔너리 반환
                response["jellyfish_score"] = {}

        except Beach.DoesNotExist:
            # 주어진 beach_id에 해당하는 해수욕장 데이터가 없을 경우 에러 반환
            return Response(
                {"error": "해당 beach_id에 대한 해수욕장 데이터를 찾을 수 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            # 강수 점수 정보 가져오기
            # 여러 개의 강수 점수 데이터가 있는 경우, 가장 최근 데이터를 가져옵니다.
            rainfall_score = RainfallScore.objects.filter(beach_id=beach_id).latest("date")
            rainfall_score_serializer = RainfallScoreSerializer(rainfall_score)
            response["rainfall_score"] = rainfall_score_serializer.data
        except RainfallScore.DoesNotExist:
            # 강수 점수 정보가 없을 경우 빈 딕셔너리 반환
            response["rainfall_score"] = {}

        return Response(response, status=status.HTTP_200_OK)
    except BeachScore.DoesNotExist:
        # 주어진 beach_id에 해당하는 해수욕장 점수 데이터가 없을 경우 에러 반환
        return Response(
            {"error": "해당 beach_id에 대한 해수욕장 점수 데이터를 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND,
        )


# -----예보 api-----#


class BeachWeatherAPIView(APIView):
    def get(self, request, beach_id):
        response_data = {}

        wind_speeds = WindSpeed.objects.filter(beach_id=beach_id)
        if wind_speeds.exists():
            wind_speed_serializer = WindSpeedSerializer(wind_speeds, many=True)
            response_data["wind_speed"] = wind_speed_serializer.data
        else:
            response_data["wind_speed"] = []

        max_temperatures = MaxTemperature.objects.filter(beach_id=beach_id)
        if max_temperatures.exists():
            max_temp_serializer = MaxTemperatureSerializer(max_temperatures, many=True)
            response_data["max_temperature"] = max_temp_serializer.data
        else:
            response_data["max_temperature"] = []

        wave_heights = WaveHeight.objects.filter(beach_id=beach_id)
        if wave_heights.exists():
            wave_height_serializer = WaveHeightSerializer(wave_heights, many=True)
            response_data["wave_height"] = wave_height_serializer.data
        else:
            response_data["wave_height"] = []

        wind_directions = WindDirection.objects.filter(beach_id=beach_id)
        if wind_directions.exists():
            wind_direction_serializer = WindDirectionSerializer(wind_directions, many=True)
            response_data["wind_direction"] = wind_direction_serializer.data
        else:
            response_data["wind_direction"] = []

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def safetyApi(request: Request):
    if "location" in request.GET:
        # 소방서 수
        fs_cnt = SafetyInfra.objects.filter(location=request.GET["location"]).values("fs_cnt")
        # 안전센터 수
        sc_cnt = SafetyInfra.objects.filter(location=request.GET["location"]).values("sc_cnt")
        # 펌뷸런스 수
        fb_cnt = SafetyInfra.objects.filter(location=request.GET["location"]).values("fb_cnt")

        response = {
            "Fire Station": fs_cnt[0]["fs_cnt"],
            "Safety Center": sc_cnt[0]["sc_cnt"],
            "Pumbulance": fb_cnt[0]["fb_cnt"],
        }
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "need location parameter"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(http_method_names=["GET"])
def beachRecommendApi(request: Request):
    if "location" in request.GET:
        region = request.GET["location"]
        all_locations = BeachScore.objects.values_list("location", flat=True).distinct()

        # BeachScore 테이블에서 선택한 지역의 beach_id 목록을 가져옵니다.
        beach_ids = BeachScore.objects.filter(location=region).values_list("beach_id", flat=True)

        # 각 테이블에서 가장 최신 데이터를 가져오고 점수를 계산합니다.
        rainfall = (
            RainfallScore.objects.filter(beach_id__in=beach_ids)
            .annotate(score=F("rain_score"))
            .values("beach_id", "score")
        )

        jellyfish = (
            JellyfishScore.objects.filter(location=region)
            .annotate(score=4 - F("jellyfish_score"))
            .values("location", "score")
        )

        beach_score = (
            BeachScore.objects.filter(location=region)
            .annotate(score=F("water_score") + F("soil_score") + F("facility_score"))
            .values("beach_id", "score", "beach_name")
        )

        # 각 테이블의 점수를 합산합니다.
        scores = {}
        beach_scores = {}
        rainfall_scores = {}
        jellyfish_scores = {}
        beach_names = {}
        for table in [
            (rainfall, "beach_id", rainfall_scores),
            (jellyfish, "location", jellyfish_scores),
            (beach_score, "beach_id", beach_scores),
        ]:
            for row in table[0]:
                if table[1] in row:
                    if row[table[1]] not in scores:
                        scores[row[table[1]]] = row["score"]
                    else:
                        scores[row[table[1]]] += row["score"]

                    table[2][row[table[1]]] = row["score"]
                    if table[0] == beach_score:
                        beach_names[row[table[1]]] = row["beach_name"]

        # 점수가 가장 높은 해수욕장 순으로 정렬합니다.
        sorted_beaches = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # 최상위 3개의 해수욕장을 선택합니다.
        TOP_COUNT = 3
        if len(sorted_beaches) > TOP_COUNT:
            sorted_beaches = sorted_beaches[:TOP_COUNT]
        else:
            sorted_beaches = sorted_beaches[:-1]
            
        top_beaches = [
            {
                "beach_id": beach[0], 
                "beach_name": beach_names[beach[0]],
                "total_score": rainfall_scores.get(beach[0], 0)
                + jellyfish_scores.get(region, 0)
                + beach_scores.get(beach[0], 0),
                "rainfall_score": rainfall_scores.get(beach[0], 0),
                "jellyfish_score": jellyfish_scores.get(region, 0),
                "beach_score": beach_scores.get(beach[0], 0),
            }
            for beach in sorted_beaches[:3]
        ]

        return Response(data=top_beaches, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "need location parameter"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
def get_jellyfish_scores(request):
    # 지역별 최신 날짜
    recent_dates = JellyfishScore.objects.values("location").annotate(recent_date=Max("date"))

    # 점수 딕셔너리
    scores = {}

    # 지역별 점수
    for item in recent_dates:
        score = JellyfishScore.objects.filter(location=item["location"], date=item["recent_date"]).first()
        if score:
            scores[score.location] = score.jellyfish_score

    return Response(scores)
