from django.utils.crypto import get_random_string
from django.forms.formsets import formset_factory
from django.http import  HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.conf import settings
from django.views.generic import ListView
from .forms import AddAudienceForm
from movies.models import Movies, ShowTime,TicketBooking
from movies.paystack import PayStack, send_ticket_to_customers
# Create your views here.

class MovieHomeView(ListView):
    template_name="movies/index.html"
    model=Movies


class MovieDetailView(View):
    context={}
    guest_code=get_random_string(length=12)
    def get(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, pk=movie_id)
        self.context['movie_obj']=movie
        
        return render(request, "movies/detail.html", self.context)
    def post(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, pk=movie_id)
        date=request.POST.get('date-picked')
        watch_time=request.POST.get('time-picked')
        ticket=request.POST.get('ticket-numb')
        showtime=ShowTime.objects.get(id=watch_time)
        if date is not None and ticket is not None:
            #store the input date and time with ticket quantity in session
            request.session['chosen_date']=date
            request.session['chosen_time']=watch_time
            request.session['ticket_num']=ticket
            #create the initial booking instance
            price=movie.view_price
            amt=int(price) * int(ticket)
            chosen_date=showtime.watch_date.date
            chosen_time=showtime.watch_time
            ticket_num=int(ticket)
            booking=TicketBooking.objects.create(movie=movie, amount=amt, daybooked=chosen_date, timebooked=chosen_time, num_of_tickets=ticket_num, status="pending", guest_unique_code=self.guest_code)

            request.session['guest_unique_code']=booking.guest_unique_code
             
            return redirect('audience-info', movie_id=movie_id)
        return render(request, "movies/detail.html", self.context)
        

# view to collect booking audience info from multiple guests and show selected date and time
class AudienceCredentialsView(View):
    def get(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, id=movie_id)
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
    def post(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, id=movie_id)
        chosen_time=request.session.get('chosen_time')
        showtime=ShowTime.objects.get(id=chosen_time)
        num_ticket=int(request.session.get('ticket_num'))
        guest_code=request.session.get('guest_unique_code')
        empty_form=AddAudienceForm()
        get_booking=TicketBooking.objects.get(guest_unique_code=guest_code, is_booked=False)
        context={
            'movie_obj':movie,
            'number_of_ticket':int(num_ticket),
            'date_ch':showtime.watch_date.date,
            'time_ch':showtime.watch_time,
            'form':empty_form
             
        }
        
        AudienceFormSet=formset_factory(AddAudienceForm, extra=num_ticket)
        audience_forms_submits=AudienceFormSet(request.POST or None)
        if audience_forms_submits.is_valid():
            for form in audience_forms_submits:
                audience_instance=form.save(commit=False)
                audience_instance.movie=movie
                audience_instance.save()
                get_booking.guests.add(audience_instance)
            return redirect('payment', movie_id=movie_id )
        return render(request, "movies/audience.html", context)
        
           
        
                



# paystack payment initialisation view
class PaymentView(View):
    def get(self, request, *args, **kwargs):
        movie_id=kwargs['movie_id']
        movie=get_object_or_404(Movies, pk=movie_id)
        guest_code=request.session.get('guest_unique_code')
        ticket=TicketBooking.objects.get(movie=movie, is_booked=False, guest_unique_code=guest_code)
        context={
            'booking_obj':ticket,
            'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY
        }
        return render(request, "movies/payment.html", context)




#verify payment callback handle
def payment_verification(request, ref_code):
    booking=get_object_or_404(TicketBooking, reference_code=ref_code)
    chosen_time=request.session.get('chosen_time')
    showtime=ShowTime.objects.get(id=chosen_time)
    paystack=PayStack()
    stats, result=paystack.verify_payment(ref_code)
    if stats and result['status']=='success':
        booking.is_booked=True
        booking.status='success'
        booking.save()
        number_of_ticket=int(request.session.get('ticket_num'))
        for guest in booking.guests.all():
            #send the ticket mail to each guests
            send_ticket_to_customers(guest.name, guest.movie.title, showtime.watch_date.date, showtime.watch_time, number_of_ticket,booking.amount, guest.email)
            print('sending ticket email to guest')
        return redirect('payment-success', movie_id=booking.movie.id) 
    return redirect('payment', movie_id=booking.movie.id)


def payment_success_view(request, movie_id):
    movie=get_object_or_404(Movies, pk=movie_id)
    context={
        'movie_obj':movie
    }
    return render(request, "movies/success.html", context)
    

    
  



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



#processing  single audience form instance, in case where the user booking decision to receive the multiple tickets by himself
#rather than send the ticket to the guests his booking for!
def process_single_guests_form(request, *args, **kwargs):
    movie_id=kwargs['movie_id']
    guest_code=request.session.get('guest_unique_code')
    movie=get_object_or_404(Movies, id=movie_id)
    get_booking=TicketBooking.objects.get(guest_unique_code=guest_code, is_booked=False)
    if request.method=="POST":
        form_submit=AddAudienceForm(request.POST or None)
        if form_submit.is_valid():
            instance=form_submit.save(commit=False)
            instance.movie=movie
            instance.save()
            get_booking.guests.add(instance)
            return redirect('payment', movie_id=movie_id)
        return redirect('audience-info', movie_id=movie_id)








    
