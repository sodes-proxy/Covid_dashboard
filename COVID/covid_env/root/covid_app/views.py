from django.shortcuts import render
from django.utils.safestring import SafeString
from rest_framework import viewsets
from rest_framework.response import Response

from .models import COVIDData
from .serializers import StateSexSerializer, StateSexAgeSerializer

import pandas as pd
import json
# Create your views here.


def index(request):
    f = open('..\\..\\..\\..\\Covid_dashboard\\COVID\\json_files\\graph-2.json',)
    data=json.load(f)
    context = {'data_json': SafeString(data)}
    return render(request, 'covid_app/index.html', context)

def graph1(request):
    f = open('..\\..\\..\\..\\Covid_dashboard\\COVID\\json_files\\graph-1.json',)
    data=json.load(f)
    context = {'data_json': SafeString(data)}
    return render(request, 'covid_app/graph1.html', context)
def graph3(request):
    f = open('..\\..\\..\\..\\Covid_dashboard\\COVID\\json_files\\graph-3.json',)
    data=json.load(f)
    context = {'data_json': SafeString(data)}
    return render(request, 'covid_app/graph3.html', context)
def graph4(request):
    f = open('..\\..\\..\\..\\Covid_dashboard\\COVID\\json_files\\graph-4.json',)
    data=json.load(f)
    context = {'data_json': SafeString(data)}
    return render(request, 'covid_app/graph4.html', context)

def pie_chart(request):
    # covid_df = pd.DataFrame.from_records(data)
    donut_json = '[ { "region": "East", "fruit": "Apples", "count": "53245" }, { "region": "West", "fruit": ' \
                 '"Apples", "count": "28479" }, { "region": "South", "fruit": "Apples", "count": "19697" }, ' \
                 '{ "region": "North", "fruit": "Apples", "count": "24037" }, { "region": "Central", ' \
                 '"fruit": "Apples", "count": "40245" }, { "region": "East", "fruit": "Oranges", "count": "200" ' \
                 '}, { "region": "South", "fruit": "Oranges", "count": "200" }, { "region": "Central", ' \
                 '"fruit": "Oranges", "count": "200" }] '
    context = {'data_json': SafeString(donut_json)}
    return render(request, 'covid_app/donut.html', context)


class StateSexSet(viewsets.ModelViewSet):
    queryset = COVIDData.objects.all()
    serializer_class = StateSexSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_fields = ['entidad_res', 'municipio_res']


class StateSexAgeSet(viewsets.ViewSet):
    queryset = COVIDData.objects.all()
    serializer_class = StateSexAgeSerializer

    def list(self, request, *args, **kwargs):
        # age = request.GET['age']
        # covid_df = pd.DataFrame.from_records(COVIDData.objects.filter(edad__gt=age). \
        #                                     values('id_registro', 'sexo', 'entidad_res', 'municipio_res', 'edad'))
        # print(covid_df)
        # df = covid_df["sexo"].value_counts()
        # print(df)
        # return Response(str(covid_df.to_json(orient='records')))
        donut_json = '[ { "region": "East", "fruit": "Apples", "count": "53245" }, { "region": "West", "fruit": ' \
                     '"Apples", "count": "28479" }, { "region": "South", "fruit": "Apples", "count": "19697" }, ' \
                     '{ "region": "North", "fruit": "Apples", "count": "24037" }, { "region": "Central", ' \
                     '"fruit": "Apples", "count": "40245" }, { "region": "East", "fruit": "Oranges", "count": "200" ' \
                     '}, { "region": "South", "fruit": "Oranges", "count": "200" }, { "region": "Central", ' \
                     '"fruit": "Oranges", "count": "200" }] '
        return Response(SafeString(donut_json))
