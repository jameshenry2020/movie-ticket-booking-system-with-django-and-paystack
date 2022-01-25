# Generated by Django 4.0.1 on 2022-01-20 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('duration', models.DurationField(max_length=50)),
                ('release_date', models.DateField()),
                ('rating', models.IntegerField(default=0)),
                ('casts', models.CharField(max_length=500)),
                ('view_price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('movies_art', models.ImageField(upload_to='thumbnail')),
            ],
        ),
        migrations.CreateModel(
            name='WatchDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ShowTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch_time', models.TimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='showtime', to='movies.movies')),
                ('watch_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.watchday')),
            ],
        ),
        migrations.AddField(
            model_name='movies',
            name='view_date',
            field=models.ManyToManyField(to='movies.WatchDay'),
        ),
    ]