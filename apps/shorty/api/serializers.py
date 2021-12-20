from rest_framework.serializers import ModelSerializer

from ..models import Shorty


class ShortySerializer(ModelSerializer):

    class Meta:
        model = Shorty
        fields = '__all__'
        read_only_fields = ('session', 'created', 'updated')
