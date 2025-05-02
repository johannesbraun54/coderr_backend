from offer_app.models import Offer, OfferDetails

def create_test_offer(self):
    self.offer = Offer.objects.create(
        user_id=self.user.id,
        title="Grafikdesign-Paket",
        image="",
        description="Ein umfassendes Grafikdesign-Paket für Unternehmen.",
        min_price=100,
        min_delivery_time=7,
        user_details = {'first_name': "Kevin", 
                        'last_name': "Kramer" , 
                        'username': "kevin" }
    )


def create_test_offerdetails(self):
    self.offerdetails = OfferDetails.objects.create(
        offer_id=self.offer.id,
        title="Basic Design",
        revisions=2,
        delivery_time_in_days=5,
        price=100,
        features=["Logo Design", "Visitenkarte"],
        offer_type="basic",
    )

    self.offerdetails = OfferDetails.objects.create(
        offer_id=self.offer.id,
        title="Standard Design",
        revisions=5,
        delivery_time_in_days=7,
        price=200,
        features=["Logo Design", "Visitenkarte", "Briefpapier"],
        offer_type="standard"
    )

    self.offerdetails = OfferDetails.objects.create(
        offer_id=self.offer.id,
        title="Premium Design",
        revisions=10,
        delivery_time_in_days=10,
        price=500,
        features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
        offer_type="premium"
    )
