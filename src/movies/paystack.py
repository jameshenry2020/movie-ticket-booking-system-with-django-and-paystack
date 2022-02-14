from django.conf import settings
import requests



class PayStack:
    PAYSTACK_SECRET_KEY=settings.PAYSTACK_SECRET_KEY
    base_url='https://api.paystack.co'

    def verify_payment(self, ref, *args, **kwargs):
        path=f"/transaction/verify/{ref}"
        headers={
            "Authorization":f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "Content-Type":"application/json"
        }
        url=self.base_url + path
        response=requests.get(url, headers=headers)
        if response.status_code == 200:
            res=response.json()
            return res['status'], res['data']
        res=response.json()
        return res['status'], res['message']