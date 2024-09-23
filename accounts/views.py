from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from accounts.decorator import allowed_users, unauthenticated_user

from .models import *
from .forms import *
from .filters import OrderFilter

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.

#created
@unauthenticated_user
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    
    # else:
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, 'Account created for '+user)
            return redirect('login')

    context={'form':form}
    return render(request,'accounts/register.html',context)
    
@unauthenticated_user
def loginPage(request):
        # if request.user.is_authenticated:
        #     return redirect('home')
        # else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,"username or password is incoorect")
                return redirect('login')
        context={}
        return render(request,'accounts/login.html',context)

def logotUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
# @allowed_users(allowed_roles=['admin','staff'])
def home(request):
    # return HttpResponse('Home page')
    order=Order.objects.all()
    customer=Customer.objects.all()
    total_cus=customer.count()
    total_ord=order.count()
    delivered=order.filter(status="Delivered").count()
    pending=order.filter(status="Pending").count()
    context={
        'orders':order,
        'customers':customer,
        'total_cus':total_cus,
        'total_ord':total_ord,
        'delivered':delivered,
        'pending':pending
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
def products(request):
    # return HttpResponse('products page')
    products=Products.objects.all()
    return render(request,'accounts/products.html',{'pro':products})
def customers(request,pk):
    # return HttpResponse('customers page')
    customer=Customer.objects.get(id=pk)
    order=customer.order_set.all()
    total_order=order.count()
    myFilter=OrderFilter(request.GET,queryset=order)
    order=myFilter.qs

    context={
        
        'cus':customer,
        'ord':order,
        'total_order':total_order,
        'myFilter':myFilter,
    }
    return render(request,'accounts/customers.html',context)

# def createOrder(request):
@login_required(login_url='login')
def createOrder(request,pk): #2
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk)
    # form=OrderForm(initial={'customer':customer})
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    if request.method=='POST':
        print("printing post:",request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()

            return redirect('/')

    
    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def updateOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)

    order=Order.objects.get(id=pk)

    formset=OrderForm(instance=order)
    if request.method=='POST':
        formset=OrderForm(request.POST,instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/')


    context={'formset':formset}
    return render(request,'accounts/order_form.html',context)

@login_required(login_url='login')
def createCus(request):

    form=CustomerForm()
    if request.method=='POST':
        form=CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/customer_form.html',context)
@login_required(login_url='login')
def createPro(request):

    form=ProductForm()
    if request.method=='POST':
        form=ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/product_form.html',context)


@login_required(login_url='login')
def updateCus(request,pk):
    customer=Customer.objects.get(id=pk)
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers',pk=customer.pk)
        
    context={'form':form}
        

        
    return render(request,'accounts/customer_form.html',context)

@login_required(login_url='login')
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    # item=order.product.name
    if request.method=='POST':
        order.delete()
        return redirect('/')
    

    context={
        'item':order,
    }

    return render(request,'accounts/delete.html',context)


def userPage(request):
    context={}
    return render(request,'accounts/user.html',context)
