from django.contrib import admin
from .models import ArticleAnalysis, UserProfile, UserActivity

@admin.register(ArticleAnalysis)
class ArticleAnalysisAdmin(admin.ModelAdmin):
    list_display = ('title', 'prediction', 'confidence', 'sentiment', 'source_domain', 'created_at', 'user')
    list_filter = ('prediction', 'sentiment', 'source_domain', 'created_at')
    search_fields = ('title', 'content', 'url')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'display_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'full_name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_analyses', 'total_votes', 'reputation_score', 'last_activity')
    list_filter = ('last_activity',)
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
