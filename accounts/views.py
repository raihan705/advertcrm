from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group



from accounts.models import *
from accounts.filters import OrderFilter

from accounts.forms import OrderForm, UserRegistrationForm
from accounts.decorators import unauthenticated_user, allowed_user,admin_only

# Create your views here.


@login_required(login_url= 'login')
@admin_only
def home(request):

    # for customer table from database tendering all  data

    customers = Customer.objects.all()

    # from order table from database rendering all data
    orders = Order.objects.all()

    # for total order count, pending and delivered from Order table

    total_order = orders.count()
    total_pending = orders.filter(status='Pending').count()
    total_delivered  = orders.filter(status='Delivered').count()

    # stored in a variable with creating a dictionary  data from two tables

    context = {'customer':customers, 'order': orders, 'total_order':total_order, 'total_pending':total_pending,
     'total_delivered':total_delivered }

    return render(request, 'accounts/dashboard.html',context)


def userpage(request):
    context  = {

    }

    return render(request, 'accounts/userpage.html', context)




@ login_required(login_url= 'login')
@allowed_user(allowed_roles=['admin'])
def products(request):

    product = Product.objects.all()
    return render(request, 'accounts/products.html',{'product_list' : product })


@ login_required(login_url= 'login')
@allowed_user(allowed_roles=['admin'])
def customer(request,customer_pk):

    #get a single customer info
    customer = Customer.objects.get(pk=customer_pk)

    # customers product info that contain order and product table also

    orders = customer.order_set.all()

    # for total order count of the customer
    order_count = orders.count()

    # filter the customer info

    myfilter = OrderFilter( request.GET, queryset = orders )
    orders = myfilter.qs

    context={

            'customer':customer, 'order':orders, 'order_count':order_count, 'myfilter': myfilter

    }
    return render(request, 'accounts/customer.html',context)

@ login_required(login_url= 'login')
@allowed_user(allowed_roles=['admin'])
def createOrder(request,customer_pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields= ('product','status'), extra=4)
    name=Customer.objects.get(pk=customer_pk)
    formset = OrderFormSet(queryset=Order.objects.none(),  instance=name ) 
    #form = OrderForm(initial ={'customer':name })
    if request.method == "POST":
        formset = OrderFormSet (request.POST, instance=name)
        if formset.is_valid():
            formset.save()
            return redirect('home')


    

    context = {

            'form':formset

    }

    return render (request,'accounts/order_form.html', context)


@ login_required(login_url= 'login')
@allowed_user(allowed_roles=['admin'])
def updateOrder(request,order_pk):

    order_id = Order.objects.get(pk=order_pk)
    form = OrderForm( instance=order_id)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order_id)
        if form.is_valid():
            form.save()
            return redirect('home')

    
    
    context = {

            'form':form

    }

    return render (request,'accounts/order_form.html', context)


@ login_required(login_url= 'login')
@allowed_user(allowed_roles=['admin'])
def deleteOrder(request,order_pk):
    item= Order.objects.get(pk=order_pk)

    if request.method == "POST":

        item.delete()
        return redirect('home')




    context= {

            'item':item
    }

    return render(request, 'accounts/deleteorderform.html',context)

@unauthenticated_user
def registerUser(request):

    
    form = UserRegistrationForm

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            

            # for getting Username for messages

            username = form.cleaned_data.get('username')
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)
            messages.success(request, 'Accoutn is created successfully for ' + username)
            return redirect('login')

    context = {

        'form':form

    }

    return render(request, 'accounts/registrationpage.html', context)


    
@unauthenticated_user
def loginUser(request):

    

    if request.method == 'POST':
        username= request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('home')

        else:
            messages.info(request,'Username or password is incorrect')

    context = {


    }

    return render(request, 'accounts/loginpage.html', context)


    


def logOut(request):
    logout(request)
    return redirect('login')
     
