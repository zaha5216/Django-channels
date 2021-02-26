from django.contrib import admin


from blogapp.models import Post, Comment

class ArticleAdmin(admin.ModelAdmin):

    prepopulated_fields = {'slug': ('title',)}


 # Register your models here.
admin.site.register(Post)
admin.site.register(Comment)

