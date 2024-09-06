from itsdangerous import URLSafeTimedSerializer

from IP_manager.settings import SECRET_KEY

def generate_token(ip_address):
    s = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    token = s.dumps({'IP_address': ip_address})
    return token