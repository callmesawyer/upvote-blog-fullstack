from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.forms import CustomUserCreationForm, CustomUserChangeForm
from blog.models import Post, Like, Comment, CustomUser

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'image', 'is_staff', 'is_active')}
         ),
    )
    # search_fields = ('email',)
    # ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
