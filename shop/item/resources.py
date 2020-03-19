from import_export.resources import ModelResource
from .models import Item 

from django.utils import timezone 



class ItemResource(ModelResource):

    class Meta:
        model = Item 
        exclude = [
            'id',
            'created',
            'updated',
            'order',

            'category',
        ]
        import_id_fields = [
            'slug',
        ]

    # def before_save_instance(self, instance, using_transactions, dry_run):
    #     print()
    #     print("1  ___ before_save_instance !!!!")
    #     # print(timezone.now())
    #     # print("instance:", instance)
    #     for i in dir(instance):
    #         print(i)
    #     print(type(instance))
    #     x = instance.description
    #     print(x)

    #     # print("using_transactions:", using_transactions)
    #     # print("dry_run:", dry_run)
    #     print()
    #     super().before_save_instance(instance, using_transactions, dry_run)

    # def after_save_instance(self, instance, using_transactions, dry_run):
    #     print()
    #     print("2  ___ after_save_instance !!!!")
    #     # print(timezone.now())
    #     # print("instance:", instance)
    #     # print("using_transactions:", using_transactions)
    #     print(dir(instance))
        
    #     print()
    #     super().after_save_instance(instance, using_transactions, dry_run)

    # def before_delete_instance(self, instance, dry_run):
    #     print()
    #     print("3  ___ before_delete_instance")
    #     print(timezone.now())
    #     print("instance:", instance)
    #     print("dry_run:", dry_run)
    #     print()
    #     super().before_delete_instance(instance, dry_run)

    # def after_delete_instance(self, instance, dry_run):
    #     print()
    #     print("4  ___ after_delete_instance")
    #     print(timezone.now())
    #     print("instance:", instance)
    #     print("dry_run:", dry_run)
    #     print()
    #     super().after_delete_instance(instance, dry_run)

    # def before_import(self, dataset, using_transactions, dry_run, **kwargs):
    #     print()
    #     print("5  ___ before_import")
    #     # print(timezone.now())
    #     # print("dataset:", dataset)
    #     print(dir(dataset))
    #     print(type(dataset))
    #     x = dataset.csv


    #     # print("using_transactions:", using_transactions)
    #     # print("dry_run:", dry_run)
    #     print()
    #     super().before_import(dataset, using_transactions, dry_run, **kwargs)

    # def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
    #     print()
    #     print("6  ___ after_import")
    #     print(timezone.now())
    #     print("dataset:", dataset)
    #     print("result:", result)
    #     print("using_transactions:", using_transactions)
    #     print("dry_run:", dry_run)
    #     print("kwargs:", kwargs)
    #     print()
    #     super().after_import(dataset, result, using_transactions, dry_run, **kwargs)

    def before_import_row(self, row, **kwargs):
        print()
        print("7  ___ before_import_row")
        print(timezone.now())
        print("row:", row)
        print("dir(row):", dir(row))
        print("type(row):", type(row))
        print("kwargs:", kwargs)
        print()
        # super().before_import_row(row, **kwargs)

    # def after_import_row(self, row, row_result, **kwargs):
    #     print()
    #     print("8  ___ after_import_row")
    #     print(timezone.now())
    #     print("row:", row)
    #     print(row_result)
    #     print("kwargs:", kwargs)
    #     print()
    #     super().after_import_row(row, row_result, **kwargs)

    # def after_import_instance(self, instance, new, **kwargs):
    #     print()
    #     print("9  ___ after_import_instance")
    #     print(timezone.now())
    #     print("instance:", instance)
    #     print("new:", new)
    #     print("kwargs:", kwargs)
    #     print()
    #     super().after_import_instance(instance, new, **kwargs)




    def before_export(self, queryset, *args, **kwargs):
        print()
        print("10  ___ before_export")
        print(timezone.now())
        print()
        super().before_export(queryset, *args, **kwargs)

    def after_export(self, queryset, data, *args, **kwargs):
        print()
        print("11  ___ after_export")
        print(timezone.now())
        print()
        super().after_export(queryset, data, *args, **kwargs)




    # Image
    # Review
    # Feature
    # Variant
    # Option

    # markers
    # similars
    # manufacturer
    # brand 
    # currency
    # in_stock
    def dehydrate_markers(self, item):
        markers = ''
        return markers

    def dehydrate_similars(self, item):
        similars = ''
        return similars

    def dehydrate_manufacturer(self, item):
        manufacturer = ''
        return manufacturer

    def dehydrate_brand(self, item):
        brand = ''
        return brand

    def dehydrate_currency(self, item):
        currency = ''
        return currency

    def dehydrate_in_stock(self, item):
        in_stock = ''
        return in_stock



