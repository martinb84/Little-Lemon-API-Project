from rest_framework import generics
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import UserSerializer, CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import status
from decimal import Decimal
from django.http import Http404

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    #Any user can add a new category so add code below
    '''
    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    '''

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'title']
    filterset_fields = ['category', 'price']
    search_fields = ['title']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
class SingleItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method != 'GET':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def manager_users_view(request):
    try:
        manager_group = Group.objects.get(name="Manager")
    except Group.DoesNotExist:
        return Response({"message": "Manager group does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        managers = manager_group.user_set.all()
        serializer = UserSerializer(managers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        username = request.data.get('username')
        if not username:
            return Response({"message": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        manager_group.user_set.add(user)
        return Response({"message": "User added to managers group."}, status=status.HTTP_201_CREATED)
        
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def manager_single_user_view(request, id):
    if id:
        user = get_object_or_404(User, id=id)
        managers = Group.objects.get(name="Manager")
        if request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "200-Success"}, 200)
    
    return Response({"message": "User ID is required"}, status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def delivery_crew_users_view(request):
    try:
        delivery_crew_group = Group.objects.get(name="Delivery crew")
    except Group.DoesNotExist:
        return Response({"message": "Delivery crew group does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        delivery_crew = delivery_crew_group.user_set.all()
        serializer = UserSerializer(delivery_crew, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        username = request.data.get('username')
        if not username:
            return Response({"message": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, username=username)
        delivery_crew_group.user_set.add(user)
        return Response({"message": "201-Created"}, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delivery_crew_single_user_view(request, id):
    if id:
        user = get_object_or_404(User, id=id)
        delivery_crew = Group.objects.get(name="Delivery crew")
        if request.method == 'DELETE':
            delivery_crew.user_set.remove(user)
        return Response({"message": "200-Success"}, 200)
    
    return Response({"message": "User ID required."}, status.HTTP_404_NOT_FOUND)
    
class CartMenuItemsView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Implement logic to list cart items
        queryset = Cart.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Implement logic to add item to cart
        menuitem_id = request.data.get('menuitem')
        menuitem = MenuItem.objects.get(id=menuitem_id)
        price = menuitem.price
        quantity = int(request.data.get('quantity'))
        total_price = price * quantity
        data = {'user': request.user.id, 'menuitem': menuitem_id, 'quantity': quantity, 'unit_price': price, 'price': total_price}
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # Implement logic to flush cart
        Cart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_200_OK)    
    
class OrdersView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    ordering_fields = ['date', 'status']
    filterset_fields = ['date', 'status']
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        
        elif user.groups.filter(name='Delivery crew').exists():
            return Order.objects.filter(delivery_crew=user)
            
        return Order.objects.filter(user=user)
    
    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        print(self.request.data)
        order = serializer.save(user=self.request.user, total=total)

        for cart_item in cart_items:
            OrderItem.objects.create(menuitem=cart_item.menuitem, quantity=cart_item.quantity,
                                     unit_price=cart_item.unit_price, price=cart_item.price, order=order)
            cart_item.delete()

    def calculate_total(self, cart_items):
        total = Decimal(0)
        for cart_item in cart_items:
            total += cart_item.price
        return total
    
class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if instance.user == request.user or user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        
        else:
            return Response({"error": "This order does not belong to the current user."}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        user = self.request.user
        
        if user.groups.filter(name='Manager').exists():
            if 'delivery_crew' in data:
                try:
                    delivery_crew = User.objects.get(username=data['delivery_crew'])
                except User.DoesNotExist:
                    return Response({"error": "Delivery crew not found."}, status=status.HTTP_400_BAD_REQUEST)
                
                delivery_crew_group = Group.objects.get(name='Delivery crew')
                if delivery_crew not in delivery_crew_group.user_set.all():
                    return Response({"error": "User is not a member of the Delivery crew group."}, status=status.HTTP_400_BAD_REQUEST)
                
                # Assign the delivery crew to the order
                instance.delivery_crew = delivery_crew
            if 'status' in data:
                instance.status = data['status']
            instance.save()
        elif user.groups.filter(name='Delivery crew').exists():
            if 'status' in data:
                instance.status = data['status']
                instance.save()
            else:
                return Response({"error": "Delivery crew can only update the status."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"error": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        if user.group.filter(name='Manager').exists():
            self.perform_destroy(instance)
            return Response(status=status.HTTP_200_OK)
        else:    
            return Response({"error": "You do not have permission to delete this order."}, status=status.HTTP_403_FORBIDDEN)