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
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-users/', views.admin_users, name='admin_users'),
    path("admin-orders/", views.admin_orders, name="admin_orders"),
    path("admin-products/", views.admin_products, name="admin_products"),
    path("admin-orders/update/<int:order_id>/", views.update_order_status, name="update_order_status"),





    path('product/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path("admin-users/block/<int:user_id>/", views.block_user, name="block_user"),
    path("admin-users/unblock/<int:user_id>/", views.unblock_user, name="unblock_user"),
    path("admin-users/edit/<int:user_id>/", views.edit_user, name="edit_user"),
    path("admin-users/delete/<int:user_id>/", views.delete_user, name="delete_user"),

    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("forgot-password/sent/", views.forgot_password_sent, name="forgot_password_sent"),
    path('admin-stocks/', views.admin_stocks, name="admin_stocks"),
    path('admin-dashbord/banners/', views.admin_banners, name='admin_banners'),
    path('admin-add-banner/', views.add_banner, name='add_banner'),
    path('admin-delete-banner/<int:id>/', views.delete_banner, name='delete_banner'),


   path('product/toggle-home/<int:pk>/', views.toggle_homepage_product, name='toggle_homepage_product'),




    


    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('category/', views.category_list, name='categories'),

    path('checkout/', views.checkout, name='checkout'),
    path('profile/',views.profile_view, name='profile'),
    path('profile/edit/',views.edit_profile, name='edit_profile'),
    path('orders/', views.order_history, name='order_history'),

    path('search/',views.search,name='search')




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)