from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    first_name = None
    last_name = None
    email = models.EmailField(max_length=70, unique=True)
    password = models.CharField(max_length=255)
    is_superuser = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)

class Plan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

class App(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name="user_apps", on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', related_name="app_subscription", on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        if not self.subscription: 
            free_plan = Plan.objects.get(name='Free')  
            subscription = Subscription.objects.create(app=self, plan=free_plan, active=True)
            self.subscription = subscription
            self.save()  

class Subscription(models.Model):
    app = models.OneToOneField(App, related_name="subscription_app", on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)