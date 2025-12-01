from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='products'),
    path('products/<int:product_id>/', views.products_detail,name='product_detail'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='cart_add'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='cart_decrease'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='cart_remove'),
    


    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('category/', views.category_list, name='categories'),

    path('checkout/', views.checkout, name='checkout'),
    path('profile/',views.profile_view, name='profile'),
    path('profile/edit/',views.edit_profile, name='edit_profile'),







]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)