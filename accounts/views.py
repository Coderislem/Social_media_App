from django.shortcuts import render,redirect
from .forms import login_form,RegisterStep_1
from django.views.generic.edit import FormView
from django.views.generic import CreateView
from .models import Profile
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from posts.views import Profile_posts
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
       
        return self.render_to_response(self.get_context_data(form=form))
@login_required  
def home_view(request):
    context = {"username":request.user.username}
    
    return render(request,'home.html',{"context":context})
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
      
        print("invalid form !", form.errors)
        
       
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    logout(request)
    return redirect("login")

def profile(request):
    posts = Profile_posts(request,request.user.id)
    profile_info = Profile.objects.get(user = request.user)

    return render(request,"profile.html", {"posts":posts,"profile_info":profile_info})

