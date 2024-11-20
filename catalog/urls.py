from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import categories, view_child_product
from .views import categories, view_parent_product


app_name = 'catalog'  # Define the app name for namespacing

urlpatterns = [
    path('', views.home, name='home'),  # Public home page
    path('profile/', views.profile, name='profile'),
    path('categories/', views.categories, name='categories'),
    path('create_parent_product/', views.create_parent_product, name='create_parent_product'),
    path('create_child_product/<int:parent_id>/', views.create_child_product, name='create_child_product'),
    path('parent_product/<int:product_id>/', view_parent_product, name='view_parent_product'),
    path('parent_product/<int:parent_id>/child_products/', view_child_product, name='view_child_product'),
    path('edit_parent_product/<int:product_id>/', views.edit_parent_product, name='edit_parent_product'),
    # path('edit_child_product/<int:product_id>/', views.edit_child_product, name='edit_child_product'),
    path('delete_parent_product/<int:product_id>/', views.delete_parent_product, name='delete_parent_product'),
    # path('delete_child_product/<int:product_id>/', views.delete_child_product, name='delete_child_product'),
    path('add_to_wishlist/<int:parent_id>/<int:child_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart/<int:parent_id>/<int:child_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_wishlist/<int:parent_id>/<int:child_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('remove_from_cart/<int:parent_id>/<int:child_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view_wishlist/',views.view_wishlist, name='view_wishlist'),
    path('view_add_to_cart/', views.view_add_to_cart, name='view_add_to_cart'),
    path('buy_now/<int:parent_id>/<int:child_id>/', views.buy_now, name='buy_now'),
    path('product_details/<int:parent_id>/<int:child_id>/', views.product_detail, name='product_detail'),
    path('confirm_purchase/<int:parent_id>/<int:child_id>/', views.confirm_purchase, name='confirm_purchase'),
    path('complete_purchase/<int:parent_id>/<int:child_id>/', views.complete_purchase, name='complete_purchase'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
