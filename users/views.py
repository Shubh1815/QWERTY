from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm


from .forms import LoginForm
from qwerty.settings import LOGIN_URL


def login_view(request):
    login_url = reverse_lazy("login")

    student_success_url = reverse_lazy('student:dashboard')
    manager_success_url = reverse_lazy("manager:dashboard", kwargs={
        'category': 0,
    })

    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_manager or request.user.is_superuser:
                return redirect(manager_success_url)
            return redirect(student_success_url)

        context = {'form': LoginForm}
        return render(request, 'registration/login.html', context=context)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            # Manager
            if user.is_manager or user.is_superuser:
                return redirect(manager_success_url)

            # Student
            return redirect(student_success_url)

        messages.error(request, 'Username or Password is incorrect.')
        return redirect(login_url)


@login_required(login_url=LOGIN_URL)
def logout_view(request):
    if request.user:
        logout(request)
    return redirect(reverse_lazy("login"))


@login_required(login_url=LOGIN_URL)
def change_password(request):
    if request.method == 'GET':
        password_change_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password Changed Successfully!")
            return redirect(reverse_lazy("change_password"))

        messages.error(request, "Incorrect Details!")

    context = {
        'password_change_form': password_change_form
    }

    # Manager
    if request.user.is_superuser or request.user.is_manager:
        return render(request, 'registration/manager_change_password.html', context=context)

    #Student
    return render(request, 'registration/student_change_password.html', context=context)
