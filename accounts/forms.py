from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
class login_form(forms.Form):
    identifier = forms.CharField(max_length=60,label="البريد الإلكتروني أو اسم المستخدم")
    password = forms.CharField(max_length=60,label="كلمة المرور")
    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")
        user = None
        try:
            user = User.objects.get(username =identifier)
        except User.DoesNotExist:
            try:

                 user = User.objects.get(email = identifier)
            except User.DoesNotExist:
                pass
        if user:
                user = authenticate(username = user.username,password = password)
        if not user:
                raise forms.ValidationError("بيانات الدخول غير صحيحة")
        cleaned_data['user'] = user
                
        return cleaned_data


class RegisterStep_1(forms.ModelForm):
    username = forms.CharField(max_length=50,required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,widget=forms.PasswordInput)
    repeat_password = forms.CharField(required=True,widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ["username","email","password","repeat_password"]
    def clean(self):
         cleaned_data = super().clean()
         username = cleaned_data.get("username")
         email = cleaned_data.get("email")
         password = cleaned_data.get("password")
         repeat_password = cleaned_data.get("repeat_password")
         if password != repeat_password:
              raise  forms.ValidationError("the password is not the some !")
         if User.objects.filter(username = username).exists():
              raise forms.ValidationError("this username is already exist")
         if User.objects.filter(email = email).exists():
              raise forms.ValidationError("this Email is already exist")       
              
        
    
         return cleaned_data