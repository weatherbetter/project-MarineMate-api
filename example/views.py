# from .serializers import AccidentSerializer,AccidentMonthSerializer

from django.db.models import Count, F
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
    response = {"message": "Hi world it is updated!?"}
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
                jellyfish_score = JellyfishScore.objects.get(location=location)
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
            rainfall_score = RainfallScore.objects.get(beach_id=beach_id)
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

        try:
            wind_speed = WindSpeed.objects.get(beach_id=beach_id)
            wind_speed_serializer = WindSpeedSerializer(wind_speed)
            response_data["wind_speed"] = wind_speed_serializer.data
        except WindSpeed.DoesNotExist:
            response_data["wind_speed"] = {}

        try:
            max_temperature = MaxTemperature.objects.get(beach_id=beach_id)
            max_temp_serializer = MaxTemperatureSerializer(max_temperature)
            response_data["max_temperature"] = max_temp_serializer.data
        except MaxTemperature.DoesNotExist:
            response_data["max_temperature"] = {}

        try:
            wave_height = WaveHeight.objects.get(beach_id=beach_id)
            wave_height_serializer = WaveHeightSerializer(wave_height)
            response_data["wave_height"] = wave_height_serializer.data
        except WaveHeight.DoesNotExist:
            response_data["wave_height"] = {}

        try:
            wind_direction = WindDirection.objects.get(beach_id=beach_id)
            wind_direction_serializer = WindDirectionSerializer(wind_direction)
            response_data["wind_direction"] = wind_direction_serializer.data
        except WindDirection.DoesNotExist:
            response_data["wind_direction"] = {}

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET"])
def safetyApi(request: Request):
    if "location" not in request.GET:
        return Response({"error": "The 'location' parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    # 소방서 수
    fs_cnt = SafetyInfra.objects.filter(location=request.GET["location"]).values("fs_cnt")
    # 안전센터 수
    sc_cnt = SafetyInfra.objects.filter(location=request.GET["location"]).values("sc_cnt")
    # 펌뷸런스 수
    fb_cnt = SafetyInfra.objects.filter(location=request.GET["location"]).values("fb_cnt")

    # 오류 확인
    if not fs_cnt or not sc_cnt or not fb_cnt:
        return Response(
            {"error": "No safety infrastructure data found for the given location."}, status=status.HTTP_404_NOT_FOUND
        )
