from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import RegisterUserSerializer, ManageUserSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = ManageUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
