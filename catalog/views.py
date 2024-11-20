from django.shortcuts import render, redirect, get_object_or_404
from .forms import ParentProductForm, ChildProductForm
from .models import ParentProduct, ChildProduct, AddToCart, WishList
from django.shortcuts import render, get_object_or_404, redirect
from .models import ChildProduct, WishList
from .forms import ChildProductForm
from .models import WishList, AddToCart
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'catalog/home.html')

def categories(request):
    parent_products = ParentProduct.objects.all()  # Get all parent products
    return render(request, 'catalog/categories.html', {'parent_products': parent_products}) 

def profile(request):
    user = request.user
    wishlist_items = WishList.objects.filter(user=user)
    addtocart_items = AddToCart.objects.filter(user=user) 
    
    return render(request, 'catalog/profile.html', {
        'wishlist_items': wishlist_items,
        'addtocart_items': addtocart_items,
    })
def create_parent_product(request):
    if request.method == 'POST':
        form = ParentProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog/profile.html')  # Correctly redirecting using the app namespace
    else:
        form = ParentProductForm()
    return render(request, 'catalog/create_parent_product.html', {'form': form})

def view_parent_product(request, product_id):
    parent_product = get_object_or_404(ParentProduct, id=product_id)  # Get the parent product
    child_products = ChildProduct.objects.filter(parent=parent_product)  # Get all child products for this parent

    return render(request, 'catalog/view_parent_product.html', {
        'parent_product': parent_product,
        'child_products': child_products,
    })


def create_child_product(request, parent_id):
    parent_product = get_object_or_404(ParentProduct, id=parent_id)  # Get the parent product
    if request.method == 'POST':
        form = ChildProductForm(request.POST, request.FILES)
        if form.is_valid():
            child_product = form.save(commit=False)
            child_product.parent = parent_product  # Link child product to the parent
            child_product.save()
            return redirect('catalog:view_child_product', parent_id=parent_product.id)  # Redirect to child product view
    else:
        form = ChildProductForm(initial={'parent': parent_product})
    return render(request, 'catalog/create_child_product.html', {
        'form': form,
        'parent_product': parent_product
    })

def view_child_product(request, parent_id):
    parent_product = get_object_or_404(ParentProduct, id=parent_id)
    child_products = ChildProduct.objects.filter(parent=parent_product)  # Get child products

    return render(request, 'catalog/view_child_product.html', {
        'parent_product': parent_product,
        'child_products': child_products,
    })

def edit_parent_product(request, product_id):
    parent_product = get_object_or_404(ParentProduct, id=product_id)
    if request.method == "POST":
        form = ParentProductForm(request.POST, request.FILES, instance=parent_product)
        if form.is_valid():
            form.save()
            return redirect('catalog:categories')  # Correctly redirecting using the app namespace
    else:
        form = ParentProductForm(instance=parent_product)
    return render(request, 'catalog/edit_product.html', {'form': form, 'product': parent_product, 'type': 'Parent'})

def delete_parent_product(request, product_id):
    parent_product = get_object_or_404(ParentProduct, id=product_id)
    if request.method == "POST":
        parent_product.delete()
        return redirect('catalog:categories')  # Correctly redirecting using the app namespace
    return render(request, 'catalog/delete_confirmation.html', {'product': parent_product, 'type': 'Parent'})

def add_to_wishlist(request, child_id, parent_id):
    child_product = get_object_or_404(ChildProduct, id=child_id)
    user = request.user
    print(parent_id)
    print(parent_id)
    cart_item, created = WishList.objects.get_or_create(
        user=user,
        child_product=child_product,
    )
    if created:
        messages.success(request, f"{child_product.title} has been added to your wishlist.")
    else:
        messages.info(request, f"{child_product.title} is already in your wishlist.")
    return redirect('catalog:view_parent_product', product_id=parent_id)


def view_wishlist(request):
    wishlist_items = WishList.objects.filter(user=request.user).select_related('child_product')
    user = request.user
    context = {
        'wishlist_items': wishlist_items,
        'user':user,
    }
    return render(request, 'catalog/wishlist.html', context)

def add_to_cart(request, child_id, parent_id): 
    child_product = get_object_or_404(ChildProduct, id=child_id)
    user = request.user
    print(parent_id)
    print(child_id)

    cart_item, created = AddToCart.objects.get_or_create(
        user=user,
        child_product=child_product,
    )
    if created:
        messages.success(request, f'{child_product.title} has been added to your cart!')
    else:
        messages.info(request, f'{child_product.title} is already in your cart.')
    return redirect('catalog:view_parent_product', product_id=parent_id)

def view_add_to_cart(request):
    add_to_cart_items = AddToCart.objects.filter(user=request.user).select_related('child_product')
    user = request.user
    context = {
        'add_to_cart_items': add_to_cart_items,
        'user': user,
    }
    return render(request, 'catalog/add_to_cart.html', context)


def remove_from_wishlist(request, parent_id, child_id):
    wishlist_items = WishList.objects.filter(child_product__parent__id=parent_id, child_product__id=child_id)
    if wishlist_items.exists():
        wishlist_items.delete()
    return redirect('catalog:view_wishlist')


def remove_from_cart(request, parent_id, child_id):
    cart_items = AddToCart.objects.filter(child_product__parent__id=parent_id, child_product__id=child_id)
    if cart_items.exists():
        cart_items.delete()
    return redirect('catalog:view_add_to_cart')


def product_detail(request, parent_id, child_id):
    product = get_object_or_404(ChildProduct, parent_id=parent_id, id=child_id)
    context = {
        'product': product,
        'parent_id': parent_id,
        'child_id': child_id,
    }
    return render(request, 'catalog/product_detail.html', context)

def buy_now(request, parent_id, child_id):
    child_product = get_object_or_404(ChildProduct, id=child_id, parent_id=parent_id)
    return render(request, 'catalog/buy_now.html', {'child_product': child_product})

def confirm_purchase(request, parent_id, child_id):
    try:
        parent_product = ParentProduct.objects.get(id=parent_id)
        child_product = ChildProduct.objects.get(id=child_id, parent=parent_product)
    except (ParentProduct.DoesNotExist, ChildProduct.DoesNotExist):
        return redirect('catalog:categories') 
    context = {
        'parent_product': parent_product,
        'child_product': child_product,
    }
    return render(request, 'catalog/confirm_purchase.html', context)

def complete_purchase(request, parent_id, child_id):
    parent_product = get_object_or_404(ParentProduct, pk=parent_id)
    child_product = get_object_or_404(ChildProduct, pk=child_id)
    return render(request, 'catalog/purchase_success.html', {'parent_product': parent_product, 'child_product': child_product})