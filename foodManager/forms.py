from django import forms
from .models import Registro
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class ConsumirForm(forms.ModelForm):

    class Meta: 
        model = Registro
        fields = ('cantidad_comprada',)

class CustomUserCreationUserForm(forms.Form):
    first_name = forms.CharField(label='Nombre', min_length=3, max_length=100)
    username = forms.CharField(label='Usuario', min_length=4, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma contraseña', widget=forms.PasswordInput)

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name'].lower()
        return first_name

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username = username)
        if r.count():
            raise ValidationError("Usuario ya existente")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email ya existente")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas son diferentes")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
        )
        return user