from rest_framework import serializers
from app.product.models import DisplayCode, CardBalance


class DisplayCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DisplayCode
        fields = '__all__'


class CardBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardBalance
        fields = '__all__'

