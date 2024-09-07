# 配置信息，key=value
# 我们指定redis为broker的存储位置
broker_url = 'redis://127.0.0.1:6379/15'
broker_connection_retry_on_startup = True  # 设置在启动broker时如果失败是否重连
