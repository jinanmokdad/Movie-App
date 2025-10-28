from django.forms import ModelForm
from .models import Movie
from django import forms

class CreateMovie(ModelForm):
    rating = forms.FloatField(
        min_value=0,
        max_value=5,
        label="Rating (0–5)"
    )
    release_year = forms.IntegerField(
        min_value=1940,
        max_value=2030,
        label="Release Year (1940–2030)"
    )

    class Meta:
        model = Movie
        fields = ['movie_id', 'movie_name', 'release_year', 'rating']
