from django.shortcuts import render, get_object_or_404,redirect
from .models import Product
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Product, CartItem,Category,Order,Banner
from django.contrib.auth.decorators import login_required


def home(request):
    watch = Product.objects.get(id=4)
    airpods = Product.objects.get(id=9)
    banners = Banner.objects.all()
    categories = Category.objects.all()
    home_products = Product.objects.filter(show_on_homepage=True)

    return render(request, 'home.html', {
        'watch': watch,
        'airpods': airpods,
        'banners': banners,
        'categories': categories,
        'products': home_products,
    })


    

def search(request):
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})



def product_list(request):
    category_id = request.GET.get('category')

    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    return render(request, 'product_list.html', {'products': products})




def category_list(request):
    category = Category.objects.all()
    return render(request, 'category.html', {'categories': category})




def products_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products_details.html', {'product': product})




def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')  # redirect to login

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(item.total_price() for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        address = request.POST['address']

        # 1️⃣ Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total
        )

        # 2️⃣ Create order items
        for item in cart_items:
            order.items.create(
                product_name=item.product.name,
                quantity=item.quantity,
                price=item.product.price
            )

        # 3️⃣ Clear cart
        cart_items.delete()

        messages.success(request, "Order placed successfully! 🎉")
        return redirect('order_history')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total,
    })


@login_required
def profile_view(request):
    if request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    return render(request, 'profile.html')


@login_required
def edit_profile(request):
    user = request.user

    # Create profile if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = request.FILES.get('profile_image')

        user.username = username
        user.email = email
        user.save()

        if image:
            profile.profile_image = image
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    return render(request, 'edit_profile.html', {"user": user, "profile": profile})




def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})




def admin_dashboard(request):
    users = User.objects.count()
    products = Product.objects.count()
    orders = Order.objects.count()
    banners = Banner.objects.count()
    banners_list = Banner.objects.all()

    return render(request, 'admin_dashboard.html', {
        'users': users,
        'products': products,
        'orders': orders,
        'banners': banners,
        'banners_list': banners_list
    })


@login_required
def admin_users(request):
    if not request.user.is_staff:
        return redirect('profile')

    # Only normal users (non-admin)
    users = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')

    return render(request, 'users.html', {'users': users})
@login_required
def admin_orders(request):
    if not request.user.is_staff:
        return redirect("profile")

    orders = Order.objects.all().order_by("-created_at")

    return render(request, "orders.html", {"orders": orders})
def admin_products(request):
    if not request.user.is_staff:
        return redirect('home')

    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_products')

    else:
        form = ProductForm()

    return render(request, 'products_admin.html', {
        'products': products,
        'form': form,
        'categories': categories
    })


@login_required
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return redirect("profile")

    order = Order.objects.get(id=order_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        order.status = new_status
        order.save()
        return redirect("admin_orders")

    return render(request, "update_order_status.html", {"order": order})



from .forms import ProductForm





def edit_product(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == "POST":
        product.name = request.POST.get("name")
        product.price = request.POST.get("price")
        product.description = request.POST.get("description")
        product.category_id = request.POST.get("category")
        product.stock = request.POST.get("stock")

        if request.FILES.get("image"):
            product.image = request.FILES["image"]

        product.save()
        return redirect("admin_products")

    return redirect("admin_products")




@login_required
def delete_product(request, id):
    if not request.user.is_staff:
        return redirect('home')

    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('admin_dashboard')

def block_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('admin_users')

def unblock_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('admin_users')

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_users')

def edit_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.save()
        return redirect('admin_users')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # You can add check if email exists here
        return redirect("forgot_password_sent")

    return render(request, "forgot_password.html")

def forgot_password_sent(request):
    return render(request, "password_sent.html")
def admin_stocks(request):
    products = Product.objects.all()
    return render(request, "admin_stocks.html", {"products": products})



def admin_banners(request):
    banners = Banner.objects.all()
    banner_count = banners.count()

    return render(request, 'banner_update.html', {
        'banners': banners,
        'banner_count': banner_count
    })


def add_banner(request):
    if request.method == "POST":
        image = request.FILES.get('image')
        if image:
            Banner.objects.create(image=image)
        return redirect('admin_banners')


def delete_banner(request, id):
    banner = Banner.objects.get(id=id)
    banner.delete()
    return redirect('admin_banners')

def toggle_homepage_product(request, pk):
    product = Product.objects.get(id=pk)
    product.show_on_homepage = not product.show_on_homepage
    product.save()
    return redirect('admin_products')
