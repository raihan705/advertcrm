from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_funtion):
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('home')

        else:
            return view_funtion(request, *args, **kwargs)

    return wrapper

def allowed_user(allowed_roles = []):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:

                return view_function(request, *args, **kwargs)

            else:

                return HttpResponse ('You are not allowed to this page..')

            

        return wrapper

    return decorator


def admin_only(view_function):
    def wrapper(request, *args, **kwarg):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('userpage')

        if group == 'admin':
            
            return view_function(request, *args, **kwarg)

    return wrapper
