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

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('login')

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found")
            return redirect('login')

        if profile.phone != phone:
            messages.error(request, "Invalid phone number")
            return redirect('login')

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

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already registered")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

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
# ADD TO CART (PRODUCTION SAFE)
# ==========================
def add_to_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', [])

        try:
            name = str(request.POST.get('name'))
            price = float(request.POST.get('price', 0))
            weight = float(request.POST.get('weight', 1))
            total = price * weight
        except Exception:
            return redirect('index')

        cart.append({
            'name': name,
            'price': price,
            'weight': weight,
            'total': total
        })

        request.session['cart'] = cart
        request.session.modified = True

        grand_total = sum(float(item['total']) for item in cart)

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
# CART (PRODUCTION SAFE)
# ==========================
def cart(request):
    try:
        cart = request.session.get('cart', [])
    except Exception:
        request.session['cart'] = []
        cart = []

    safe_cart = []
    grand_total = 0

    for item in cart:
        try:
            name = str(item.get('name', 'Item'))
            price = float(item.get('price', 0))
            weight = float(item.get('weight', 1))
            total = float(item.get('total', price * weight))

            safe_cart.append({
                'name': name,
                'price': price,
                'weight': weight,
                'total': total
            })

            grand_total += total

        except Exception:
            continue

    request.session['cart'] = safe_cart
    request.session.modified = True

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
        request.session.modified = True

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