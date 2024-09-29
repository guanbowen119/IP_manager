from rest_framework.serializers import ModelSerializer

from apps.devices.models import Device


class DeviceModelSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'write_only': True,
            }
        }