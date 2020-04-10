from .admin import * 

from box.apps.sw_shop.sw_customer.admin import (
    Customer, CustomerAdmin,
    CustomerGroup, CustomerGroupAdmin,
    Coupon, CouponAdmin,
    Subscriber, SubscriberAdmin,
)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(CustomerGroup, CustomerGroupAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(Customer, CustomerAdmin)
