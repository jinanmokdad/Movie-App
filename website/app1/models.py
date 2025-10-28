from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Movie(models.Model):
    movie_id = models.IntegerField(primary_key=True)
    movie_name = models.CharField(max_length=100)
    release_year = models.IntegerField(
        validators=[MinValueValidator(1940), MaxValueValidator(2030)]
    )  # release year must be between 1940 and 2030
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )  # rating must be between 0 and 5

    def __str__(self):
        return self.movie_name
