from distutils import errors
from json import JSONDecodeError
from logging import raiseExceptions
from time import sleep
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core import serializers as core_serializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .serializer import *
from .models import RetailStore
from .forms import InputForm, SearchForm, UpdateForm
from rest_framework.decorators import api_view
from django import forms
# Create your views here.
@api_view(['GET'])
def appView(request):
    if request.method == "GET":
        form1 = InputForm()
        form2 = SearchForm()
        form3 = UpdateForm()
        return render(request, 'myapp/base.html', {'upload_form': form1, 'search_form': form2, 'update_from': form3 })    

@api_view(['POST'])
def uploadView(request):
    if request.method == "POST":
        try:
            upload_serailzer = UploadSerializer(data=request.FILES)
            if upload_serailzer.is_valid(raise_exception=True):
                file = upload_serailzer.validated_data['file']
                reader = pd.read_csv(file)
                for _, row in reader.iterrows():
                    store_id = row['store_id']
                    sku = row['sku']
                    retail_store_obj = RetailStore.objects.filter(store_id=store_id, sku=sku).first()
                    if retail_store_obj:
                        retail_store_serializer = RetailStoreDataSerializer(retail_store_obj, data=dict(row))
                    else:
                        retail_store_serializer = RetailStoreDataSerializer(data=dict(row))
                    if retail_store_serializer.is_valid(raise_exception=True):
                        retail_store_serializer.save()
                
                
                # retail_store_queryset = RetailStore.objects.all()
                # ser = RetailStoreDataSerializer(retail_store_queryset, many=True)
                # return Response({"status": "Successful", "data": ser.data}, status=status.HTTP_200_OK) 
                
                return Response({"status": "Successfully uploaded"}, status=status.HTTP_200_OK)          

        except serializers.ValidationError as e:
            return Response({"message": "Validation Failure", "error": repr(e.detail)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print('exception', e)
            return Response({"message": "Failed to process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def searchView(request):
    if request.method == "POST":
        try:
            form = SearchForm(request.POST)
            if form.is_valid():
                kwargs = dict()
                data = form.cleaned_data
                for key , val in data.items():
                    if data[key]:
                        kwargs[key] = val
                if "product_name" in kwargs:
                    product_name = kwargs.pop('product_name')
                    retail_store_qs = RetailStore.objects.filter(product_name__icontains=product_name,**kwargs).values("store_id", "sku", "product_name", "price", "date")
                else:
                    retail_store_qs = RetailStore.objects.filter(**kwargs).values("store_id", "sku", "product_name", "price", "date")
                seralizer = RetailStoreDataSerializer(retail_store_qs, many=True)
                return Response({"status": "Successful", "pricing_data": seralizer.data}, status=status.HTTP_200_OK) 
            else:
                return Response({"message": "Validation Failure", "error": repr(form.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print('exception', e)
            return Response({"message": "Failed to process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updateView(request):
    if request.method == "POST":
        try:
            form = UpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                store_id = form.cleaned_data.get('store_id')
                sku = form.cleaned_data.get('sku')
                product_name = form.cleaned_data.get('product_name')
                price = form.cleaned_data.get('price')
                date = form.cleaned_data.get('date')
                retail_store_obj = RetailStore.objects.filter(store_id=store_id, sku=sku).first()
                if retail_store_obj:
                    if product_name:
                        retail_store_obj.product_name = product_name
                    if price:
                        retail_store_obj.price = price
                    if date:
                        retail_store_obj.date = date
                    
                    retail_store_obj.save()
                    return Response({"status": "Successfully updated"}, status=status.HTTP_200_OK) 
                else:
                    return Response({"status": "Failed to update. Record does not exist"}, status=status.HTTP_400_BAD_REQUEST) 
            else:
                return Response({"message": "Validation Failure", "error": repr(form.errors)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # print('exception', e)
            return Response({"message": "Failed to process the request"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



