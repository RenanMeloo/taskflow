from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, UserSerializer


class RegisterViews(generics.CreateAPIView):
    # choose the serializer for the view
    serializer_class = RegisterSerializer
    # set the permission classes for the view
    permission_classes = [AllowAny]


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        # The profile is always the logged-in user's
        return self.request.user
