from django.contrib import admin

from .models import Users, Author, Book, Favorite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from django.db import models
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Users)
class UsersAdmin(ModelAdmin):
    ...


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    compressed_fields = True

    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }


@admin.register(Book)
class OrdersAdmin(ModelAdmin):
    ...


@admin.register(Favorite)
class OrdersAdmin(ModelAdmin):
    ...
