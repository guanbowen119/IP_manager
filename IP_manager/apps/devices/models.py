from django.db import models

from apps.users.models import User
from utils.models import BaseModel


class Device(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices', verbose_name='用户')
    ip = models.GenericIPAddressField()