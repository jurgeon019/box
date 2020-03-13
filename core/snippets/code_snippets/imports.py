

from django import forms
from django.db import models

# https://docs.djangoproject.com/en/2.1/ref/models/database-functions/
from django.db.models import Q, F, Count, CharField, FloatField, DateTimeField Sum, Value, ExpressionWrapper
from django.db.models.functions import Lower, Greatest, Extract, Cast, Coalesce, Now, Trunc, Repeat,Length, Upper

# https://docs.djangoproject.com/en/2.1/ref/applications/#django.apps.AppConfig
from django.apps import AppCongifg

# https://docs.djangoproject.com/en/2.1/ref/urls
from django.urls import path, include, re_path, register_converter, reverse_lazy

# https://docs.djangoproject.com/en/2.1/ref/urls/#module-django.conf.urls
from django.conf.urls import static, url, handler400, handler403, handler404, handler500

# https://docs.djangoproject.com/en/2.1/topics/settings/
from django.conf import settings

# https://docs.djangoproject.com/en/2.1/topics/http/shortcuts/
from django.shortcuts import reverse, redirect, render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse

# https://docs.djangoproject.com/en/2.1/topics/signals/
from django.db.models.signals import (
  post_save, pre_save, post_delete, pre_delete,
  
)
from django.dispatch import receiver

# https://docs.djangoproject.com/en/2.1/ref/utils/
from django.utils import cache, dateparse, decorators, encoding, feedgenerator, functional, html, http, module_loading, safestring, text, timezone, translation
from django.utils.text import slugify, format_lazy

# https://docs.djangoproject.com/en/2.1/topics/pagination/
from django.core.paginator import Paginator

# https://docs.djangoproject.com/en/2.1/ref/exceptions/
from django.core.exceptions import ValidationError










# https://ccbv.co.uk

#######################################################
#                  CLASS BASED VIEWS
# https://docs.djangoproject.com/en/2.1/topics/class-based-views/

# https://ccbv.co.uk/projects/Django/2.2/django.views.generic.base/
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/base
from django.views.generic.base import View, TemplateView, RedirectView, ContextMixin, TemplateResponseMixin

# https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-display/
from django.views.generic.detail import BaseDetailView, DetailView, 
                                    SingleObjectMixin, SingleObjectTemplateResponseMixin
# https://ccbv.co.uk/projects/Django/2.2/django.views.generic.list/
from django.views.generic.list import BaseListView, ListView, MultipleObjectMixin, MultipleObjectTemplateResponseMixin

# https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-editing/
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

# https://ccbv.co.uk/projects/Django/2.2/django.views.generic.dates/
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/generic-date-based/
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, WeekArchiveView, DayArchiveView, TodayArchiveView, DateDetailView

# https://ccbv.co.uk/projects/Django/2.2/django.views.generic/GenericViewError/
# 
from django.views.generic import GenericViewError






#######################################################
#           CLASS BASED VIEWS MIXINS
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins/

# https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins-simple/
from django.views.generic.base import ContextMixin, TemplateResponseMixin

# https://ccbv.co.uk/projects/Django/2.2/django.views.generic.detail/
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins-single-object/
from django.views.generic.detail import BaseDetailView, DetailView, 
                                    SingleObjectMixin, SingleObjectTemplateResponseMixin

# https://ccbv.co.uk/projects/Django/2.2/django.views.generic.list/
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins-multiple-object/
from django.views.generic.list import BaseListView, ListView, MultipleObjectMixin, MultipleObjectTemplateResponseMixin

# https://ccbv.co.uk/projects/Django/2.2/django.views.generic.edit/
# https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins-editing/
from django.views.generic.edit import (BaseCreateView, BaseDeleteView, BaseFormView, BaseUpdateView,
                                      CreateView, DeleteView, UpdateView, FormView,
                                      DeletionMixin, FormMixin, ModelFormMixin, ProcessFormView

# https://docs.djangoproject.com/en/2.1/ref/class-based-views/mixins-date-based/
from ??? import YearMixin, MonthMixin, DayMixin, WeekMixin, DateMixin, BaseDateListView








#######################################################
#       CLASS BASED GENERIC VIEWS - FLATTENED INDEX








#######################################################
#                     CONTRIB
# https://docs.djangoproject.com/en/2.1/ref/contrib/

# https://docs.djangoproject.com/en/2.1/ref/contrib/messages/
from django.contrib import messages

# https://docs.djangoproject.com/en/2.1/ref/contrib/admin/
from django.contrib import admin

# https://docs.djangoproject.com/en/2.1/ref/contrib/auth/
# https://docs.djangoproject.com/en/2.1/topics/auth/
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib.auth.models import User

# https://docs.djangoproject.com/en/2.1/topics/auth/default/#module-django.contrib.auth.forms
from django.contrib.auth.forms import AdminPasswordChangeForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, UserChangeForm, UserCreationForm

# https://docs.djangoproject.com/en/2.1/topics/auth/default/#all-authentication-views
# https://ccbv.co.uk/projects/Django/2.2/django.contrib.auth.views/
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, 
PasswordChangeDoneView, PasswordContextMixin, PasswordResetView, PasswordResetCompleteView, PasswordResetDoneView, PasswordResetConfirmView, 
PasswordResetCompleteView, AdminPasswordChangeForm, AuthenticationForm, PasswordChangeForm, 
PasswordResetForm, SUccessURLAllowerdHostsMixin,
UserCreationForm, UserChangeForm, SetPasswordForm)

# https://docs.djangoproject.com/en/2.1/topics/auth/default/#the-login-required-decorator
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required, staff_member_required

# https://ccbv.co.uk/projects/Django/2.2/django.contrib.auth.mixins/
# https://docs.djangoproject.com/en/2.1/topics/auth/default/#the-loginrequired-mixin
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
