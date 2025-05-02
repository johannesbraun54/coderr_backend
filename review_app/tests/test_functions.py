from review_app.models import Review

def create_test_review(self):
    self.review = Review.objects.create(business_user= self.second_user,
    reviewer = self.user,
    rating= 4,
    description= "Alles war toll!")