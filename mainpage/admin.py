from django.contrib import admin

from mainpage.models import Article, Comment, LikeList, Image, Audio, LikeListComment

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(LikeListComment)
admin.site.register(LikeList)
admin.site.register(Image)
admin.site.register(Audio)
# Register your models here.
