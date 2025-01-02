from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

class LoginForm(forms.Form):  # Renamed to follow Python naming conventions
    identifier = forms.CharField(
        max_length=60,
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter username or email'
        })
    )
    password = forms.CharField(
        max_length=60,
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        identifier = cleaned_data.get("identifier")
        password = cleaned_data.get("password")
        
        if not identifier or not password:
            raise forms.ValidationError("Please fill in all fields")

        user = None
        try:
            # First try username
            user = User.objects.get(username=identifier)
        except User.DoesNotExist:
            try:
                # Then try email
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid credentials")

        if user:
            user = authenticate(username=user.username, password=password)
            if not user:
                raise forms.ValidationError("Invalid credentials")
            
        cleaned_data['user'] = user
        return cleaned_data

class RegisterForm(forms.ModelForm):  # Renamed for consistency
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email'
        })
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create password'
        })
    )
    repeat_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm password'
        })
    )
    
    class Meta:
        model = User
        fields = ["username", "email", "password", "repeat_password"]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")
        
        if password and repeat_password and password != repeat_password:
            raise forms.ValidationError({
                "repeat_password": "Passwords do not match"
            })

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user