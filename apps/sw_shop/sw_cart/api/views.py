from .serializers import * 
from rest_framework import viewsets 
from box.apps.sw_shop.sw_cart.utils import get_cart 


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    def get_queryset(self):
        request = self.request 
        cart = get_cart(request)
        print(cart.id)
        return CartItem.objects.all()#.filter(cart=cart)

    def create(self, request, *args, **kwargs):
        cart_item = self.get_object()
        quantity  = request.query_params 
        print(quantity)
        cart = get_cart(request)
        cart.add_item(cart_item.id)
        return super().create(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     print(request)
    #     print(*args)
    #     # print(**kwargs)
    #     return super().delete(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        print(request)
        print(dir(self))
        cart_item = self.get_object()
        print(cart_item)
        print(*args)
        # print(**kwargs)
        return super().update(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     print(request)
    #     print(*args)
    #     # print(**kwargs)
    #     return super().retrieve(request, *args, **kwargs)

