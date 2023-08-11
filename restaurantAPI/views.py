from django.shortcuts import render
from rest_framework import generics, routers, viewsets
from rest_framework.decorators import api_view
from restaurant.models import Menu, Booking
from .seriallizers import MenuSerializer, BookingSerializer


class MenuView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class SingleMenuView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

