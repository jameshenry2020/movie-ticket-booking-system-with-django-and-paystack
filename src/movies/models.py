import email
from django.urls import reverse
from django.db import models

# Create your models here.
class WatchDay(models.Model):
    date=models.DateField()


    def __str__(self) -> str:
        return f"day-of-movies-{self.id}"

class Movies(models.Model):
    title=models.CharField(max_length=200)
    genre=models.CharField(max_length=200)
    description=models.TextField()
    duration=models.CharField(max_length=50, default="1hour 30mins")
    release_date=models.DateField()
    rating=models.IntegerField(default=0)
    casts=models.CharField(max_length=500)
    view_price=models.DecimalField(max_digits=7, decimal_places=2)
    movies_art=models.ImageField(upload_to="thumbnail")
    view_date=models.ManyToManyField(WatchDay)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie-detail', kwargs={'movie_id':self.pk})


class ShowTime(models.Model):
    movie=models.ForeignKey(Movies, related_name="showtime", on_delete=models.CASCADE)
    watch_date=models.ForeignKey(WatchDay, on_delete=models.CASCADE)
    watch_time=models.TimeField()

    def __str__(self):
        return f"{self.movie.title}-at-{self.watch_time}"

GENGER_CHOICE=(
    ("male", "male"),
    ("female", "female")
)


class Audience(models.Model):
    movie=models.ForeignKey(Movies, related_name='booked_audience', on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    email=models.EmailField()
    gender=models.CharField(max_length=6, choices=GENGER_CHOICE)

    def __str__(self):
        return self.name


class TicketBought(models.Model):
    # movie=
    # guest=
    # amount=
    # ticket=
    # completed=
    # date=
    pass


