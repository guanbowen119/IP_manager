import json

import lark_oapi as lark
import requests
from lark_oapi.api.authen.v1 import *

from IP_manager.settings import LARK_APP_ID, LARK_APP_SECRET

"""
https://open.feishu.cn/open-apis/authen/v1/authorize?app_id=cli_a673a786b333900d&redirect_uri=http%3A%2F%2F192.168.232.128%3A8000%2Flark_redirect%2F&scope=contact:contact.base:readonly&state=abc
"""

def get_app_access_token(user_access_token):
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {
        'Authorization': f'Bearer {user_access_token}',
    }

    response = requests.get(url, headers=headers)
    print(response.text)


def get_user_access_token(code):
    client = lark.Client.builder() \
        .app_id(LARK_APP_ID) \
        .app_secret(LARK_APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    request: CreateAccessTokenRequest = CreateAccessTokenRequest.builder() \
        .request_body(CreateAccessTokenRequestBody.builder()
                      .grant_type("authorization_code")
                      .code(code)
                      .build()) \
        .build()

    request.headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer t-g1049tnSTRYDD4H3GLM2DQVFKNOAHT3HKA4TZV6Z'
    }

    response: CreateAccessTokenResponse = client.authen.v1.access_token.create(request)

    if not response.success():
        lark.logger.error(
            f"client.authen.v1.access_token.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")
        return

    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

    return response.data.access_token


def get_user_info(user_access_token):
    url = 'https://open.feishu.cn/open-apis/authen/v1/user_info'
    headers = {
        'Authorization': f'Bearer {user_access_token}',
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data.get('data')

from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from IP_manager.settings import SECRET_KEY

def generate_token(open_id):
    s = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    token = s.dumps({'open_id': open_id})
    return token

def check_token(token):
    s = URLSafeTimedSerializer(secret_key=SECRET_KEY)
    try:
        token = s.loads(token, max_age=300)  # 如果传入的token存在时间超过了300秒则错误
    except SignatureExpired:
        return None
    else:
        return token.get('open_id')
