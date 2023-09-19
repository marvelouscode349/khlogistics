from . models import Subscription   
from datetime import date
    
class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
    # Check the user's subscription status
        if request.user.is_authenticated:
            try:
                user_subscription = Subscription.objects.get(user=request.user)
                current_date = date.today()

                if current_date > user_subscription.end_date:
                # Subscription has expired, add a message to the response
                    request.subscription_expired = True
                else:
                    request.subscription_expired = False
            except(Subscription.DoesNotExist):
                request.subscription_expired = True


        response = self.get_response(request)
        return response
