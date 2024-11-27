from django.shortcuts import render,redirect
from .forms import login_form,RegisterStep_1
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
# Create your views here.

class login_view(FormView):
    template_name = "login.html"
    form_class = login_form
    success_url = reverse_lazy("home")
    def form_valid(self,form):
        user = form.cleaned_data['user']
        login(self.request,user)
        return super().form_valid(form)
    def form_invalid(self, form):
        # عرض نموذج مع الأخطاء إذا فشل التحقق
        return self.render_to_response(self.get_context_data(form=form))
    
def home_view(request):
    return render(request,'home.html')
class Register_view(FormView):
    template_name = "register_1.html"
    form_class = RegisterStep_1
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        User.objects.create_user(
            username = cleaned_data["username"],
            email = cleaned_data["email"],
            password = cleaned_data["password"]
        )
        return super().form_valid(form)
    def form_invalid(self, form):
      
        print("النموذج يحتوي على أخطاء:", form.errors)
        
       
        return self.render_to_response(self.get_context_data(form=form))