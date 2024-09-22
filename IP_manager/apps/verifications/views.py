import io
import random
import string

from captcha.image import ImageCaptcha
from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import celery_send_sms_code


class ImageCodeView(APIView):
    @staticmethod
    def get(request, uuid):
        chr_all = string.ascii_letters + string.digits
        text = ''.join(random.sample(chr_all, 4))
        img = ImageCaptcha().generate_image(text)

        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 100, text)  # 100秒过期

        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes = img_bytes.getvalue()

        return HttpResponse(img_bytes, content_type='image/jpeg')

class SmsCodeView(APIView):
    @staticmethod
    def get(request, mobile):
        query_params = request.query_params.dict()
        image_code = query_params.get('image_code')
        uuid = query_params.get('uuid')

        if not all([image_code, uuid]):
            return Response({'errmsg': '参数不全'}, status=status.HTTP_400_BAD_REQUEST)

        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return Response({'errmsg': '图片验证码已过期'}, status=status.HTTP_400_BAD_REQUEST)
        if redis_image_code.decode().lower() != image_code.lower():
            return Response({'errmsg': '图片验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

        send_flag = redis_cli.get('send_flag_%s' % mobile)
        if send_flag is not None:
            return Response({'errmsg': "不要频繁发送验证码"}, status=status.HTTP_400_BAD_REQUEST)
        sms_code = '%04d' % random.randint(0, 9999)

        pipeline = redis_cli.pipeline()
        pipeline.setex(mobile, 300, sms_code)
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        pipeline.execute()

        celery_send_sms_code.delay(mobile, sms_code)

        return Response(status=status.HTTP_200_OK)
