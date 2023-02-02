from django.contrib import admin
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
    fields = ('title', 'slug', 'photo', 'get_cover', 'content', 'author',
              'category', 'tags', 'created_at', 'views', )
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

