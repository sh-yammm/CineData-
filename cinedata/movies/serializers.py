from rest_framework import serializers

from .models import Movies


class MoviesSerializer(serializers.ModelSerializer):

    cast = serializers.PrimaryKeyRelatedField(queryset=Movies.objects.all(), many=True)

    class Meta:

        model = Movies

        fields = '__all__'

        read_only_fields = ['uuid','active_status']