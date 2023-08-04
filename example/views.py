from rest_framework.request import Request
from rest_framework.response import Response
from .models import Accident, LifesavingEquipment, SafetyInfra, RainfallScore, JellyfishScore, BeachScore
from .serializers import EquipmentSerializer
from django.db.models import Count, F
from django.http import HttpRequest, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView


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


@api_view(["GET"])
def equipmentApi(request):
    totalequipment = LifesavingEquipment.objects.all()  # 모델로 만들어진 객체를 모두 가져오기
    serializer = EquipmentSerializer(totalequipment, many=True)  # 다양한 내용들에 대해 내부적으로도 직렬화
    return Response(serializer.data)


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
            "Fire Station" : fs_cnt[0]['fs_cnt'],
            "Safety Center" : sc_cnt[0]['sc_cnt'],
            "Pumbulance" : fb_cnt[0]['fb_cnt'],
        }
        
    return Response(data=response, status=status.HTTP_200_OK)


class BeachRecommendationView(APIView):
    def get(self, request, format=None):
        # 사용자 입력 데이터
        region = request.GET.get('location')

        # BeachScore 테이블에서 선택한 지역의 beach_id 목록을 가져옵니다.
        beach_ids = BeachScore.objects.filter(location=region).values('beach_id')

        # 각 테이블에서 가장 최신 데이터를 가져오고 점수를 계산합니다.
        latest_rainfall_date = RainfallScore.objects.latest('date').date
        rainfall = RainfallScore.objects.filter(beach_id__in=beach_ids, date=latest_rainfall_date).annotate(score=F('rain_score')).values('beach_id', 'score')

        latest_jellyfish_date = JellyfishScore.objects.latest('date').date
        jellyfish = JellyfishScore.objects.filter(beach_id__in=beach_ids, date=latest_jellyfish_date).annotate(score=4 - F('jellyfish_score')).values('beach_id', 'score')

        beach_score = BeachScore.objects.filter(location=region).annotate(score=F('water_score') + F('soil_score') + F('facility_score')).values('beach_id', 'score', 'beach_name')

        # 각 테이블의 점수를 합산합니다.
        scores = {}
        beach_scores = {}
        rainfall_scores = {}
        jellyfish_scores = {}
        beach_names = {}
        for table in [rainfall, jellyfish, beach_score]:
            for row in table:
                if 'beach_id' in row:
                    if row['beach_id'] not in scores:
                        scores[row['beach_id']] = row['score']
                    else:
                        scores[row['beach_id']] += row['score']

                    if table == rainfall:
                        rainfall_scores[row['beach_id']] = row['score']
                    elif table == jellyfish:
                        jellyfish_scores[row['beach_id']] = row['score']
                    elif table == beach_score:
                        beach_scores[row['beach_id']] = row['score']
                        beach_names[row['beach_id']] = row['beach_name']

        # 점수가 가장 높은 해수욕장 순으로 정렬합니다.
        sorted_beaches = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # 최상위 3개의 해수욕장을 선택합니다.
        top_beaches = [
            {
                'beach_name': beach_names[beach[0]],
                'total_score': beach[1],
                'rainfall_score': rainfall_scores.get(beach[0], 0),
                'jellyfish_score': jellyfish_scores.get(beach[0], 0),
                'beach_score': beach_scores.get(beach[0], 0)
            }
            for beach in sorted_beaches[:3]
        ]

        return Response(top_beaches)

