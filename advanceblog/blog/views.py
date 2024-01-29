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
from wordcloud import WordCloud
from django.core.files import File
import math as m
from rest_framework.pagination import PageNumberPagination
# Create your views here.
chroma_collection=BlogConfig.chroma_collection
###########################  Ml/Embedding functions ###################

def give_embedding(text):
    text=f"""
        {text}
        """
    text=re.sub("[\n\.,:!\?&#@\*%]"," ",text)
    text=re.sub(" +"," ",text)

    embedding=BlogConfig.embedding_model.encode(text)
    return f"{embedding}"

def convert_to_numpy(string_embedding):
    return np.array(
        re.sub(" +"," ",(re.sub("[\[\]]"," ",string_embedding))).split(),
        dtype=float
        )

def recommend(target_embedding,query_dict,for_home=True):
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
    print(similar_blog_df)
    if for_home:
        return list(similar_blog_df.id)[:15]
    return list(similar_blog_df.id)[1:15]


def recommend_blogs(blog):
    target=blog.__dict__['embedding']
    target_embedding=convert_to_numpy(target)
    print(type(target_embedding))
    
    similar_blogs=json.dumps(
        list(
            # Blog.objects.filter(category=blog.category).values('id','embedding')
            Blog.objects.all().values('id','embedding')
            )
        )
    # print(similar_blogs)
    
    ids= recommend(target_embedding,similar_blogs,for_home=False)
    print(ids)
    blogs=Blog.objects.filter(id__in=ids)
    recommended_blogs=sorted(
        blogs,
        key=lambda x : ids.index(x.id)
    )
    return recommended_blogs

############################################################################
 
############################## Profile Views ##############################
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
def follow_user(request):
    '''
    one user following another user view
    '''
    try:
        user=Profile.objects.get(user=request.user)
        to_follow_id=request.POST['to_follow_id']
        to_follow=Profile.objects.get(
            id=to_follow_id
        )
        print(to_follow.user.id)
        user.follows.add(to_follow)
        return JsonResponse(
            data={
                'message':f'You followed {to_follow.user.username} successfully....'
            },
            status=201,
            safe=False
        )
    except:
          return JsonResponse(
            data={
                'message':f'OOP"s error occurred.........'
            },
            status=400,
            safe=False
        )
    


##############################################################################

###################### Blog Views #############################################
import os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_blog(request):
    if request.method=='POST':
        user_id=request.user
        print(user_id)
        category_id=1
        # user=User.objects.get(id=user_id)
        category=Category.objects.get(id=category_id)
        blog=Blog()
        blog.user=user_id
        blog.category=category
        blog.title=request.POST['title']
        blog.body=request.POST['body']
        blog.published=bool(request.POST['published'])
        text=request.POST['title']+request.POST['body'][10:800]
        blog.embedding=give_embedding(
            request.POST['title']+request.POST['body']+request.POST['tags_for_seo']
            )
        blog.tags_for_seo=request.POST['tags_for_seo']
        blog.tags_embedding=give_embedding(request.POST['tags_for_seo'].replace("#",""))
        wordcloud = WordCloud().generate(text)
        file_path=f"{user_id.username}_{text[:5]}.png"
        wordcloud.to_file(file_path)
        f=File(open(file_path,"rb"))
        print(f.name)
        blog.blog_pic=f
       

        blog.save()

        f.close()
        os.remove(file_path)
        print("Blog saved successfully")
        return JsonResponse(
            data={
                'mssg':'Blog Posted Successfully...'
            },
            status=201
        )
        
    else:
        return JsonResponse(
            data={
                'mssg':"Method not allowed try post also give the access token in the header while submitting",
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
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
    try:
        user = request.user
        print(user.username)
        blog=Blog.objects.get(id=id)
        recommended_blogs=recommend_blogs(blog)
        blog_serializer=BlogSerializer(blog)
        recommeded_serializer=AllBlogSerializer(recommended_blogs,many=True)
        return JsonResponse(
            data={
                'blog':blog_serializer.data,
                'recommendations_by_engine':recommeded_serializer.data
            },
            safe=False,
            status=200
            )
    except:
        return JsonResponse(
            {
                'mssg':f'No such data for {id}'
            },
            safe=False,
            status=status.HTTP_404_NOT_FOUND
            )

@api_view(['GET'])    
# @permission_classes([IsAuthenticated])
def show_blogs_based_on_category(request,cat_name):
    user=request.user
    print(user)
    # try:
    print(request.session)
    if user.is_authenticated:
        return JsonResponse(
            # data=serializer.data,
            data={'mssg':None},
            safe=False,
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        category_blogs=Blog.objects.filter(
            category__name=cat_name,
            published=True
            
        ).order_by(
            '-created_at'
        )
        serializer=AllBlogSerializer(category_blogs,many=True)
        return JsonResponse(
            data=serializer.data,
            safe=False,
            status=200
        )
    # except:
    #     return JsonResponse(
    #             data={'mssg':None},
    #             safe=False,
    #             status=status.HTTP_204_NO_CONTENT
    #         )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def like_blog(request):
    # get the blog from the request part
    id=request.POST['id']
    blog=Blog.objects.filter(id=id).first()
    user=request.user
    profile=Profile.objects.get(
        user=user
    )
    if profile not in blog.likes.all():
        blog.likes.add(
            profile
        )
        blog.save()
        print("like added")
        other_blogs=Blog.objects.filter(
            user=blog.user
        ).order_by("-created_at")[:5]
        serializer=AllBlogSerializer(other_blogs,many=True)
        return JsonResponse(
            data={
                'message':f'Like added to {blog.title} successfully',
                'other_blogs':serializer.data
            },
            safe=False,
            status=status.HTTP_201_CREATED
        )
    else:
        return JsonResponse(
            data={'message':f'You have already liked {blog.title}'},
            status=status.HTTP_208_ALREADY_REPORTED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_comment(request):
    user=request.user
    blog_id=request.POST['blog_id']
    comment_text=request.POST['comment']
    comment=Comment.objects.create(
        user=user,
        text=comment_text,
        blog=Blog.objects.get(id=blog_id)
    )
    comment.save()
    return JsonResponse(
        data={'message':'Commment added successfully....'},
        safe=False,
        status=201

    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_to_favourite(request):
    user=request.user
    blog_id=request.POST['blog_id']

    fav_blog,created=Favourite.objects.get_or_create(
            user=user,
            blog=Blog.objects.get(id=blog_id)
            )
    if created:
        fav_blog.save()
        return JsonResponse(
            data={
                'message':'blog added to Favourites...'
            },
            status=201
        )
    else:
        return JsonResponse(
            data={
                'message':'blog already in Favourites...'
            },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_from_favourite(request):
    user=request.user
    blog_id=request.POST['blog_id']

    fav_blog=Favourite.objects.get(
            user=user,
            blog__id=blog_id
            )
 
    fav_blog.delete()
    return JsonResponse(
        data={
            'message':'blog removed from Favourites...'
        },
        status=200
        )
   



    # favourite_blog=Favourite.objects.create(
    #         user=user,
    #         blog=Blog.objects.get(id=blog_id)
    # )
    # favourite_blog.save()
    return JsonResponse(
        data={
            'message':'blog added to Favourites...'
        },
        status=201
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favourites(request):
    user=request.user
    user_favs=user.favourite_set.all().order_by('-added_at')
    serializer=FavouriteSerializer(user_favs,many=True)
    return JsonResponse(
        serializer.data,
        safe=False
    )



######################################## Draft Views ##################
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def add_to_draft(request):
    user=request.user
    # blog_id=request.POST['blog_id']
    category_id=5
    # user=User.objects.get(id=user_id)
    category=Category.objects.get(id=category_id)
    blog=Blog()
    blog.user=user
    blog.category=category
    blog.title=request.POST['title']
    blog.body=request.POST['body']
    blog.published=False
    blog.embedding=give_embedding(
            request.POST['title']+request.POST['body']+request.POST['tags_for_seo'].replace("#","")
        )
    blog.tags_for_seo=request.POST['tags_for_seo']
    blog.tags_embedding=give_embedding(request.POST['tags_for_seo'].replace("#",""))
    blog.save()
    drafted_blog=Draft()
    drafted_blog.blog=blog
    drafted_blog.user=user
    drafted_blog.save()
    print("Blog saved to draft successfully.....")
    return JsonResponse(
        data={
            'mssg':'Blog Saved to Draft Successfully...'
        },
        status=201
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])        
def view_draft(request):
    user=request.user
    print(user)
    drafts=Draft.objects.filter(user=user)
    serializer=DraftSerializer(drafts,many=True)
    print(serializer.data)
    return JsonResponse(
        data={
            'drafts':serializer.data,
            'total_drafts':len(drafts)
        },
        safe=False,
        status=200
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def publish_draft(request):
    draft_id=request.POST['draft_id']
    draft=Draft.objects.get(id=draft_id)
    draft.blog.published=True
    draft.blog.save()
    print(draft.blog.published)
    draft.delete()
    return JsonResponse(
        
        {
            'mssg':'Draft published successfulyy....'
            },
            status=200
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def remove_draft(request):
    draft_id=request.POST['draft_id']
    draft=Draft.objects.get(id=draft_id)
    draft.blog.delete()
    draft.delete()
    return JsonResponse(
        {
            'mssg':'Draft blog deleted successfully.......'
            },
        status=200
        )

#######################################################################################


##############################################################################



#################################  Authentication Views #####################################
@api_view(['POST'])
@csrf_exempt
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
@csrf_exempt
def register_user(request):
    username=request.POST['uname']
    password1=request.POST['password1']
    password2=request.POST['password2']
    if password1==password2:
        name=request.POST['name']
        age=request.POST['age']
        mobile=request.POST['mobile']
        email=request.POST['email']
        if 'bio' in request.POST:
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
                    profile.save()
                    return JsonResponse(
                        data={
                        'mssg':"Profile created Successfully...",
                        'status':1,
                        'access_token':str(access)
                        },
                        status=201
                    )
                else:
                    profile.save()
                    return JsonResponse(
                        data={
                        'mssg':"Profile created Successfully...",
                        'status':1,
                        'access_token':str(access)
                        },
                        status=201
                    )

            else:
                profile.save()
                return JsonResponse(
                    {
                        'mssg':"Profile created Successfully...",
                        'status':1,
                        'access_token':str(access)
                    },
                    status=201
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
def for_home_by_liked(request):
    user=request.user
    print(user)
    if user.is_authenticated:
        # give user the blogs based on the activity which will be stored in local storage using react
        # 2 give user the blogs based on the likes
        profile=Profile.objects.get(user=user)
        # get the profile , now based on the profile get the likes
        total_likes_by_user=profile.user_likes.count()
        # print(total_likes_by_user)
        if total_likes_by_user==0:
            # show by activity
            return JsonResponse(
            {
                'msg':'not yet done'
            },
            status=200
            )
        else:
            liked_blogs=json.dumps(
                list(profile.user_likes.all().values('id','embedding'))
                )  #get all liked blog and convert to json for giving to pandas

            blogs=recommend_blogs_for_home(liked_blogs,profile) #call recommed function
            by_liked=AllBlogSerializer(blogs,many=True).data  #serialize data
            paginator = PageNumberPagination()  #create object for pagintion
            paginator.page_size = 10  #set page_size
            result_page = paginator.paginate_queryset(blogs, request) #paginate the queryset

            by_liked=AllBlogSerializer(result_page,many=True).data #serialize 

            return paginator.get_paginated_response(by_liked) #send response

    else:
        blogs=Blog.objects.all().order_by("-created_at")
        paginator=PageNumberPagination()
        paginator.page_size=10
        results=paginator.paginate_queryset(blogs,request)
        serialized_results=AllBlogSerializer(results,many=True).data
        return paginator.get_paginated_response(serialized_results)
    
        # return JsonResponse(
        #     serialized_results,
        #     status=200,
        #     safe=False
        # )


def recommend_blogs_for_home(query_dict,profile):
    df=read_json(query_dict)  #convert json containing id and embedding to df
    df['numpy_embedding']=df.embedding.apply(
        lambda x : np.array(
            re.sub(" +"," ",(re.sub("[\[\]]"," ",x))).split(),
        dtype=float
        )
    )  # convert embedding which is in float to numpy array


    print(df.id.values,"======== are the id of liked blogs")
    target_vector=np.stack(df.numpy_embedding.values).mean(0)  #get the mean of all liked vectors
    blogs=json.dumps(
        list(
        Blog.objects.exclude(
                            id__in=df.id.values
                            ).order_by("-created_at").values(
                'id',
                'embedding'
                )
            )
            ) 
    # 1. get the blogs which are not already liked and also not of the user
    # 2. order them by date andconvert it to dictionary
    # 3. convert the queryset to list
    # 4. cnvert list to json
    ids=recommend(target_vector,blogs) # this will apply cosine similarity and give ids 
    print(ids)
    blogs=Blog.objects.filter(id__in=ids) #get blogs of recommended ids
    recommended_blogs=sorted(
        blogs,
        key=lambda x : ids.index(x.id)
    )  # sort by the index of similarity
    return recommended_blogs

# @api_view(['GET'])
# def setup_vector_db(request):
#     blogs=Blog.objects.all()
#     for blog in blogs:
#         text=blog.title+blog.body+blog.tags_for_seo
#         category=blog.category.name
#         id=str(blog.id)

#         chroma_collection.add(
#             documents=[text],
#             ids=[id],
#             metadatas=[{'category':category}]
#         )

#         print("=====\tdone\t=======")
    
#     return JsonResponse(
#         {
#             'mssg':'done'
#         }
    # )

    





        
    