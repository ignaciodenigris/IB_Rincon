from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import Registrar_Form
from django.contrib.auth.forms import AuthenticationForm

def registrar_view(request):
    if request.method == 'POST':
        form=Registrar_Form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada')
            return redirect ('login')
    else:
        form = Registrar_Form()
    return render (request,'Rincon/registrar_cuenta.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
           username = form.cleaned_data.get('username')    
           password = form.cleaned_data.get('password')
           user = authenticate(username=username, password=password)
           if user is not None:
                login(request, user)
                messages.info(request, 'Welcome {username}')
                return redirect ('/')
           else:
             messages.error(request, 'Invalid username or password')
        else: 
          messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'Rincon/login.html', {'form': form})