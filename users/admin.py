from django.contrib import admin
from.models import Profile
# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "avatar", "newsletter_subscription"]
    readonly_fields = []
    search_fields = ["user__username", "user__email", "user__first_name", "user__last_name", "bio"]
    list_filter = ["newsletter_subscription"]
    empty_value_display = "null"    
