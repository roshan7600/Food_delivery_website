from django.urls import path
from . import views
from .views import send_contact_email

urlpatterns = [
    # Home & Menu
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),

    # Authentication
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # Food Management
    path('addfood/', views.add_food, name='add_food'),

    # Cart Functionality
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),

    # Address & Payment
    path('address/', views.address_view, name='address'),
    path('save-address/', views.save_address, name='save_address'),
    path('dummy-payment/', views.dummy_payment, name='dummy_payment'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment/', views.payment_view, name='payment'),  # Optional

    # Orders
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-orders/', views.order_history, name='order_history'),
    path('order-history/', views.order_history, name='order_history'),

    path('order-success/', views.order_success, name='order_success'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('orders/confirm/<int:order_id>/', views.confirm_order, name='confirm_order'),

    # Admin
    path('admin/orders/', views.admin_orders, name='admin_orders'),
    path('admin/customers/', views.admin_customers, name='admin_customers'),
    path('admin/order/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
    path('admin/customers/<int:user_id>/orders/', views.admin_customer_orders, name='admin_customer_orders'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),

    # Search
    path('search/', views.search_view, name='search'),
    # email
    path('send-contact-email/', send_contact_email, name='send_contact_email'),
]
