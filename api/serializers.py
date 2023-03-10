from rest_framework import serializers #for serializer
from django.contrib.auth.hashers import make_password #for hashing password
import re

from . import models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ['id', 'item', 'price']

class UserSerializer(serializers.ModelSerializer): #M


    def validate_username(self, value):  #можно делать кастомную валидацию обьявляя функцию валидейт_название поля (селф валую)
        if len(value) < 5:
            raise serializers.ValidationError("Username should be not less than 5 letters") # raise он типа прерывает и вызывает вт это
        return value


    def validate_password(self, password):  # можно делать кастомную валидацию обьявляя функцию валидейт_название поля (селф валую)
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$'
        if re.match(pattern, password) is None:
            raise serializers.ValidationError(
                "Password should contain at least 8 characters, 1uppercase and lowercase characters")  # raise он типа прерывает и вызывает вт это
        return password

    class Meta:
        model = models.User
        fields = ['id', 'username', 'password']


        # from rest_framework import serializers
        # class CommentSerializer(serializers.Serializer):
        #     email = serializers.EmailField()
        #     content = serializers.CharField(max_length=200)
        #     created = serializers.DateTimeField()  крч сверху то же самое что и здесь чтобы уменьшить код используется класс Мета

    # можно переписывать методы сериализации
    # есть create - для создания, save - для обновления, мб ещё есть, остальные не нашёл :D
    def create(self, validated_data):
        # validated_data пушто это уже отвалидированные данные, т.е прошли все проверки, но ещё не стали JSON
        # сейчас мы будем хэшировать пароль с помощью метода make_password()
        # validated_data['password'] - берем отвалидированный пароль и даём ему новое значение пихая этот же пароль в метод make_password
        validated_data['password'] = make_password(validated_data['password'])
        # мы хотим использовать метод create из класса ModelSerializer, но при этом мы добавили доп.функциональность - хэшировали пароль
        # поэтому используем super().create(validated_data) для добавления нашей доп.функции
        return super(UserSerializer, self).create(validated_data)
    # супер это класс чтобы использовать и переписывать родитль методы класса

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        # return instance
        # мы хотим использовать метод create из класса ModelSerializer, но при этом мы добавили доп.функциональность - хэшировали пароль
        # поэтому используем super().create(validated_data) для добавления нашей доп.функции
        return instance

class UserItemSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = models.User
        fields = ['items']

    def create(self, validated_data):
        user_id = self.context['view'].kwargs['user_id']
        user = models.User.objects.get(id=user_id)
        items_data = validated_data.pop('items')
        items = []
        for item_data in items_data:
            item, created = models.Item.objects.get_or_create(item=item_data['item'], defaults={'price': item_data['price']})
            items.append(item)
        user.items.add(*items)
        return user

    def update(self, instance, validated_data):
        user_id = self.context['view'].kwargs['user_id']
        user = models.User.objects.get(id=user_id)
        items_data = validated_data.pop('items')
        items = []
        for item_data in items_data:
            item, created = models.Item.objects.get_or_update(item=item_data['item'], defaults={'price': item_data['price']})
            items.append(item)
        user.items.add(*items)
        return user
