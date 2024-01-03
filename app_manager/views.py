from django.shortcuts import render
from app_manager.models import User
from rest_framework import generics, permissions
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework import viewsets
from .models import App, Plan, Subscription
from .serializers import AppSerializer, PlanSerializer, SubscriptionSerializer,UserRegisterSerializer, PasswordResetSerializer, SubscriptionReadSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class UserSignUpView(generics.CreateAPIView, generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer_registration = self.serializer_class(data=request.data)
        if not serializer_registration.is_valid():
            return Response({'result': serializer_registration.errors})
        user = serializer_registration.save()
        serialized_data = UserRegisterSerializer(user).data
        return Response({"result": "User Register Successfully", "data": serialized_data})


class PasswordResetView(CreateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Password reset successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.select_related("owner", "subscription").all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.owner == self.request.user:
            serializer.save()
        else:
            raise PermissionDenied(detail="You don't have permission to perform this action")

    def perform_destroy(self, instance):
        if instance.owner == self.request.user:
            instance.delete()
        else:
            raise PermissionDenied(detail="You don't have permission to perform this action")

class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]  

    def list(self, request, *args, **kwargs):
        queryset = Subscription.objects.all()
        serializer_data = SubscriptionReadSerializer(queryset, many=True).data

        return Response(serializer_data)

    def create(self, request, *args, **kwargs):
        plan_name = request.data.get('plan_name', None)
        if not plan_name:
            return Response({"message": "Plan name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            return Response({"message": f"Plan with name '{plan_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        plan_name = request.data.get('plan_name', None)
        if not plan_name:
            return Response({"message": "Plan name is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            return Response({"message": f"Plan with name '{plan_name}' does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.pop('partial', False))
        serializer.is_valid(raise_exception=True)
        serializer.save(plan=plan)
        return Response(serializer.data)
    
    def perform_destroy(self, instance):
        instance.active = False
        instance.save()