import io
import random
import string

from captcha.image import ImageCaptcha
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection


# Create your views here.
class ImageCodeView(View):

    @staticmethod
    def get(request, uuid):
        chr_all = string.ascii_letters + string.digits
        text = ''.join(random.sample(chr_all, 4))
        img = ImageCaptcha().generate_image(text)

        redis_cli = get_redis_connection('code')
        redis_cli.setex(uuid, 100, text)

        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes = img_bytes.getvalue()

        return HttpResponse(img_bytes, content_type='image/jpeg')
