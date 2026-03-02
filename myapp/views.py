from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ContactMessage, Profile


# ==========================
# HOME
# ==========================
def index(request):
    return render(request, 'index.html')


# ==========================
# LOGIN (USERNAME + PHONE + PASSWORD)
# ==========================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        password = request.POST.get("password")

        # Step 1: Authenticate username + password
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('login')

        # Step 2: Check phone number
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found")
            return redirect('login')

        if profile.phone != phone:
            messages.error(request, "Invalid phone number")
            return redirect('login')

        # Step 3: Login success
        login(request, user)
        return redirect('index')

    return render(request, "login.html")


# ==========================
# LOGOUT
# ==========================
def logout_view(request):
    logout(request)
    return redirect('login')


# ==========================
# REGISTER
# ==========================
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password check
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        # Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        # Phone check (unique phone)
        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Create profile with phone
        Profile.objects.create(user=user, phone=phone)

        messages.success(request, "Registration successful. Please login.")
        return redirect('login')

    return render(request, 'register.html')


# ==========================
# PROFILE
# ==========================
@login_required
def profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})


# ==========================
# CATEGORY PAGES
# ==========================
def vegetables(request):
    return render(request, "vegetables.html")

def fruits(request):
    return render(request, "fruits.html")

def groceries(request):
    return render(request, "groceries.html")

def stationery(request):
    return render(request, "stationery.html")

def essentials(request):
    return render(request, "essentials.html")

def decor(request):
    return render(request, "decor.html")


# ==========================
# ADD TO CART
# ==========================
def add_to_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', [])

        name = request.POST.get('name')
        price = int(request.POST.get('price', 0))
        weight = float(request.POST.get('weight', 1))
        total = price * weight

        cart.append({
            'name': name,
            'price': price,
            'weight': weight,
            'total': total
        })

        request.session['cart'] = cart

        grand_total = sum(item['total'] for item in cart)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'message': f'{name} added to cart',
                'total_price': total,
                'grand_total': grand_total
            })

        messages.success(request, f"{name} added to cart")
        return redirect(request.META.get('HTTP_REFERER', 'index'))

    return redirect('index')


# ==========================
# CART
# ==========================
def cart(request):
    cart = request.session.get('cart', [])
    safe_cart = []

    for item in cart:
        price = int(item.get('price', 0))
        weight = float(item.get('weight', 1))
        total = item.get('total', price * weight)

        safe_cart.append({
            'name': item.get('name', 'Item'),
            'price': price,
            'weight': weight,
            'total': total
        })

    request.session['cart'] = safe_cart
    grand_total = sum(i['total'] for i in safe_cart)

    return render(request, 'cart.html', {
        'cart': safe_cart,
        'grand_total': grand_total
    })


# ==========================
# REMOVE FROM CART
# ==========================
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
        request.session['cart'] = cart
    return redirect('cart')


# ==========================
# CONTACT
# ==========================
def contact(request):
    if request.method == "POST":
        ContactMessage.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            message=request.POST.get('message')
        )
        messages.success(request, "Message sent successfully")
        return redirect('contact')

    return render(request, 'contact.html')
