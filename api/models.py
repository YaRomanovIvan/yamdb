import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name="Категория",
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Категории"
        verbose_name = "Категория"

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name="Жанр",
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Наименование", db_index=True
    )
    year = models.PositiveIntegerField(
        validators=[MaxValueValidator(datetime.date.today().year)],
        verbose_name="Год",
        db_index=True,
    )
    description = models.TextField(
        default="",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="titles",
        verbose_name="Категория",
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Тайтлы"
        verbose_name = "Тайтл"

    def get_genres(self):
        return ", ".join([str(p) for p in self.genre.all()])

    get_genres.short_description = "Жанры"

    def __str__(self):
        return (
            f"Наименование: {self.name}, "
            f"Год: {self.year}, "
            f"Жанр: {self.genre}, "
            f"Категория: {self.category}. "
        )


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        "Title",
        on_delete=CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )
    pub_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата написания поста",
        db_index=True,
    )

    class Meta:
        ordering = ["pub_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="unique_title_review"
            )
        ]
        verbose_name = "Обзор"
        verbose_name_plural = "Обзоры"

    def __str__(self):
        return f"Review: {self.text}"


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="comments",
    )
    review = models.ForeignKey(
        Review,
        on_delete=CASCADE,
        related_name="comments",
    )
    text = models.TextField(
        verbose_name="Текст комменатария",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации коммментария",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["pub_date"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f"Comment: {self.text}"
