from rest_framework.serializers import ModelSerializer

from apps.oauth.models import OAuthLarkUser


class OAuthLarkUserModelSerializer(ModelSerializer):
    class Meta:
        model = OAuthLarkUser
        fields = '__all__'
