from dataclasses import field
from wsgiref.validate import validator
from rest_framework import serializers
from .models import RetailStore


def validate_file_name(file):
    if not str(file).endswith(".csv"):
        raise serializers.ValidationError("Uploaded file is not a csv file.")

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(validators=[validate_file_name])



class RetailStoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailStore
        fields = "__all__"