from django.shortcuts import redirect
from django.conf.global_settings import LOGIN_URL


def is_manager(login_url=LOGIN_URL):
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Manager
                if request.user.is_manager or request.user.is_superuser:
                    return func(request, *args, **kwargs)
            return redirect(login_url)
        return wrapper
    return inner


def is_student(login_url=LOGIN_URL):
    def inner(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Student
                if not request.user.is_manager and not request.user.is_superuser:
                    return func(request, *args, **kwargs)
            return redirect(login_url)

        return wrapper
    return inner
