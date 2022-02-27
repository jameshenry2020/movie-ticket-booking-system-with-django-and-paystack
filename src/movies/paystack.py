import imp
from django.conf import settings
import requests
from django.template.loader import render_to_string
from django.core.mail import send_mail



class PayStack:
    PAYSTACK_KEY=settings.PAYSTACK_SECRET_KEY
    base_url='https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path=f"/transaction/verify/{ref}"
        headers={
            "Authorization":f"Bearer {self.PAYSTACK_KEY}",
            "Content-Type":"application/json"
        }
        url=self.base_url + path
        response=requests.get(url, headers=headers)
        if response.status_code == 200:
            res=response.json()
            return res['status'], res['data']
        res=response.json()
        return res['status'], res['message']





#send email helper function 
def send_ticket_to_customers(name, movie_title, date, showtime, ticket, price, email):
    render_msg=render_to_string('email_template.html', {
        "guest_name":name,
        "movie_title":movie_title,
        "movie_date":date,
        "movie_time":showtime,
        "ticket_num":ticket,
        "total_price":price
    })
    send_mail(
        "thanks for successful booking a ticket to watch a movie in H & k Cinema",
        render_msg,
        settings.EMAIL_HOST,
        [email,]

    )

    