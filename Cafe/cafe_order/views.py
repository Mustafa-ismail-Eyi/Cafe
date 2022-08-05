from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from .forms import CustomerLoginForm, CustomerRegisterInForm
from .models import Customer, Foods, Order, OrderFoods
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .utils import utils
from django.contrib.auth.models import User
import datetime
from django.db.models import Avg, Count, Min, Max, Sum
from django import template



def welcome(request):
    return render(request, 'cafe_order/welcome.html')

# This view renders a registration form
# The view controls the is user already in database or not
# And also user both saved on Customer model and django admin's user model
def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegisterInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['customer_email']
            
            if Customer.objects.filter(customer_email=email).exists():
                user = form.cleaned_data.get('customer_name_surname')
                messages.info(
                    request, 'User already exists! Try logging in.')
                return redirect('cafe_order:login')
            else:
                customer={
                    'customer_email':form['customer_email'].value(),
                    'customer_username':utils.create_user_name(form['customer_email'].value()),
                    'customer_password':form['customer_password'].value(),
                    'customer_name_surname':form['customer_name_surname'].value()
                }
                customer_model = Customer(**customer)
                customer_model.save()
                user = User.objects.create_user(first_name = customer['customer_name_surname'], username = customer['customer_username'], password = customer['customer_password'],email=customer['customer_email'])
                user.is_active = True
                user.save()
                return redirect('cafe_order:login')
    else:
        form = CustomerRegisterInForm()
    context = {
        'form':form
    }
    return render(request, "cafe_order/customer_register.html", context)


# This view renders a login form
# with help of authenticate function users get in
def customer_login(request):
    if request.user.is_authenticated:
        return redirect('cafe_order:home')
    else:
        if request.method == 'POST':
            form = CustomerLoginForm(request.POST)
            if form.is_valid():

                password = form.cleaned_data['customer_password']
                user = authenticate(request, username = utils.create_user_name(form['customer_email'].value()), password=password)
                if user is not None:
                    login(request, user)
                    return redirect('cafe_order:home')
                else:
                    return redirect('cafe_order:login')
        else: 
            form = CustomerLoginForm()
        context = {
            'form': form
        }
        return render(request, 'cafe_order/customer_login.html', context)

# This views where the customer pick foods in other words items into cart 
@login_required(login_url='cafe_order:login')
def customer_home(request):
    foods = Foods.objects.all()
    context = {'foods': foods}
    return render(request, 'cafe_order/customer_home.html',context=context)

# This helps logout the customer
# Customer session lifetime is already controlled by SessionIdleTimeout which is in Cafe/middleware.py
@login_required(login_url='cafe_order:login')
def customer_logout(request):
    logout(request)
    return redirect('cafe_order:login')

# when user add an food on cart it creates a order until confirms her order item will added on that created order 
@login_required(login_url='cafe_order:login')
def create_order(request,id):
    customer =  Customer.objects.filter(customer_email__iregex=f'{request.user}+@.+')[0]
    filtered_order = Order.objects.filter(customer_id = customer.id, order_status = Order.STATUS[0][0])
    if filtered_order.exists():
        food_list = OrderFoods(order_id = filtered_order[0], food_id = Foods.objects.get(id=int(id)))
        food_list.save()
    else:
        order = Order(
                customer_id = customer,
                order_recieved_date = datetime.datetime.utcnow(), 
                order_status = Order.STATUS[0][0]
            )
        order.save()
        food_list = OrderFoods(order_id = order, food_id = Foods.objects.get(id=int(id)))
        food_list.save()
    return redirect('cafe_order:home')

# This views render the customer's current active cart
@login_required(login_url='cafe_order:login')
def list_orders(request):

    order_foods = OrderFoods.objects.filter(order_id__customer_id=Customer.objects.get(customer_email__iregex=f'{request.user}+@.+'),
                                            order_id__order_status = Order.STATUS[0][0]                                         
                                            ).select_related('order_id','food_id')

    order = Order.objects.filter(customer_id=Customer.objects.get(customer_email__iregex=f'{request.user}+@.+'),order_status = Order.STATUS[0][0] )
    if order:
        context = {
            'order_id': order[0].id,
            'order_foods':order_foods,

        }
    else:
        context = {
            'order_foods':order_foods,
            'order_id' : None
        }
    return render(request, 'cafe_order/customer_active_orders.html',context=context)

# Customer can remove the foods from cart before she confirms
@login_required(login_url='cafe_order:login')
def delete_food(request, id):
    OrderFoods.objects.filter(id=id).delete()

    #return redirect('cafe_order:list_orders')
    return redirect(request.META.get('HTTP_REFERER'))

# Customer confirms the current cart and status of order is changed
@login_required(login_url='cafe_order:login')
def confirm_order(request,id):
    order = Order.objects.get(id=int(id))
    order.order_status = Order.STATUS[1][0]
    order.save()
    # return (f"Do you want to confirm this that item? {id}")
    return redirect('cafe_order:home')

#This view renders the list of confirmed order which status are 'delivery taken'
@login_required(login_url='cafe_order:login')
def confirmed_order(request):

    order = Order.objects.filter(customer_id=Customer.objects.get(customer_email__iregex=f'{request.user}+@.+'),order_status = Order.STATUS[1][0])
    order_foods = OrderFoods.objects.filter(order_id__customer_id=Customer.objects.get(customer_email__iregex=f'{request.user}+@.+'),
                                            order_id__order_status = Order.STATUS[1][0]                                         
                                            ).select_related('order_id','food_id')

    if len(order)>0:
        context = {
            'order_id': order,
            'order_foods':order_foods,

        }
    else:
        context = {
            'order_foods':order_foods,
            'order_id' : None
        }
    return render(request, 'cafe_order/customer_confirmed_orders.html',context=context)


# This view lists the previous orders' informations of customer
@login_required(login_url='cafe_order:login')
def list_confirmed_orders(request):
    orders = Order.objects.filter(customer_id__customer_email__iregex=f'{request.user}+@.+')\
    .exclude(order_status__in = [Order.STATUS[0][0],Order.STATUS[1][0]])\
    .values('orderfoods__order_id')\
    .annotate(total_foods=Count('orderfoods__food_id__food_name'), price=Sum('orderfoods__food_id__food_price')) \
    .values() \
    .order_by('order_recieved_date')
    if orders:
        order_dict = {}
        for x in orders:

            order_dict[x['id']]={
                'order_recieved_date':x['order_recieved_date'],
                'order_status': x['order_status'],
                'total_foods': x['total_foods'],
                'price': x['price']
            }
    else:
        order_dict = {}
    
    context = {
        'order_dict': order_dict
    }
    return render(request, 'cafe_order/customer_previous_orders.html',context)


