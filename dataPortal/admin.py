from django.contrib import admin

# Register your models here.
from .models import MapData, Tag, Author

# admin.site.register(MapData)


@admin.register(MapData)
class MapDataAdmin(admin.ModelAdmin):
    list_display = ('data_id', 'title', 'date_created', 'uploader')
    list_display_links = ('title',)
    list_filter = ('date_created', 'author')
    
    
# 限制用户权限，只能看到自己编辑的文章
    def get_queryset(self, request):
        qs = super(MapDataAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(uploader=request.user)
      
      
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    list_display_link = ('first_name', )
    
admin.site.site_header = 'SNARC Admin Page'