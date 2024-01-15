from django.shortcuts import render
from rest_framework.decorators import *
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import JWTAuthentication
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework import status
import json
from django.contrib.auth.models import User
from .apps import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
import numpy as np
import re
from pandas import *
from sklearn.metrics.pairwise import cosine_similarity
# Create your views here.

def give_embedding(text):
    text=f"""
        {text}
        """
    embedding=BlogConfig.embedding_model.encode(text)
    return f"{embedding}"

def convert_to_numpy(string_embedding):
    return np.array(
        re.sub(" +"," ",(re.sub("[\[\]]"," ",string_embedding))).split(),
        dtype=float
        )

def recommend(target_embedding,query_dict):
    similar_blog_df=read_json(query_dict)
    similar_blog_df['similarity']=similar_blog_df.embedding.apply(
        lambda x :cosine_similarity(
            [target_embedding],
            [np.array(
            re.sub(" +"," ",(re.sub("[\[\]]"," ",x))).split(),
        dtype=float
        )]
        )[0][0]
        )
    similar_blog_df.sort_values('similarity',inplace=True,ascending=False)
    return list(similar_blog_df.id)[1:]


def recommend_blogs(blog):
    target=blog.__dict__['embedding']
    target_embedding=convert_to_numpy(target)
    print(type(target_embedding))

    similar_blogs=json.dumps(
        list(
            Blog.objects.filter(category=blog.category).values('id','embedding')
            )
        )
    # print(similar_blogs)
    
    return recommend(target_embedding,similar_blogs)

    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def show_all_profiles(request):
    if request.method=='GET':
        profiles=Profile.objects.all()
        print(json.dumps(list(profiles.values('id','name'))))
        profile_serializer=AllProfileSerializer(profiles,many=True)
        data=profile_serializer.data
        return JsonResponse(
            data=data,
            safe=False,
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def show_profile(request,id):
    if request.method=='GET':
        profile=Profile.objects.filter(id=id).first()
        print(profile.__dict__)
        print(profile)
        profile_serlizer=ProfileSerializer(profile)
        data=profile_serlizer.data
        print(data)
        return JsonResponse(
            data=data,
            safe=False,
            status=status.HTTP_200_OK
        )



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_blog(request):
    if request.method=='POST':
        user_id=request.user
        print(user_id)
        category_id=3
        # user=User.objects.get(id=user_id)
        category=Category.objects.get(id=category_id)
        blog=Blog()
        blog.user=user_id
        blog.category=category
        blog.title=request.POST['title']
        blog.body=request.POST['body']
        blog.published=bool(request.POST['published'])
        blog.embedding=give_embedding(
             request.POST['title']+request.POST['body']+request.POST['tags_for_seo']
            )
        blog.tags_for_seo=request.POST['tags_for_seo']
        blog.tags_embedding=give_embedding(request.POST['tags_for_seo'].replace("#",""))
        blog.save()
        print("Blog saved successfully")
        return JsonResponse(
            data={
                'mssg':'Blog Posted Successfully...'
            },
            status=200
        )
        
    else:
        return JsonResponse(
            data={
                'mssg':"Method not allowed try post also give the access token in the header while submitting",
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
@api_view(['GET'])
def show_categories(request):
    if request.method=='GET':
        cats=Category.objects.all()
        category_serializer=CategorySerializer(cats,many=True)
        return JsonResponse(
            data=category_serializer.data,
            status=200,
            safe=False
            )
    else:
        return  JsonResponse(
            data={
                'mssg':"Method not allowed try get ",
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@api_view(['GET'])    
@permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
def show_blog(request,id):
    # try:
    user = request.user
    print(user.username)
    blog=Blog.objects.get(id=id)
    print(recommend_blogs(blog))
    # print(blog)
    blog_serializer=BlogSerializer(blog)
    return JsonResponse(
        data=blog_serializer.data,
        safe=False,
        status=200
        )
    # except:
    #     return JsonResponse(
    #         {
    #             'mssg':f'No such data for {id}'
    #         },
    #         safe=False,
    #         status=status.HTTP_404_NOT_FOUND
    #         )




#################################  Authentication Views #####################################
@api_view(['POST'])
def login_user(request):
    username=request.POST['uname']
    password=request.POST['password']
    user=authenticate(request,username=username,password=password)
    if user is None:
        return JsonResponse({'mssg':'Incorrct Credentials','status':0},status=400)
    else:
        refresh=RefreshToken.for_user(user)
        access=refresh.access_token
        # print(str(AccessToken.for_user(user)))
        print(access)
        return JsonResponse(
            data={
                'access':str(access)
            },
            status=200
        )


@api_view(['POST'])
def register_user(request):
    username=request.POST['uname']
    password1=request.POST['password1']
    password2=request.POST['password2']
    if password1!=password2:
        # if both passwords dont match
        name=request.POST['name']
        age=request.POST['age']
        mobile=request.POST['mobile']
        email=request.POST['email']
        if bio in request.POST:
            bio=request.POST['bio']
        else:
            bio=None
        try:
        
            
            new_user=User.objects.create_user(
                username=username,
                password=password1,
                email=email
            )
            new_user.save()

            refresh=RefreshToken.for_user(new_user)
            access=refresh.access_token
            print(f"=========\n{str(access)}\n========")

            profile=Profile()
            profile.user=new_user
            profile.name=name
            profile.age=age
            profile.mobile=mobile
            profile.bio=bio

            if request.FILES:
                if 'profile_pic' in request.FILES:
                    profile.profile_pic=request.FILES['profile_pic']
                else:
                    profile.save()
                    return JsonResponse(
                        data={
                        'mssg':"Profile created Successfully...",
                        'status':1,
                        'access_token':str(access)
                        },
                        status=200
                    )

            else:
                profile.save()
                return JsonResponse(
                    {
                        'mssg':"Profile created Successfully...",
                        'status':1,
                        'access_token':str(access)
                    },
                    status=200
                )

        except:
            return JsonResponse(
                {
                    'mssg':f"Try a different username... '{username}' is already taken ",
                    'status':0
                },
                status=400
            )
    else:
        return JsonResponse(
            data={
                'mssg':"Passwords Dont Match ... Try Again",
                'status':0
            },
            safe=False,
            status=status.HTTP_400_BAD_REQUEST
            )
    
#############################################################################################

@api_view(['GET'])
def home(request):
    user=request.user
    if user.is_authenticated:
        print("======")
    return JsonResponse({'mssg':'done'})
