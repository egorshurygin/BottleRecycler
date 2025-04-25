from rest_framework import generics
from app.product.models import DisplayCode, CardBalance
from app.product.serializers import DisplayCodeSerializer, CardBalanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.TG.CodeFromDisplay import encode_in_message_on_display, get_lasts, way
from app.TG.DataBase import get_balance_by_card_id, get_telegram_id_by_card_id, change_balance_by_card_id
from app.TG.TG_BOT import agree, agree2
from sqlite3 import *
from random import *
import os


class CreateDisplayCode(APIView):
    def post(self, request, format=None):
        print('test', way)
        text = request.data.get('points')
        message = encode_in_message_on_display(text)
        print(f'{text} - {message}')
        return Response(message, status=status.HTTP_201_CREATED, headers={'display_code': message})


class GetCardBalance(APIView):
    def get(self, request, format=None):
        text = request.GET.get('card_id')
        message = get_balance_by_card_id(text)
        if "Error" in message:
            return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED, headers={'error': message})
        return Response(message, status=status.HTTP_201_CREATED, headers={'balance': message})


class ChangeCardBalance(APIView):
    def post(self, request, format=None):
        card = request.data.get('card_id')
        summ = request.data.get('summ')
        message = change_balance_by_card_id(card, summ)
        d = {}
        if 'OK' in message:
            return Response(message, status=status.HTTP_201_CREATED)
        return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED, headers={'error': message})