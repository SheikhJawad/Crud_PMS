
from django.shortcuts import render ,redirect,get_object_or_404,HttpResponse
from django.contrib import messages
from .models import Customer,Product,Order
from django.db.models import Sum, F, FloatField



def dashboard(request):
  
    # products = Product.objects.all()  # Query all products
    # return render(request, 'accounts/dashboard.html', {'products': products})
    orders = Order.objects.all()

   
    total_orders = orders.count()
    pending_orders = orders.filter(status='PENDING').count()
    delivered_orders = orders.filter(status='DELIVERED').count()
    cancelled_orders = Order.objects.filter(status='CANCELLED').count()  

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders, 
        'orders': orders
    }
    return render(request, 'accounts/dashboard.html', context)



def customers(request):
    
    customers = Customer.objects.all()
    return render(request, 'accounts/customer.html', {'customers': customers})
 

def customer_update(request, customer_id=None):
    if customer_id:
        customer = get_object_or_404(Customer, id=customer_id)
    else:
        customer = None

    if request.method == 'POST':
        if customer:
            customer.first_name = request.POST.get('first_name')
            customer.last_name = request.POST.get('last_name')
            customer.email = request.POST.get('email')
            customer.password = request.POST.get('password')
            customer.phone_number = request.POST.get('phone_number')
            customer.save()
            # messages.success(request, 'Customer has been updated successfully.')
            return  HttpResponse("Updated successfully")
            
        else:
            Customer.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                email=request.POST.get('email'),
                password=request.POST.get('password'),
                phone_number=request.POST.get('phone_number')
            )
            messages.success(request, 'Customer has been created successfully.')
        return redirect('customers')

    # return render(request, 'accounts/customer_form.html', {'customer': customer})
    return Httpresponse("updated succefully")

def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer has been deleted successfully.')
        return redirect('customers')
    return render(request, 'accounts/customer_confirm_delete.html', {'customer': customer})





def customer_update(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.first_name = request.POST.get('first_name')
        customer.last_name = request.POST.get('last_name')
        customer.email = request.POST.get('email')
        customer.password = request.POST.get('password')
        customer.phone_number = request.POST.get('phone_number')
        customer.save()
        return httpresponse( 'Customer has been updated successfully.')
        return redirect('customers')  
    return render(request, 'accounts/update_profile.html', {'customer': customer})

def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer has been deleted successfully.')
        return redirect('customers')  
    return render(request, 'accounts/customer_confirm_delete.html', {'customer': customer})

def user_profile_view(request):
    if request.method == 'POST':
   
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            phone_number=phone_number
        )
        customer.save()
        messages.success(request, 'Customer profile has been successfully created.')
        return redirect('user_profile_view')  

    return render(request, 'accounts/user_profile.html')

def place_order(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
        total_bill = float(request.POST.get('total_bill', 0.0))

        customer = get_object_or_404(Customer, id=customer_id)
        product = get_object_or_404(Product, id=product_id)

       
        order = Order(
            customer=customer,
            product=product,
            quantity=quantity,
            total_bill=total_bill
        )
        order.save()

        messages.success(request, 'Order placed successfully!')
        return redirect('order_list')

    customers = Customer.objects.all()
    products = Product.objects.all()
    return render(request, 'accounts/place_order.html', {'customers': customers, 'products': products})

def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, 'Order status updated successfully!')
        else:
            messages.error(request, 'Invalid status choice!')
        return redirect('dashboard') 
    return render(request, 'accounts/update_order.html', {'order': order})


def remove_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order removed successfully!')
        return redirect('order_list')  
    return render(request, 'accounts/remove_order.html', {'order': order})

def order_list(request):
    orders = Order.objects.all()
    return render(request, 'accounts/order_list.html', {'orders': orders})