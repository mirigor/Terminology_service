from rest_framework import serializers
from .models import ReferenceBook, ReferenceBookElement


class ReferenceBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceBook
        fields = '__all__'


class ReferenceBookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceBookElement
        fields = '__all__'
