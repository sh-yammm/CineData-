from rest_framework import serializers
from .models import Movies, Rating
from django.db.models import Avg


class MoviesListRetrieveSerializer(serializers.ModelSerializer):

    # combined = serializers.SerializerMethodField()

    avg_rating = serializers.SerializerMethodField()

    out_of_users = serializers.SerializerMethodField()

    class Meta:

        model = Movies
        fields = '__all__'
        read_only_fields = ['uuid', 'active_status']
        depth = 1

    def get_avg_rating(self,obj):
        
        avg_rating = obj.rating_set.aggregrate(avg_rating=Avg('rating'))['avg_rating']

        return avg_rating 
    
    def get_out_of_user(self,obj):

        return obj.rating_set.count()
    
    # def get_combined(self,obj):

    #     return f'{obj.name}-{obj.released_year}'

class MoviesCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = Movies
        exclude = ['cast','active_status','uuid']

class RatingSerializer(serializers.ModelSerializer):

    class Meta:

        model = Rating 