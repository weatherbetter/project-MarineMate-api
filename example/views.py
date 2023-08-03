from django.http import HttpRequest, HttpResponse, JsonResponse

# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LifesavingEquipment
from .serializers import EquipmentSerializer


def index(request: HttpRequest):
    response = {"message": "Hi world it is updated!?"}
    return JsonResponse(response)


# Create your views here.
@api_view(["GET"])
def equipmentAPI(request):
    totalequipment = LifesavingEquipment.objects.all()  # 모델로 만들어진 객체를 모두 가져오기
    serializer = EquipmentSerializer(totalequipment, many=True)  # 다양한 내용들에 대해 내부적으로도 직렬화
    return Response(serializer.data)
