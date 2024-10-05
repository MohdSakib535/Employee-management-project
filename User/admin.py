from django.contrib import admin
from User.models import CustomUser,Role,Department

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'role','email')  # 
    search_fields = ('username',)  # Add search capability
    list_filter = ('role',)  # Add filter option

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Role)
