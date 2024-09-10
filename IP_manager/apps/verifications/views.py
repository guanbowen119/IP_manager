import io
import random
import string

from captcha.image import ImageCaptcha
from django.http import HttpResponse, JsonResponse
from django.views import View
from django_redis import get_redis_connection
from celery_tasks.sms.tasks import celery_send_sms_code


# Create your views here.
class ImageCodeView(View):

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

class SmsCodeView(View):
    @staticmethod
    def get(request, mobile):
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')

        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        redis_cli = get_redis_connection('code')
        redis_image_code = redis_cli.get(uuid)
        if redis_image_code is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})

        send_flag = redis_cli.get('send_flag_%s' % mobile)
        if send_flag is not None:
            return JsonResponse({'code': 400, 'errmsg': "不要频繁发送验证码"})
        sms_code = '%04d' % random.randint(0, 9999)

        pipeline = redis_cli.pipeline()
        pipeline.setex(mobile, 300, sms_code)
        pipeline.setex('send_flag_%s' % mobile, 60, 1)
        pipeline.execute()

        celery_send_sms_code.delay(mobile, sms_code)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
