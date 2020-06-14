from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_funtion):
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('home')

        else:
            return view_funtion(request, *args, **kwargs)
            
    return wrapper