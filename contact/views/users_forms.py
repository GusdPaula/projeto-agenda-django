from django.shortcuts import render, redirect
from contact.forms import RegisterForm, RegisterUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

@login_required(login_url='contact:login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(request,'contact/register.html',
                    {
                        'form':form,
                        'title':"Update user",
                    })
    

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(request,'contact/register.html',
                    {
                        'form':form,
                        'title':"Update user",
                    })

    form.save()
    return redirect('contact:user_update')
    

# Create your views here.
def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário registrado!')

            return redirect('contact:login')

    return render(request,'contact/register.html',
                  {
                      'form':form,
                      'title':'Register user',
                  })

def login_view(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)

            messages.success(request, 'You are online!')

            return redirect('contact:index')
        
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request,'contact/login.html',
                  {
                      'form':form,
                  })


@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)

    return redirect('contact:login')