"""
生产者（）
消费者
队列（中间人，经纪人）
celery -- 将这三者实现了

在终端中执行这行代码以开启celery服务
celery -A celery_tasks.main worker -l info -P eventlet （windows系统需要添加最后一个参数）
"""

import os
from celery import Celery

# 为celery的运行来设置django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')

# 1.创建celery实例
app = Celery('meiduo_mall')

# 2.设置broker
# 通过加载配置文件设置broker
app.config_from_object('celery_tasks.config')

# 3.让celery自动检测指定的包的任务
# autodiscover_tasks的参数是一个列表，列表中的元素是tasks的路径
app.autodiscover_tasks(['celery_tasks.sms'])
