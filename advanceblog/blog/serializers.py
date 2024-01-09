from rest_framework import serializers
from .models import *
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile
        fields=['user','name','age','mobile','bio','follows','followed_by']
        # extra_kwargs = {'follows': {'required': False}}
        depth=1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=[
            'title',
            'body',
            'likes',
            'user',
            'category',
            'created_at',
            'updated_at',
            'published',
            'summary',
            'tags_for_seo'
        ]


        