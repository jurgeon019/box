from .admin import * 

from box.sw_shop.customer.admin import (
    Customer, CustomerAdmin,
)
admin.site.register(Customer, CustomerAdmin)

