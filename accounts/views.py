from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm



from accounts.models import *
from accounts.filters import OrderFilter

from accounts.forms import OrderForm

# Create your views here.

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


def products(request):

    product = Product.objects.all()
    return render(request, 'accounts/products.html',{'product_list' : product })



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



def deleteOrder(request,order_pk):
    item= Order.objects.get(pk=order_pk)

    if request.method == "POST":

        item.delete()
        return redirect('home')




    context= {

            'item':item
    }

    return render(request, 'accounts/deleteorderform.html',context)


def registerUser(request):

    form = UserCreationForm()

    context = {

        'form':form

    }

    return render(request, 'accounts/registrationpage.html', context)


def loginUser(request):

    context = {


    }

    return render(request, 'accounts/loginpage.html', context)