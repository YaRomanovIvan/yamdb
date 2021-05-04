from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializers(many=True, required=False)
    category = CategorySerializers(required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        required=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        """Author and title unique validation.

        Author can't publish more than one review on title. Validator also
        should be run only during creating review obj.
        """

        request = self.context.get("request")
        if request.method != "POST":
            return data

        view = self.context.get("view")
        author = request.user
        title_id = view.kwargs.get("title_id")
        is_author_has_review = Review.objects.filter(
            author=author, title__id=title_id
        ).exists()

        if is_author_has_review:
            raise serializers.ValidationError(
                "The user can't publish more than one review on title. "
                "But he have written one already."
            )
        return data

    class Meta:
        model = Review
        exclude = ["title"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        exclude = ["review"]
