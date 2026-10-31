from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer


class RegisterViews(generics.CreateAPIView):
    # choose the serializer for the view
    serializer_class = RegisterSerializer
    # set the permission classes for the view
    permission_classes = [AllowAny]