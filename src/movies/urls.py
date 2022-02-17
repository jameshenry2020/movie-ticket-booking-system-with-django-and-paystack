from django.urls import path 
from movies.views import (MovieHomeView, 
                    MovieDetailView,
                    AudienceCredentialsView,
                    PaymentView,
                    get_json_showtime_data,
                    create_audience_form,         
                    payment_verification )


urlpatterns=[
    path('', MovieHomeView.as_view(), name='home-view'),
    path('audience-register/', create_audience_form, name='audience_form'),
    path('verification/<str:ref_code>/', payment_verification, name='verify'),
    path('<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),   
    # path('booking-success/', booking_success, name='success'),
    path('<int:movie_id>/audience/', AudienceCredentialsView.as_view(), name='audience-info'),
    path('<int:movie_id>/showtime/<int:date_id>/', get_json_showtime_data, name='show-time'),
    path('<int:movie_id>/payment/',  PaymentView.as_view(), name='ticket-payment')
    
    
]