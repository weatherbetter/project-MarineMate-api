# from .serializers import AccidentSerializer,AccidentMonthSerializer
from django.db.models import Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view

# drf
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Accident, LifesavingEquipment
from .serializers import EquipmentSerializer


def index(request: HttpRequest):
    response = {"message": "Hi world it is updated!?"}
    return JsonResponse(response)


# 수난사고 현황 API


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
def equipmentAPI(request):
    totalequipment = LifesavingEquipment.objects.all()  # 모델로 만들어진 객체를 모두 가져오기
    serializer = EquipmentSerializer(totalequipment, many=True)  # 다양한 내용들에 대해 내부적으로도 직렬화
    return Response(serializer.data)
