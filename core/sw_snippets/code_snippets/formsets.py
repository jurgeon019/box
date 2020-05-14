from django.db import models 
from django.contrib.auth import get_user_model 


User = get_user_model()



class Item(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title 


class IntermediateItemFeature(models.Model):
    item = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, related_name='intermediate_features')
    name = models.CharField(max_length=255)
    value = models.TextField()

    def __str__(self):
        return self.name  


class ItemFeature(models.Model):
    item  = models.ForeignKey(Item, related_name='features', on_delete=models.SET_NULL, null=True,)
    name  = models.ForeignKey('ItemFeatureAttribute', related_name='features', on_delete=models.CASCADE)
    value = models.ForeignKey('ItemFeatureValue',     related_name='features', on_delete=models.CASCADE)
    # value = models.TextField()

    def __str__(self):
        return self.name  


class ItemFeatureAttribute(models.Model):
    name  = models.CharField(max_length=255)

    def __str__(self):
        return self.name  


class ItemFeatureValue(models.Model):
    value = models.TextField()

    def __str__(self):
        return self.value 










class Site(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name        


class UserProfile(models.Model):
    # user = models.OneToOneField(to=User,unique=True, on_delete=models.CASCADE)
    sites = models.ManyToManyField(Site,blank=True, related_name='user_profiles')

    def __str__(self):
        return self.name








from django.contrib import admin 
from .models import * 

class SiteAdmin(admin.ModelAdmin):
    pass 

class UserProfileAdmin(admin.ModelAdmin):
    filter_horizontal = [
        'sites',
    ]

from django.forms import ModelForm 
from django import forms 

class SiteForm(forms.ModelForm):
    user_profiles = forms.ModelMultipleChoiceField(
        label='Users granted access',
        queryset=UserProfile.objects.all(),
        required=False,
        help_text='Admin users (who can access everything) not listed separately',
        widget=admin.widgets.FilteredSelectMultiple('user profiles', False))

class SiteAdmin(admin.ModelAdmin):
    fields = ('user_profiles',)

    def save_model(self, request, obj, form, change):
        super(SiteAdmin, self).save_model(request, obj, form, change) 
        obj.user_profiles.clear()
        for user_profile in form.cleaned_data['user_profiles']:
             obj.user_profiles.add(user_profile)

    # def get_form(self, request, obj=None, **kwargs):
    #     if obj:
    #         result = [ o.pk for o in obj.user_profiles.all() ]
    #     else:
    #         result = []
    #     self.form.base_fields['user_profiles'].initial = result
    #     return super(SiteAdmin, self).get_form(request, obj, **kwargs)

    form = SiteForm 

class FeatureForm(forms.ModelForm):
    # user_profiles = forms.ModelMultipleChoiceField(
    #     label='Users granted access',
    #     queryset=UserProfile.objects.all(),
    #     required=False,
    #     help_text='Admin users (who can access everything) not listed separately',
    #     widget=admin.widgets.FilteredSelectMultiple('user profiles', False),
    # )
    title = forms.CharField()

class IntermediateItemFeatureInlineFormSet(forms.models.BaseInlineFormSet):
    model = IntermediateItemFeature

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        # if self.request.GET.get('something', None):
        if True:
            # self.can_delete = True
            # self.data = {
            #     'form-1-DELETE':'on',
            # }
            # self.data = {
            #     'form-TOTAL_FORMS': '3',
            #     'form-INITIAL_FORMS': '2',
            #     'form-MAX_NUM_FORMS': '',
            #     'form-0-name': 'Article #1',
            #     'form-0-value': '2008-05-10',
            #     'form-0-DELETE': 'on',
            #     'form-1-name': 'Article #2',
            #     'form-1-value': '2008-05-11',
            #     'form-1-DELETE': '',
            #     'form-2-name': '',
            #     'form-2-value': '',
            #     'form-2-DELETE': '',
            # }
            self.initial = [
                {
                    'name':'1',
                    'value':'1',
                },
                {
                    'name':'2',
                    'value':'2',
                },
            ]

class IntermediateItemFeatureForm(forms.ModelForm):
    delete = forms.BooleanField()
    class Meta:
        model = IntermediateItemFeature
        exclude = []

class IntermediateItemFeatureInline(admin.TabularInline):
    form = IntermediateItemFeatureForm
    formset = IntermediateItemFeatureInlineFormSet
    extra = 0 
    model = IntermediateItemFeature

    def get_formset(self, request, obj=None, *args, **kwargs):
        formset = super().get_formset(request, obj, *args, **kwargs)
        formset.request = request
        return formset

    def get_extra(self, request, obj=None, *args, **kwargs):
        extra = super().get_extra(request, obj, *args, **kwargs)
        something = request.GET.get('something', None)
        if something:
            extra = ...# figure out how much initial forms there are, from the request ...
        extra = 5
        return extra

class ItemFeatureInline(admin.TabularInline):
    extra = 0 
    model = ItemFeature

    autocomplete_fields = [
        'name',
        'value',
    ]
    # raw_id_fields = [
    #     'name',
    #     'value',
    # ]

class ItemAdmin(admin.ModelAdmin):
    inlines = [
        # IntermediateItemFeatureInline
        ItemFeatureInline
    ]

    def save_formset(self, request, form, formset, change):
        if formset.model == IntermediateItemFeature:
            instances = formset.save(commit=False)
            for instance in instances:
                print(instance)
        super().save_formset(request, form, formset, change)

class ItemFeatureAdmin(admin.ModelAdmin):
    pass 

class ItemFeatureValueAdmin(admin.ModelAdmin):
    search_fields = [
        'value',
    ]

class ItemFeatureAttributeAdmin(admin.ModelAdmin):
    search_fields = [
        'name',
    ]

class IntermediateItemFeatureAdmin(admin.ModelAdmin):
    pass 


# admin.site.register(Site, SiteAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemFeature, ItemFeatureAdmin)
admin.site.register(ItemFeatureValue, ItemFeatureValueAdmin)
admin.site.register(ItemFeatureAttribute, ItemFeatureAttributeAdmin)
admin.site.register(IntermediateItemFeature, IntermediateItemFeatureAdmin)

