from django.contrib import admin

# Register your models here.
from  .models import *
admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Favourite)
admin.site.register(Draft)

