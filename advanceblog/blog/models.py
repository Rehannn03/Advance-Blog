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
    bio=models.TextField()
    # profile_pic=models.ImageField()
    created_at=models.DateField(auto_now_add=True)
    follows=models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False

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

        Profile
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
    embedding=models.TextField()
    summary=models.TextField()
    tags_for_seo=models.CharField(max_length=200,blank=True,null=True)


    def __str__(self) -> str:
        return f"{self.user.username}  ||  {self.user.title[:10]}"
    
    def total_likes(self):
        return str(self.likes.count())
    

class Favourite(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username

class Draft(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
    



