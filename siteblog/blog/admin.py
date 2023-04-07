from django.contrib import admin
from django.db.models import Q
from .models import *
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Содержание')

    def clean_pinned_post(self):
        """
        Category should have only one pinned post.
        If Category already has pinned post it would be set False
        """
        current_category = self.cleaned_data['category']
        old_pinned_post = Post.objects.filter(Q(category=current_category)&
                                              Q(pinned_post=True))
        if (old_pinned_post.exists()):
            for post in old_pinned_post:
                post.pinned_post = False
                post.save()
        return self.cleaned_data["pinned_post"]

    class Meta:
        model = Post
        fields = '__all__'



class PostAdmin(admin.ModelAdmin):
    # preview
    list_display = ('id', 'title', 'slug',  'author',
              'created_at', 'views', 'category', 'get_miniature',)
    list_display_links = ('id', 'title', 'slug', 'get_miniature',)
    search_fields = ('slug', 'title',)
    list_filter = ('id', 'title', 'created_at', 'views',)

    # editor
    save_as = True
    save_on_top = True
    prepopulated_fields = {'slug':('title',)}
    fields = ('title', 'slug', 'is_published', 'photo', 'get_cover', 'content', 
              'author', 'category', 'pinned_post',
              'tags', 'created_at', 'views', )
    readonly_fields = ('views', 'get_cover', 'created_at',)
    form = PostAdminForm

    def get_photo(self, obj, width=200):
        if obj.photo:
            return mark_safe(f'<img src="{ obj.photo.url }" width="{ width }">')
        else:
            return '-'

    def get_cover(self, obj):
        return self.get_photo(obj, 500)

    def get_miniature(self, obj):
        return self.get_photo(obj, 100)

    get_cover.short_description = 'Обложка'
    get_miniature.short_description = 'Миниатюра'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'active',)
    list_filter = ('post', 'user', 'created_at')
    actions = ['approve_comments',]

    @admin.action(description='Mark selected comments as active')
    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
