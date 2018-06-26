from rest_framework import serializers
from .models import Producto, Registro
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ('id', 'nombre', 'marca', 'cantidad_actual')

class RegistroSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Registro
        fields = ('id', 'producto', 'usuario', 'fecha', 'cantidad_comprada')

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            email = validated_data['email'],
            password = make_password(validated_data['password'])
        )
        user.save()
        return user