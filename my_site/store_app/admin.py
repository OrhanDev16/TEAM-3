from django.contrib import admin
from .models import *

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1

class TaskFileInline(admin.TabularInline):
    model = TaskFile
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_at",)

class FavoriteItemInline(admin.TabularInline):
    model = FavoriteItem
    extra = 1

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "age", "phone_number", "status")
    search_fields = ("username", "phone_number")
    list_filter = ("status",)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_name", "category", "owner")
    list_filter = ("category",)
    search_fields = ("project_name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "priority", "completed", "deadline")
    search_fields = ("title",)
    list_filter = ("priority", "completed", "project")
    inlines = [SubtaskInline, TaskFileInline, CommentInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    inlines = [FavoriteItemInline]
