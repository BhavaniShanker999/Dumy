from django.shortcuts import render,redirect
from django.forms import inlineformset_factory

from .forms import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .decorators import *
from django.contrib.auth.models import Group



@unaunthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			customer_model.objects.create(
                            user=user,
                            name=user.username,
                        )

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')

	context = {'form': form}
	return render(request, 'accounts/register.html', context)

@unaunthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
				login(request, user)
				return redirect('/')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer_model.order_model_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)

	context = {'orders': orders, 'total_orders': total_orders,
            'delivered': delivered, 'pending': pending}
	return render(request, 'accounts/user.html', context)




@login_required(login_url='login')
@admin_only
def home(request):
    customers_info=customer_model.objects.all()
    orders_info=order_model.objects.all()
    total_customers=customers_info.count()
    total_orders=orders_info.count()
    pending = orders_info.exclude(status='Delivered').count()
    delivered=orders_info.filter(status='Delivered').count()

    context={'customers_info':customers_info,'orders_info':orders_info,
             'total_customers': total_customers, 'total_orders': total_orders,
             'pending': pending, 'delivered': delivered}

    return render(request,'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products_info=Product_model.objects.all()
    context={'products_info':products_info}
    return render(request,'accounts/products.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,keyy):
    customer=customer_model.objects.get(id=keyy)
    orders=customer.order_model_set.all()
    orders_count=orders.count()
    myfilter=order_filter(request.GET,queryset=orders)
    orders=myfilter.qs
    context = {'customer': customer, 'orders': orders,
               'orders_count': orders_count,'myfilter':myfilter}
    return render(request,'accounts/customer.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, keyy):
    create_order_formset=inlineformset_factory(customer_model,order_model,fields=('products_mod','status'))
    customer_mod =customer_model.objects.get(id=keyy)
    formset = create_order_formset(instance=customer_mod)
    if request.method == 'POST':
        formset = create_order_formset(request.POST,instance=customer_mod)
        
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context={'formset':formset}
    return render(request,'accounts/create_order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_product(request):
    form=add_product_form()
    if request.method=='POST':
        form=add_product_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    context={'form':form}
    return render(request,'accounts/add_product.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request,pk):
    order=order_model.objects.get(id=pk)
    form=create_order_form(instance=order)
    if request.method == 'POST':
        form = create_order_form(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'accounts/update_order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request,pk):
    order=order_model.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
     
    context = {'order': order}
    return render(request,'accounts/delete_order.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer_model
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context = {'form': form}
	return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add_customer(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'accounts/add_customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_customer(request, pk):
    customer = customer_model.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/update_customer.html', context)
