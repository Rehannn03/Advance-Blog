from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class AllProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(source='user.username', read_only=True)
    # user = UserSerializer(read_only=True)
    # follows = serializers.SerializerMethodField()
    no_of_followers = serializers.SerializerMethodField()
    no_of_following = serializers.SerializerMethodField()
    no_of_blogs= serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=['id',
                'user',
                'name',
                'profile_pic',
                # 'age',
                # 'mobile',
                # 'bio',
                # 'follows',
                # 'followed_by',
                'no_of_followers',
                'no_of_following',
                'no_of_blogs',

                ]
        
        depth=1


    # def get_follows(self, profile):
        # Check if it's a single object serialization
        # print("========",self.context)
        # if not self.context.get('many'):
           
        #     return None
        # return [follow.user.username for follow in profile.follows.all()]

    # for the number of followers
    def get_no_of_followers(self,profile):
        return profile.followed_by.count()
    

    # for the number of following
    def get_no_of_following(self,profile):
        return profile.follows.count()
    
    # for the number of blogs the user has
    def get_no_of_blogs(self,profile):
        # print((profile.blog_set.count()))
        return profile.blog_set.count()
    
class ProfileSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(source='user.username', read_only=True)
    # user = UserSerializer(read_only=True)

    # for the followers and following of each user
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    no_of_followers = serializers.SerializerMethodField()
    no_of_following = serializers.SerializerMethodField()


    # for the blogs of each user
    blogs= serializers.SerializerMethodField()
    no_of_blogs= serializers.SerializerMethodField()
    class Meta:
        model=Profile
        fields=['id',
                'user',
                'name',
                'profile_pic',
                'age',
                'mobile',
                'bio',
                'following',
                'followers',
                'no_of_followers',
                'no_of_following',
                'no_of_blogs',
                'blogs'

                ]
        
        depth=1



    # for the number of followers
    def get_no_of_followers(self,profile):
        return profile.followed_by.count()
    

    # for the number of following
    def get_no_of_following(self,profile):
        return profile.follows.count()
    
    # for the number of blogs the user has
    def get_no_of_blogs(self,profile):
        # print((profile.blog_set.count()))
        return profile.blog_set.count()
    
    def get_following(self,profile):
        return [{'id':following.id,'username':following.user.username } for following in profile.follows.all()][:10]
    
    def get_followers(self,profile):
        return [
            {'id':follower.id,'username':follower.user.username }
            
            for follower in profile.followed_by.all()
            ][:10]
    
    def get_blogs(self,profile):
        return list(
            profile.blog_set.all().order_by('-created_at').values('id','title','summary')
        )





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


        