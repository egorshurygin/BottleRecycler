from django.urls import path, include
from app.product.views import *

urlpatterns = [
    path('write/points', CreateDisplayCode.as_view()),
    path('read/balance', GetCardBalance.as_view()),
    path("change/balance", ChangeCardBalance.as_view())
]