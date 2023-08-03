import csv

from django.http import HttpRequest, HttpResponse, JsonResponse

# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import LifesavingEquipment
from .serializers import CalcSerializer


def index(request: HttpRequest):
    response = {"message": "Hi world it is updated!?"}
    return JsonResponse(response)


# Create your views here.
@api_view(["GET"])
def randomAPI(request):
    totalCalcs = LifesavingEquipment.objects.all()  # 모델로 만들어진 객체를 모두 가져오기
    serializer = CalcSerializer(totalCalcs, many=True)  # 다양한 내용들에 대해 내부적으로도 직렬화
    return Response(serializer.data)


data = None
file_dir = "C:/Users/jinse/"


def read_data(table_name):
    with open(file_dir + f"{table_name}.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        global data
        data = list(reader)
        return


def footer(table_name, class_name, bulk_list):
    class_name.objects.bulk_create(bulk_list)

    with open(file_dir + f"{table_name}.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
    return print(writer)


def add_equipment(request):
    read_data("equipment")
    if not data:
        return HttpResponse("Nothing to update")

    arr = []
    for row in data:
        arr.append(
            LifesavingEquipment(
                equipment_long=row[0],
                equipment_lat=row[1],
                spot=row[2],
            )
        )

    footer("equipment", LifesavingEquipment, arr)
    return HttpResponse("LifesavingEquipment table updated")
