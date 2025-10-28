from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse

def index(request):
	return render(request,'index.html')


def add_movie(request):
	if request.method == 'POST':
		form = CreateMovie(request.POST)
		if form.is_valid():
			movieform = form.cleaned_data
			movie_id = movieform['movie_id']
			movie_name = movieform['movie_name']
			release_year = movieform['release_year']
			rating = movieform['rating']
			Movie.objects.create(movie_id=movie_id, movie_name=movie_name, release_year=release_year, rating=rating)
			return render(request, 'index.html')
	else:
		form = CreateMovie()
	movies = Movie.objects.all()
	return render(request, 'add_movie.html', {'form': form, 'movies': movies})

def get_movies(request):
	movies = Movie.objects.all()
	return render(request, 'get_movies.html', {'movies': movies})

def update_movie(request, movie_id):
	movie = get_object_or_404(Movie, pk=movie_id)
	if request.method == 'POST':
		form = CreateMovie(request.POST, instance=movie)
		if form.is_valid():
			form.save()
			return redirect('get_movies')
	else:
		form = CreateMovie(instance=movie)
	return render(request, 'update_movie.html', {'form': form, 'movie': movie})

def delete_movie(request, movie_id):
	movie = get_object_or_404(Movie, pk=movie_id)
	if request.method == 'POST':
		movie.delete()
		return redirect('get_movies')
	return render(request, 'delete_movie.html', {'movie': movie})
from django.shortcuts import render
from .forms import CreateMovie
from .models import Movie

		