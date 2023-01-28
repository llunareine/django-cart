from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .models import User, Item
from rest_framework import status
from rest_framework import generics


from django.shortcuts import get_object_or_404, render


# Вместо функций, будем использовать классы, шо бы можно было наследовать класс APIView и получить доступ к методам get,post, delete
# class Users(APIView):
#     def get(self, request): #для полуяения данных запроса пишем реквест во всех функциях в вью
#         users = User.objects.all()
#         serializer = serializers.UserSerializer(users, many=True) # мэни тру это ставим всегда когда передаем лист обьектов
#         return Response(serializer.data)
#
#     # def get(request, user_id):
#     #     user = get_object_or_404(User, pk=user_id)
#     #     return (request, 'api/users/<int:user_id', {'user': user})
#
#     # def get(self, request, user_id):
#     #     users = User.objects.all()
#     #     serializer = serializers.UserSerializer(users, many=True)  # мэни тру это ставим всегда когда передаем лист обьектов
#     #     return Response(serializer.data)
#
#     def post(self, request):
#         serializer = serializers.UserSerializer(data=request.data) #дата=реквест.дата - в сериалайзер передает данные из этого запмроса
#         if serializer.is_valid():
#             # вызываем метод save для сохранения
#             serializer.save()
#             # Возвращаем JSON с данными, которые мы добавили в БД
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # если валидация провалилась, возвращаем сообщение об ошибке и статус 400
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class UserDetail(APIView):
#     def get(self, request, user_id):  # для полуяения данных запроса пишем реквест во всех функциях в вью
#         users = User.objects.get(pk=user_id)
#         serializer = serializers.UserSerializer(users)  # мэни тру это ставим всегда когда передаем лист обьектов
#         return Response(serializer.data)
#
#     def delete(self, request, user_id):  # для полуяения данных запроса пишем реквест во всех функциях в вью
#         users = User.objects.filter(pk=user_id).delete()
#         serializer = serializers.UserSerializer(users, many=True)  # мэни тру это ставим всегда когда передаем лист обьектов
#         return Response(serializer.data)
#
#     def put(self,request, user_id):
#         users = User.objects.get(pk=user_id)
#         serializer = serializers.UserSerializer(users, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#         return Response(serializer.data)

class UserList(generics.ListCreateAPIView):
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        obj = get_object_or_404(User, id=user_id)
        return obj

class Items(generics.ListCreateAPIView):
    serializer_class = serializers.UserItemSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return User.objects.filter(id=user_id)

