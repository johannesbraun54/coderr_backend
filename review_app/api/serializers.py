from rest_framework import serializers
from review_app.models import Review
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer']

    def _valdiate_double_rate(self, request):
        has_already_rated_user = Review.objects.filter(
            business_user=self.initial_data.get('business_user'), reviewer=request.user).exists()
        if has_already_rated_user:
            raise serializers.ValidationError(
                {'error': 'already rated this user'})

    def _validate_user_type(self):
        business_user = User.objects.get(pk=self.initial_data.get('business_user'))
        if business_user.userprofile.type == "customer":
            raise serializers.ValidationError(
                {'error': 'you can only rate business users'})

    def _validate_patch_fields(self, request):
        if request.method == 'PATCH':
            request_contains_reviewer = request.data.get('reviewer', None)
            request_contains_business_user = request.data.get('business_user', None)
            if request_contains_reviewer or request_contains_business_user:
                raise serializers.ValidationError(
                    {'error': 'you can only patch rating and description'})

    def validate_business_user(self, value):
        request = self.context.get('request')
        self._valdiate_double_rate(request)
        self._validate_user_type()
        self._validate_patch_fields(request)
        return value

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review