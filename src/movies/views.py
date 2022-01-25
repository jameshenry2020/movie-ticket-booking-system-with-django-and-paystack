from ast import Add
from django.forms.formsets import formset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from .forms import AddAudienceForm
from movies.models import Movies, ShowTime
# Create your views here.

class MovieHomeView(ListView):
    template_name="movies/index.html"
    model=Movies


class MovieDetailView(View):
    context={}
    def get(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, pk=movie_id)
        self.context['movie_obj']=movie
        
        return render(request, "movies/detail.html", self.context)
    def post(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        date=request.POST.get('date-picked')
        watch_time=request.POST.get('time-picked')
        ticket=request.POST.get('ticket-numb')
        if date is not None and ticket is not None:
            request.session['chosen_date']=date
            request.session['chosen_time']=watch_time
            request.session['ticket_num']=ticket
            return redirect('audience-info', movie_id=movie_id)
        return render(request, "movies/detail.html", self.context)
        

# view to collect booking audience info and show selected date and time
class AudienceCredentialsView(View):
    send_to_guest=False
    def get(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, id=movie_id)
        chosen_date=request.session.get('chosen_date')
        chosen_time=request.session.get('chosen_time')
        num_ticket=request.session.get('ticket_num')
        total_price=int(movie.view_price) * int(num_ticket)
        form=AddAudienceForm()
        showtime=ShowTime.objects.get(id=chosen_time)
        
        context={
            'movie_obj':movie,
            'number_of_ticket':int(num_ticket),
            'date_ch':showtime.watch_date.date,
             'time_ch':showtime.watch_time,
             'total_charge':total_price,
             'form':form
        }

        return render(request, "movies/audience.html", context)


#utility views
def get_json_showtime_data(request, *args, **kwargs):
    movie_id=kwargs['movie_id']
    movie_date=kwargs['date_id']
    movie_time=list(ShowTime.objects.filter(movie__id=movie_id, watch_date__id=movie_date).values()) 
    return JsonResponse({
        'data':movie_time
    })

#utility view for sending formset to template when a checkbox is clicked
def create_audience_form(request):
    num_ticket=int(request.session.get('ticket_num'))
    if num_ticket > 1:
        audience_formset=formset_factory(AddAudienceForm, extra=num_ticket)
    return render(request, "partials/_audience_form.html", {'audienceFormset':audience_formset})
    





    
