from django.urls import path, include
from . import views

urlpatterns = [
    path('categories', views.CategoriesView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleItemView.as_view()),
    path('groups/manager/users', views.manager_users_view),
    path('groups/manager/users/<int:id>', views.manager_single_user_view),
    path('groups/delivery-crew/users', views.delivery_crew_users_view),
    path('groups/delivery-crew/users/<int:id>', views.delivery_crew_single_user_view),
    path('cart/menu-items', views.CartMenuItemsView.as_view()),
    path('orders', views.OrdersView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
]