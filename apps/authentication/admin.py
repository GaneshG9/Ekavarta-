from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile, UserVerification


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_verified', 'created_at')
    list_filter = ('user_type', 'is_verified', 'verification_status', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extended Profile', {
            'fields': ('phone_number', 'user_type', 'is_verified', 'verification_status', 
                      'whatsapp_number', 'telegram_username', 'business_name', 'business_type',
                      'interested_services', 'profile_picture', 'address', 'city', 'state', 
                      'country', 'pincode')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Extended Profile', {
            'fields': ('phone_number', 'user_type', 'business_name', 'business_type')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'language_preference', 'ai_interaction_enabled', 'created_at')
    list_filter = ('language_preference', 'ai_interaction_enabled', 'created_at')
    search_fields = ('user__username', 'user__email')


@admin.register(UserVerification)
class UserVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verification_type', 'is_verified', 'verified_at', 'created_at')
    list_filter = ('verification_type', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('verification_token',)
