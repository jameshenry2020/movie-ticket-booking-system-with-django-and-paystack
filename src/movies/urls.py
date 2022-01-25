from django.urls import path 
from .views import MovieHomeView, MovieDetailView,get_json_showtime_data,create_audience_form, AudienceCredentialsView


urlpatterns=[
    path('', MovieHomeView.as_view(), name='home-view'),
    path('<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),
    path('audience-register/', create_audience_form, name='audience_form'),
    path('<int:movie_id>/audience/', AudienceCredentialsView.as_view(), name='audience-info'),
    path('<int:movie_id>/showtime/<int:date_id>/', get_json_showtime_data, name='show-time')
]