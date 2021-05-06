from django.shortcuts import render,redirect
from django.http import HttpResponse
from user_app.forms import CustomRegisterForm
 
# Create your views here.
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        register_form = CustomRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()

            messages.success(request , ("New User account created"))
            return redirect('todolist')
    else:

        register_form = CustomRegisterForm()
    return render(request, 'register.html' , {'register_form' : register_form})
