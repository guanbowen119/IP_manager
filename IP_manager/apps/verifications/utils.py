from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from IP_manager.settings import SECRET_KEY

def generate_token(ip_address):
    s = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    token = s.dumps({'ip_address': ip_address})
    return token

def check_token(token):
    s = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    try:
        token = s.loads(token, max_age=300)  # 如果传入的token存在时间超过了3600秒则错误
    except SignatureExpired:
        return None
    else:
        return token.get('ip_address')
