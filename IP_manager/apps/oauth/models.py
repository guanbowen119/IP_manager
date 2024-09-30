from django.db import models
from utils.models import BaseModel


class OAuthLarkUser(BaseModel):
    """飞书登陆用户数据"""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_lark'
        verbose_name = '飞书登录用户数据'
        verbose_name_plural = verbose_name
