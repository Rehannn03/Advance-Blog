from typing import Any
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# profile model for the User
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=250,null=False,blank=False)
    age=models.CharField(max_length=4,blank=True,null=True)
    mobile=models.CharField(max_length=20,null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    profile_pic=models.ImageField(
        'profile_pics/',
        default='static/default_profile_pic.jpg',
        # null=True,
        # blank=True
    )
    created_at=models.DateField(auto_now_add=True)
    follows=models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True

    )
    profile_pic = models.ImageField(
        upload_to ='profilepics/',
        default='default_profile_pic.jpg'
        )

    def __str__(self) -> str:
        return self.user.username
    
    def count_following(self):
        return str(self.follows.count())
    
    def count_followers(self):
        return self.followed_by.count()
    
    
class Category(models.Model):
    name=models.CharField(
        max_length=200,
        null=False,
        blank=False,
        unique=True
        )
    
    def __str__(self) -> str:
        return self.name
    

class Blog(models.Model):
    title=models.CharField(
        max_length=400,
        null=False,
        blank=False
        )
    body=models.TextField()
    likes=models.ManyToManyField(

        Profile,
        blank=True,
        related_name="user_likes"
    )
    # image=img
    user=models.ForeignKey(User,
                           on_delete=models.CASCADE
                           )
    category=models.ForeignKey(Category,
                           on_delete=models.CASCADE
                           )
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(null=True,blank=True)
    published=models.BooleanField(default=False)
    # True if published else False for in Draft
    embedding=models.TextField(null=True,blank=True)
    summary=models.TextField(null=True,blank=True)
    tags_for_seo=models.CharField(max_length=200,blank=True,null=True)
    tags_embedding=models.TextField(null=True,blank=True)
    blog_pic = models.ImageField(
    upload_to ='blog_pics/',
        # default='default_profile_pic.jpg',
        null=True,
        blank=True
        )

    def __str__(self) -> str:
        return f"{self.user.username}  ||  {self.title[:100]}"
    
    def total_likes(self):
        return str(self.likes.count())
    
from datetime import datetime
class Favourite(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username+"  "+self.blog.title[:10]

class Draft(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
    
class Comment(models.Model):
    text=models.CharField(max_length=500,blank=True,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment_time=models.DateTimeField(auto_now_add=True)


# class Tag(models.Model):
#     name=models.CharField(max_length=50,deafult='#lifestyle')

#     def __str__(self) -> str:
#         return self.name