from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from .models import FoodItem, Category, Cart, Order, OrderItem, Address
from django.contrib import admin


from django.views.decorators.csrf import csrf_exempt
import json
from django.core.mail import EmailMultiAlternatives
from .models import ContactMessage 

# ----------------- Public Views -------------------

def home(request):
    category_id = request.GET.get('category')
    query = request.GET.get('q', '').strip()
    items = FoodItem.objects.all()
    categories = Category.objects.all()
    if category_id:
        items = items.filter(category__id=category_id)
    if query:
        items = items.filter(name__icontains=query)
    return render(request, 'home.html', {
        'food_items': items,
        'categories': categories,
        'selected_category': category_id,
        'query': query,
    })

def menu(request):
    items = FoodItem.objects.all()
    return render(request, 'menu.html', {'items': items})

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    return render(request, 'register.html')

# def login_user(request):
#     if request.method == 'POST':
#         username = request.POST['username'].strip()
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid credentials.')
#     return render(request, 'login.html')



from django.contrib.auth.views import redirect_to_login

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # ✅ Redirect staff users to admin panel
            if user.is_staff:
                return redirect('/admin/')

            # ✅ Redirect normal users
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')



# ----------------- Food & Cart -------------------

@login_required
def add_food(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("You are not authorized.")
    categories = Category.objects.all()
    items = FoodItem.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        price = request.POST.get('price', '').strip()
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if not (name and price and category_id):
            messages.error(request, 'All required fields are necessary.')
            return redirect('add_food')

        try:
            price = float(price)
        except ValueError:
            messages.error(request, 'Invalid price format.')
            return redirect('add_food')

        category = get_object_or_404(Category, id=category_id)
        FoodItem.objects.create(name=name, description=description, price=price, category=category, image=image)
        messages.success(request, 'Food item added successfully!')
        return redirect('add_food')

    return render(request, 'addfood.html', {'categories': categories, 'items': items})

@login_required
@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item, created = Cart.objects.get_or_create(user=request.user, food_item=item)
    cart_item.quantity = cart_item.quantity + quantity if not created else quantity
    cart_item.save()
    messages.success(request, f'{item.name} added to cart!')
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.food_item.price * item.quantity for item in cart_items)
    show_address_form = request.session.pop('show_address_form', False)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'show_address_form': show_address_form
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')

@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    messages.success(request, "All items removed from cart.")
    return redirect('view_cart')


@login_required
# @require_POST
def checkout(request):
    return redirect('address')

# ----------------- Address & Order -------------------



@login_required
def save_address(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if not name or not mobile or not address:
            messages.error(request, "Please fill all fields.")
            return redirect('checkout')

        request.session['delivery_address'] = {
            'name': name,
            'mobile': mobile,
            'address': address
        }

        request.session.modified = True
        messages.success(request, "Address saved. Proceed to payment.")
        return redirect('dummy_payment')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('checkout')



@login_required
def dummy_payment(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.food_item.price * item.quantity for item in cart_items)

    # ✅ Print to confirm address exists in session
    print(">>> Delivery Address in Session:", request.session.get('delivery_address'))

    return render(request, 'dummy_payment.html', {
        'total_amount': total,   
        'cart_items': cart_items  
    })



@login_required
def place_order(request):
    if request.method == 'POST':
        # ✅ Get address data from session
        address_data = request.session.get('delivery_address')
        if not address_data:
            messages.error(request, "Address not found.")
            return redirect('checkout')

        # ✅ Get user's cart items
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('view_cart')

        # ✅ Save address to database
        address = Address.objects.create(
            user=request.user,
            address_line=address_data['address'],
            phone=address_data['mobile'],
            city='N/A',
            pincode='000000'
        )

        # ✅ Calculate total price
        total_price = sum(item.food_item.price * item.quantity for item in cart_items)

        # ✅ Create the Order with name and mobile now added
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            address=address,
            name=address_data['name'],       
            mobile=address_data['mobile'],   
            status='Success'
        )

        # ✅ Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price
            )

        # ✅ Clear cart and session
        cart_items.delete()
        request.session.pop('delivery_address', None)

        # ✅ Show success message and render success page
        messages.success(request, 'Order placed successfully!')
        return render(request, 'order_success.html', {'order_id': order.id})

    # 🚫 Redirect non-POST requests to checkout
    return redirect('checkout')



@login_required
def order_success(request):
    return render(request, 'order_success.html')

# ----------------- Orders -------------------

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['Pending', 'Success']:
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled.")
    else:
        messages.error(request, "Only pending or successful orders can be cancelled.")
    return redirect('my_orders')

@login_required
@require_POST
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Success'
        order.save()
        messages.success(request, "Order confirmed successfully!")
    return redirect('my_orders')

# ----------------- Profile -------------------

@login_required
def profile(request):
    total_orders = Order.objects.filter(user=request.user).count()
    pending_orders = Order.objects.filter(user=request.user, status='Pending').count()
    delivered_orders = Order.objects.filter(user=request.user, status='Delivered').count()
    cancelled_orders = Order.objects.filter(user=request.user, status='Cancelled').count()
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'profile.html', {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'orders': recent_orders,
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name').strip()
        request.user.email = request.POST.get('email').strip()
        request.user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'update_profile.html')

# ----------------- Admin Views -------------------

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin_orders.html', {'orders': orders})

@login_required
@user_passes_test(lambda u: u.is_staff)
@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.save()
        messages.success(request, f"Order #{order.id} updated to {order.status}")
    else:
        messages.error(request, "Invalid status.")
    return redirect('admin_orders')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_customers(request):
    customers = User.objects.filter(is_staff=False)
    return render(request, 'admin_customers.html', {'customers': customers})

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_customer_orders(request, user_id):
    user = get_object_or_404(User, id=user_id)
    orders = Order.objects.filter(user=user)
    return render(request, 'admin_customer_orders.html', {'customer': user, 'orders': orders})

# ----------------- Search -------------------

def search_view(request):
    query = request.GET.get('q', '').strip()
    food_items = FoodItem.objects.filter(name__icontains=query) if query else []
    return render(request, 'search_results.html', {'food_items': food_items, 'query': query})



@login_required
def address_view(request):
    if request.method == 'POST':
        address_line = request.POST.get('address_line', '').strip()
        city = request.POST.get('city', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not address_line or not city or not pincode or not phone:
            messages.error(request, "Please fill all fields.")
            return redirect('address')

        Address.objects.create(
            user=request.user,
            address_line=address_line,
            city=city,
            pincode=pincode,
            phone=phone
        )

        if 'save_only' in request.POST:
            messages.success(request, "Address saved successfully.")
            return redirect('address')

        elif 'proceed' in request.POST:
            messages.success(request, "Address saved. Proceed to payment.")
            return redirect('payment')

    return render(request, 'address.html')



@login_required
def payment_view(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)
        if cart_items.exists():
            total_price = sum(item.food_item.price * item.quantity for item in cart_items)
            order = Order.objects.create(user=request.user, total_price=total_price, status='Success')
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    food_item=item.food_item,
                    quantity=item.quantity,
                    price=item.food_item.price
                )
            Cart.objects.filter(user=request.user).delete()
        messages.success(request, "Order placed successfully!")
        return redirect('order_success')
    return render(request, 'payment.html')



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'address', 'name')



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


# real time message in gmail


@csrf_exempt
def send_contact_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            # ✅ Save to database
            ContactMessage.objects.create(name=name, email=email, message=message)

            # ✅ Send HTML email to admin
            subject = 'New Contact Message from ClickToEat'
            text_content = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
            html_content = f"""
                <h2>New Contact Message</h2>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Email:</strong> {email}</p>
                <p><strong>Message:</strong><br>{message}</p>
            """
            email_message = EmailMultiAlternatives(
                subject, text_content,
                from_email='your_django_email@gmail.com',
                to=['roshanpatel31296@gmail.com']
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()

            # ✅ Send auto-reply to sender
            reply_subject = "Thanks for contacting ClickToEat"
            reply_text = (
                f"Hi {name},\n\nThanks for contacting ClickToEat! "
                f"We’ve received your message and will get back to you soon.\n\n"
                f"Your Message:\n{message}"
            )
            reply_html = f"""
                <p>Hi {name},</p>
                <p>Thanks for contacting <strong>ClickToEat</strong>! We’ve received your message and will get back to you soon.</p>
                <p><strong>Your Message:</strong></p>
                <p>{message}</p>
                <br>
                <p>Best regards,<br>ClickToEat Team</p>
            """
            reply_email = EmailMultiAlternatives(
                reply_subject, reply_text,
                from_email='your_django_email@gmail.com',
                to=[email]
            )
            reply_email.attach_alternative(reply_html, "text/html")
            reply_email.send()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})

    return JsonResponse({'status': 'failed', 'error': 'Invalid request'})




