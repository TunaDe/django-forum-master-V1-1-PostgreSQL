from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# NOTE: Stripe is only needed when users hit the payment endpoints.
# Import it lazily so management commands (e.g. createsuperuser) can run
# even if the optional dependency isn't installed.
try:
    import stripe  # type: ignore
except ModuleNotFoundError:
    stripe = None


def _get_stripe():
    if stripe is None:
        raise ImproperlyConfigured(
            "Stripe support is not available because the 'stripe' package is not installed. "
            "Install it with: pip install stripe"
        )
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


# Create your views here.


def advert(request):
    if request.method == "POST":
        return redirect('advert:ad_checkout')
    return render(request, "advert/ad_content.html")


def checkout(request):
    context = { "key":settings.STRIPE_PUBLISHABLE_KEY }
    if request.method == "POST":
        return render(request, "advert/successful_ad.html")
    return render(request, "advert/buy_ad.html", context)



def checked_out(request):
    stripe_client = _get_stripe()
    if request.method == "POST":
        stripe_client.Charge.create(
            amount=1000,
            currency="usd",
            description="Advert payment",
            source=request.POST["stripeToken"],
        )
    return render(request, "advert/paid_ads.html")
