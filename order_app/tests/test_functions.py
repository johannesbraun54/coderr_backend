from offer_app.models import OfferDetails
from order_app.models import Order

def create_test_order(self):
    self.order = Order.objects.create(
        offer_detail = OfferDetails.objects.get(id=1),
        customer_user=self.user,
        business_user=self.second_user,
        title="Logo Design",
        revisions=3,
        delivery_time_in_days=5,
        price=150,
        features=[
            "Logo Design",
            "Visitenkarten"
        ],
        offer_type="basic",
        status="in_progress"
    )