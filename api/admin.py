from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "description",
        "get_genres",
        "category",
    )
    list_filter = (
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = (
        "name",
        "year",
        "description",
        "category",
    )
    empty_value_display = "-пусто-"


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "slug",
    )
    empty_value_display = "-пусто-"
    prepopulated_fields = {"slug": ("name",)}


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title_id", "author", "text")
    empty_value_display = "-пусто-"


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "author", "text")
    empty_value_display = "-пусто-"


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
