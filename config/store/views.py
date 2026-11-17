from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import WatchForm, Watch
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Watch, Order, OrderItem
from django.db import transaction
from .forms import CheckoutForm, OrderTrackingForm
from django.utils import timezone




def home(request):
    featured_watches = Watch.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('-created_at')[:4]

    return render(request, 'store/home.html', {
        'featured_watches': featured_watches
    })

# Display active watches with product search and sorting options
def shop(request):
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'newest')

    watches = Watch.objects.filter(is_active=True)

    # Search watches by name, category or description
  # Display active watches and allow customers to search products
def shop(request):
    search_query = request.GET.get('q', '').strip()

    watches = Watch.objects.filter(is_active=True)

    if search_query:
        watches = watches.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    watches = watches.order_by('-created_at')

    return render(request, 'store/shop.html', {
        'watches': watches,
        'search_query': search_query,
    })



def product_details(request):
    return render(request, 'store/product_details.html')



# Display the admin dashboard with live inventory statistics
def admin_dashboard(request):

    total_products = Watch.objects.count()

    active_products = Watch.objects.filter(
        is_active=True
    ).count()

    low_stock = Watch.objects.filter(
        stock__lte=5,
        is_active=True
    ).count()

    total_units = sum(
        Watch.objects.values_list('stock', flat=True)
    )


    return render(request, 'store/dashboard/dashboard.html', {
        'total_products': total_products,
        'active_products': active_products,
        'low_stock': low_stock,
        'total_units': total_units,
    })



def admin_products(request):
    watches = Watch.objects.all().order_by('-created_at')

    return render(request, 'store/dashboard/products.html', {
        'watches': watches
    })


def add_watch(request):

    if request.method == 'POST':
        form = WatchForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('admin_products')

    else:
        form = WatchForm()

    return render(request, 'store/dashboard/add_watch.html', {
        'form': form
    })

def product_details(request, watch_id):
    watch = get_object_or_404(
        Watch,
        id=watch_id,
        is_active=True
    )

    return render(request, 'store/product_details.html', {
        'watch': watch
    })

def edit_watch(request, watch_id):
    watch = get_object_or_404(Watch, id=watch_id)

    if request.method == 'POST':
        form = WatchForm(
            request.POST,
            request.FILES,
            instance=watch
        )

        if form.is_valid():
            form.save()
            return redirect('admin_products')

    else:
        form = WatchForm(instance=watch)

    return render(request, 'store/dashboard/edit_watch.html', {
        'form': form,
        'watch': watch
    })

def delete_watch(request, watch_id):
    watch = get_object_or_404(Watch, id=watch_id)

    if request.method == 'POST':
        watch.delete()
        return redirect('admin_products')

    return render(request, 'store/dashboard/delete_watch.html', {
        'watch': watch
    })


# Add a selected watch to the customer's shopping cart
@require_POST
def add_to_cart(request, watch_id):
    watch = get_object_or_404(
        Watch,
        id=watch_id,
        is_active=True
    )

    cart = request.session.get('cart', {})

    watch_id = str(watch.id)

    if watch_id in cart:
        cart[watch_id] += 1
    else:
        cart[watch_id] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# Display the customer's shopping cart and calculate its total
def cart(request):
    cart_items = request.session.get('cart', {})

    watches = Watch.objects.filter(
        id__in=cart_items.keys(),
        is_active=True
    )

    items = []
    total = 0

    for watch in watches:
        quantity = cart_items.get(str(watch.id), 0)
        subtotal = watch.price * quantity

        items.append({
            'watch': watch,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total,
    })


# Update the quantity of a watch in the customer's shopping cart
@require_POST
def update_cart(request, watch_id):
    watch = get_object_or_404(
        Watch,
        id=watch_id,
        is_active=True
    )

    cart = request.session.get('cart', {})
    watch_id = str(watch.id)

    if watch_id in cart:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            return redirect('cart')

        if 1 <= quantity <= watch.stock:
            cart[watch_id] = quantity
            request.session['cart'] = cart
            request.session.modified = True

    return redirect('cart')


# Remove a selected watch from the customer's shopping cart
@require_POST
def remove_from_cart(request, watch_id):
    cart = request.session.get('cart', {})

    watch_id = str(watch_id)

    if watch_id in cart:
        del cart[watch_id]

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


# Display all customer orders in the admin dashboard
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'store/dashboard/orders.html', {
        'orders': orders
    })

# Display the details of a selected customer order
def admin_order_details(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id
    )

    order_items = order.items.select_related('watch').all()

    return render(request, 'store/dashboard/order_details.html', {
        'order': order,
        'order_items': order_items,
    })

# Update the status of a customer order
@require_POST
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    new_status = request.POST.get('order_status')

    valid_statuses = [
        status[0] for status in Order.ORDER_STATUS
    ]

    if new_status in valid_statuses:
        order.order_status = new_status
        order.save()

    return redirect('admin_order_details', order_id=order.id)

# Display the checkout page and create a customer order after form submission

# Display the checkout page, calculate the order summary, and create a customer order
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    watches = Watch.objects.filter(
        id__in=cart.keys(),
        is_active=True
    )

    items = []
    total = 0

    for watch in watches:
        quantity = cart.get(str(watch.id), 0)
        subtotal = watch.price * quantity

        items.append({
            'watch': watch,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        total += subtotal

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                order.order_number = (
                    f"TL-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                )
                order.total_amount = total
                order.save()

                for item in items:
                    watch = Watch.objects.select_for_update().get(
                        id=item['watch'].id,
                        is_active=True
                    )

                    quantity = item['quantity']

                    if quantity > watch.stock:
                        raise ValueError(
                            f"Insufficient stock for {watch.name}"
                        )

                    OrderItem.objects.create(
                        order=order,
                        watch=watch,
                        quantity=quantity,
                        price=watch.price
                    )

                    watch.stock -= quantity
                    watch.save()

            request.session['cart'] = {}
            request.session.modified = True

            return redirect('order_success', order_id=order.id)

    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form,
        'items': items,
        'total': total,
    })

# Display confirmation details after a customer successfully places an order
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'store/order_success.html', {
        'order': order,
    })


# Verify customer details and display the progress of their order


# Display the customer order tracking search form
def track_order(request):
    form = OrderTrackingForm()
    return render(request, 'store/track_order.html', {
        'form': form,
    })


# Verify customer details and display their orders on a separate results page

# Verify customer details and display their orders with order statistics
@require_POST
def track_order_results(request):
    form = OrderTrackingForm(request.POST)

    if form.is_valid():
        customer_name = form.cleaned_data['customer_name'].strip()
        customer_phone = form.cleaned_data['customer_phone'].strip()

        orders = Order.objects.filter(
            customer_name__iexact=customer_name,
            customer_phone=customer_phone
        ).order_by('-created_at')

        # Calculate the customer's order statistics
        total_orders = orders.count()

        active_orders = orders.exclude(
            order_status__in=['delivered', 'cancelled']
        ).count()

        delivered_orders = orders.filter(
            order_status='delivered'
        ).count()

        return render(request, 'store/track_order_results.html', {
            'orders': orders,
            'customer_name': customer_name,
            'total_orders': total_orders,
            'active_orders': active_orders,
            'delivered_orders': delivered_orders,
        })

    return render(request, 'store/track_order.html', {
        'form': form,
    })

# Display the About Us page with information about TimeLux Watches
def about(request):
    return render(request, 'store/about.html')

# Display the TimeLux Watches contact page
def contact(request):
    return render(request, 'store/contact.html')