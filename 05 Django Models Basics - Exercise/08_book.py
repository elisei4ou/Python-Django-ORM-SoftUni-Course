from django.db import models


class Book(models.Model):
    class Genres(models.TextChoices):
        FC = 'Fiction', 'Fiction'
        NFC = "Non-Fiction", "Non-Fiction"
        SF = "Science Fiction", "Science Fiction"
        HR = 'Horror', 'Horror'

    title = models.CharField(max_length=30)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=20, choices=Genres.choices)
    publication_date = models.DateField(editable=False, auto_now=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.title