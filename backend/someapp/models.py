from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    pass


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    birth_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.first_name} {self.middle_name or ''} {self.last_name}".strip()


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_year = models.PositiveIntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    file = models.FileField(upload_to='books/', blank=True, null=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="favorites")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f"{self.user.username} {self.author.first_name} {self.author.last_name}"
