from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Favorite
from .forms import FavoriteForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.db.models.functions import Lower
from django.urls import reverse
from django.http import JsonResponse

from .models import Product, Category, Favorite
from .forms import ProductForm


def all_products(request):
    """ A view to show all products """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        
        # Check if products queryset is empty
        if not products.exists():
            messages.warning(request, "Your search returned no results.")

    current_sorting = f'{sort}_{direction}'

    # Initialize an empty list for favorite product IDs
    favorite_ids = []

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the list of favorite product IDs for the logged-in user
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    
    if request.user.is_superuser:
        products_with_favorites = Product.objects.annotate(favorites_count=Count('favorite'))
    
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'favorite_ids': favorite_ids,
        'products': products_with_favorites,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    # Initialize is_favorite as False
    is_favorite = False

    # Check if the user is authenticated and if the product is in their favorites
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'is_favorite': is_favorite,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can add products to the store')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can edit products.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated {product.name}!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Deleta a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can delete products.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'Successfully deleted {product.name}')
    return redirect(reverse('products'))


@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    _, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, f'"{product.name}" has been added to your favorites!')
    else:
        messages.info(request, f'"{product.name}" is already in your favorites.')
    return redirect('product_detail', product_id=product_id)


@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    deleted, _ = Favorite.objects.filter(user=request.user, product=product).delete()
    if deleted:
        messages.success(request, f'"{product.name}" has been removed from your favorites.')
    else:
        messages.info(request, f'"{product.name}" was not found in your favorites.')
    return redirect('product_detail', product_id=product_id)


@login_required
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).values_list('product', flat=True)
    favorite_products = Product.objects.filter(id__in=favorites)

    if not favorite_products.exists():
        messages.info(request, "You haven't added any favorites yet.")

    context = {
        'products': favorite_products,
    }

    return render(request, 'products/products.html', context)