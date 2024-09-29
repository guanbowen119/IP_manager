from django.db import models

from apps.users.models import User
from utils.models import BaseModel


class Device(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices', verbose_name='用户')
    ip = models.GenericIPAddressField()
    logged_in = models.BooleanField(default=True)

    class Meta:
        db_table = 'tb_devices'
        verbose_name = '设备管理'
        verbose_name_plural = verbose_name