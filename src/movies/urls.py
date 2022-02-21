from django.urls import path 
from movies.views import (MovieHomeView, 
                    MovieDetailView,
                    AudienceCredentialsView,
                    PaymentView,
                    get_json_showtime_data,
                    create_audience_form,
                    process_single_guests_form,         
                    payment_verification,
                    payment_success_view )


urlpatterns=[
    path('', MovieHomeView.as_view(), name='home-view'),
    path('audience-register/', create_audience_form, name='audience_form'),
    path('verification/<str:ref_code>/', payment_verification, name='verify'),
    path('<int:movie_id>/', MovieDetailView.as_view(), name='movie-detail'),   
    path('<int:movie_id>/booking-success/', payment_success_view, name='payment-success'),
    path('<int:movie_id>/audience/', AudienceCredentialsView.as_view(), name='audience-info'),
    path('<int:movie_id>/add-guest/', process_single_guests_form, name='guest-info'),
    path('<int:movie_id>/showtime/<int:date_id>/', get_json_showtime_data, name='show-time'),
    path('<int:movie_id>/payment/',  PaymentView.as_view(), name='payment')
    
    
]