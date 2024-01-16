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

    # Initialize query parameters
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    products = Product.objects.all()

    # Handling favorite products for authenticated users
    if request.user.is_authenticated:
        # Annotate with favorite counts if the user is a superuser
        if request.user.is_superuser:
            products = products.annotate(favorites_count=Count('favorite'))
        # Get the list of favorite product IDs for the logged-in user
        favorite_ids = Favorite.objects.filter(
            user=request.user).values_list('product_id', flat=True)
    else:
        favorite_ids = []

    # Sorting functionality
    if request.GET:
        # Extract and process the sorting parameters
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

        # Search functionality
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

        # Handle empty search results
        if not products.exists():
            messages.warning(request, "Your search returned no results.")

    # Context for rendering the products template
    current_sorting = f'{sort}_{direction}'
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'favorite_ids': favorite_ids,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    is_favorite = False  # Initialize is_favorite
    favorites_count = 0  # Initialize favorites count

    # Check user is authenticated & if product is in their favorites
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(
            user=request.user, product=product).exists()

    # Superuser specific feature: count how many users favorited this product
    if request.user.is_superuser:
        favorites_count = Favorite.objects.filter(product=product).count()

    context = {
        'product': product,
        'is_favorite': is_favorite,
        'favorites_count': favorites_count,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """

    # Restrict access to superusers only
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry only store owners can add products to the store')
        return redirect(reverse('home'))

    # Handles form submission for adding a new product.
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Saves product, redirects to detail page on successful submission.
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Displays an error message if the form is invalid.
            messages.error(
                request,
                'Failed to add product. Please ensure the form is valid.')
    else:
        # Provides an empty form for adding a new product.
        form = ProductForm()

    # Renders the add product template with the form.
    template = 'products/add_product.html'
    context = {'form': form}

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    # Restricts the editing functionality to superusers.
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can edit products.')
        return redirect(reverse('home'))
    # Retrieves the product to edit or returns a 404 error if not found.
    product = get_object_or_404(Product, pk=product_id)

    # Handles form submission for editing the product.
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            # Saves changes to the product and redirects to its detail page.
            form.save()
            messages.success(request, f'Successfully updated {product.name}!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Displays an error message if the form is invalid.
            messages.error(
                request,
                'Failed to update product. Please ensure the form is valid.')
    else:
        # Fills the form with the existing product details for editing.
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    # Renders the edit product template with the form.
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Deleta a product from the store """

    # Restricts delete functionality to superusers.
    if not request.user.is_superuser:
        messages.error(request, 'Sorry only store owners can delete products.')
        return redirect(reverse('home'))

    # Retrieves the product to delete or returns a 404 error if not found.
    product = get_object_or_404(Product, pk=product_id)
    product.delete()    # Deletes the selected product.
    messages.success(request, f'Successfully deleted {product.name}')
    # Redirects to the products page after deletion.
    return redirect(reverse('products'))


@login_required
def add_to_favorites(request, product_id):
    """ Add a product to the user's favorites """

    product = get_object_or_404(Product, id=product_id)
    _, created = Favorite.objects.get_or_create(
        user=request.user, product=product)
    if created:
        messages.success(
            request, f'"{product.name}" has been added to your favorites!')
    else:
        messages.info(
            request, f'"{product.name}" is already in your favorites.')
    return redirect('product_detail', product_id=product_id)


@login_required
def remove_from_favorites(request, product_id):
    """ Remove a product from the user's favorites """

    product = get_object_or_404(Product, id=product_id)
    deleted, _ = Favorite.objects.filter(
        user=request.user, product=product).delete()

    if deleted:
        messages.success(
            request, f'"{product.name}" has been removed from your favorites.')
    else:
        messages.info(
            request, f'"{product.name}" was not found in your favorites.')
    return redirect('product_detail', product_id=product_id)


@login_required
def user_favorites(request):
    """ Display the user's favorite products """

    favorites = Favorite.objects.filter(user=request.user).values_list(
            'product', flat=True)
    favorite_products = Product.objects.filter(id__in=favorites)

    if request.user.is_superuser:
        favorite_products = favorite_products.annotate(favorites_count=Count('favorite'))

    if not favorite_products.exists():
        messages.info(request, "You haven't added any favorites yet.")

    context = {
        'products': favorite_products,
    }

    return render(request, 'products/products.html', context)
