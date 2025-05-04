from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.store, name="store"),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_signup, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('addProduct/', views.add_product, name='addProduct'),
    path('cart/', views.cart, name="cart"),
    path('order_history/', views.order_history, name="order_history"),
    path('main/', views.main, name="main"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('profile/', views.profile, name='profile'),
    path('editar-perfil/', views.edit_profile, name='edit_profile'),
    path('productHistory/', views.product_history, name='productHistory'),
    path('personalizacion/', views.personalizacion, name='personalizacion'),
    path('personalizaciones/', views.lista_personalizaciones, name='admin_personalizaciones'),
    path('personalizaciones/atender/<int:pk>/', views.atender_personalizacion, name='atender_personalizacion'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('product/<int:pk>/like/', views.like_product, name='like_product'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('gestion/orders/', views.admin_order_list, name='admin_order_list'),
    path('gestion/orders/<int:order_id>/update/', views.update_order_status, name='update_order_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)