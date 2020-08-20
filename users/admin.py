from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here. Decorator @admin.register(): admin.site.register(models.User, CustomUserAdmin)과 같음
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """ Custom User """

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom profile",
            {
                "fields": (
                    "avata",
                    "gender",
                    "bio",
                    "birthdate",
                    "city",
                    "currency",
                    "language",
                    "login_method",
                )
            },
        ),
    )
    list_filter = UserAdmin.list_filter + ("superhost", "city")

    list_display = (
        # Model에서 생성된 field를 admin패널에서 보여줄 때 column항목
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "city",
        "email_verified",
        "email_secret",
        "login_method",
    )

