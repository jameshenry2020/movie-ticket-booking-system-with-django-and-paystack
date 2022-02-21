import secrets
from tokenize import Triple

from django.db import models
from django.urls import reverse


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

STATUS_CHOICE=(
    ('pending','pending'),
    ('decline','decline'),
    ('success','success'),
)


class TicketBooking(models.Model):
    movie=models.ForeignKey(Movies, on_delete=models.CASCADE)
    guests=models.ManyToManyField(Audience)
    amount=models.IntegerField(default=0)
    daybooked=models.DateField(blank=True, null=True)
    timebooked=models.CharField(max_length=20, blank=True, null=True)
    is_booked=models.BooleanField(default=False)
    num_of_tickets=models.IntegerField(default=0)
    date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10, choices=STATUS_CHOICE)
    guest_unique_code=models.CharField(max_length=30, unique=True, null=True, blank=True)
    reference_code=models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.movie.title}-booking-{self.id}"
    
    def save(self, *args, **kwargs):
        while not self.reference_code:
            ref=secrets.token_urlsafe(50)
            check_similar_ref=TicketBooking.objects.filter(reference_code=ref)
            if not check_similar_ref:
                self.reference_code=ref
        return super().save(*args, **kwargs)

    def paystack_amount_value(self):
        return int(self.amount) * 100



