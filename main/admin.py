from django.contrib import admin
from .models import Collection, Card, StudyProgress


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'user')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('question', 'collection', 'created_at', 'updated_at')
    list_filter = ('created_at', 'collection')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StudyProgress)
class StudyProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'collection', 'updated_at')
    list_filter = ('updated_at',)
    search_fields = ('user__username', 'collection__name')
    readonly_fields = ('updated_at',)
