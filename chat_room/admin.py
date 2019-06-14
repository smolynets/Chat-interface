from django.contrib import admin

from .models import Message, Room, User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('last_message',)


admin.site.register(Message)
admin.site.register(Room)
admin.site.register(User, UserAdmin)
