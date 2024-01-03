from rest_framework import serializers
from .models import User,App, Plan, Subscription
class UserRegisterSerializer(serializers.ModelSerializer):
    # email = serializers.CharField(write_only=True)
    # username = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "username",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print("validated_data", validated_data)
        password = validated_data.pop('password')
        print("password", password)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        print("value",value)
        try:
            user = User.objects.get(email=value)
            print("user", user)
        except User.DoesNotExist:
            raise serializers.ValidationError('No user found with this email')
        return user

    def save(self):
        user = self.validated_data['email']
        user.set_password(self.validated_data['new_password'])
        user.save()

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'



class SubscriptionSerializer(serializers.ModelSerializer):
    # plan = PlanReadSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'

class AppSerializer(serializers.ModelSerializer):
    owner = UserRegisterSerializer()
    subscription = SubscriptionSerializer()
    class Meta:
        model = App
        fields = '__all__'


class SubscriptionReadSerializer(serializers.ModelSerializer):
    app = AppSerializer()
    plan = PlanSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'