from django.db import models
from box.core.sw_auth.models import BoxAbstractUser 
from django.contrib.auth import get_user_model 
from django.utils import timezone




class ProjectUser(BoxAbstractUser):
    pass 

