from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth import get_user_model




# Create your models here.
class Users(AbstractUser):
    salary = models.IntegerField(default=0)
    shift = models.CharField(max_length=50, default="Morning")
    type = models.CharField(max_length=50, default="Agent")
    
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related_name to avoid conflicts
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission, 
        related_name='custom_user_permission_set',  # Custom related_name to avoid conflicts
        blank=True
    )
    
    def __str__(self):
        return self.first_name
    
    
class Games(models.Model):
    name = models.CharField(max_length=100)
    credentials = models.CharField(max_length=200)
    login_link = models.CharField(max_length=250)
    balance = models.IntegerField()
    
    def __str__(self):
        return self.name
    

class GameLoads(models.Model):
    game = models.ForeignKey(Games, on_delete=models.CASCADE) 
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically adds current date & time

    
    def __str__(self):
        return self.amount
    
# Signal to create a GameLoad when a Game is created
@receiver(post_save, sender=Games)
def create_initial_gameload(sender, instance, created, **kwargs):
    if created:  # If a new Game is created
        GameLoads.objects.create(game=instance, amount=instance.balance)


# Signal to update the Game's balance when a GameLoad is added
@receiver(post_save, sender=GameLoads)
def update_game_balance(sender, instance, created, **kwargs):
    if created:  # If a new GameLoad is created
        # Check if the GameLoad is not the first one (i.e., initial balance)
        game_loads_count = GameLoads.objects.filter(game=instance.game).count()
        if game_loads_count > 1:  # Only update if it's not the first GameLoad
            instance.game.balance += instance.amount
            instance.game.save()
            
    

class CashApps(models.Model):
    cash_tag = models.CharField(max_length=50)
    ownership = models.CharField(max_length=20)
    balance = models.IntegerField(default=0)
    system = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    installation_date = models.DateField()
    delivery_email = models.CharField(max_length=50)
    delivery_password = models.CharField(max_length=50)
    delivery_recovery = models.CharField(max_length=100)
    vintech_email = models.CharField(max_length=50)
    vintech_password = models.CharField(max_length=50)
    vintech_recovery = models.CharField(max_length=100)
    verification_date = models.DateField()
    
    
    def __str__(self):
        return self.cash_tag

class CashOuts(models.Model):
    cashapp = models.ForeignKey(CashApps, on_delete=models.CASCADE)
    cashout_date = models.DateField()
    amount = models.IntegerField()
    status = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    by = models.CharField(max_length=100)
    comment = models.CharField(max_length=250, null=True)    
    
    
    
class PagePairs(models.Model):
    page1 = models.CharField(max_length=200)
    page2 = models.CharField(max_length=200)
    games = models.ManyToManyField(Games, blank=True)  # Can have zero or more games

    def __str__(self):
        return f"{self.page1} - {self.page2}"

    # Custom clean method to enforce lowercase uniqueness
    def clean(self):
        # Convert page1 and page2 to lowercase for comparison
        page1_lower = self.page1.lower()
        page2_lower = self.page2.lower()

        # Create a filter for existing page pairs with the same page1 and page2 combination
        existing_pairs = PagePairs.objects.filter(
            (Q(page1__iexact=page1_lower) & Q(page2__iexact=page2_lower)) |
            (Q(page1__iexact=page2_lower) & Q(page2__iexact=page1_lower))
        )

        # Exclude the current instance (for updates)
        if self.pk:
            existing_pairs = existing_pairs.exclude(pk=self.pk)

        # Raise a validation error if such a pair already exists
        if existing_pairs.exists():
            raise ValidationError("A page pair with these values already exists.")

    # Save override to call clean method before saving
    def save(self, *args, **kwargs):
        self.full_clean()  # This calls the clean method to ensure validation
        super().save(*args, **kwargs)
        
    @staticmethod
    def get_page_id_and_games_by_page_name(page):
        # Filter PagePairs where the page name matches either page1 or page2
        page_pair = PagePairs.objects.filter(
            Q(page1__iexact=page) | Q(page2__iexact=page)
        ).first()

        # If a match is found
        if page_pair:
            if page_pair.page1.lower() == page.lower():
                return {'page_id': 1, 'games': page_pair.games.all()}
            elif page_pair.page2.lower() == page.lower():
                return {'page_id': 2, 'games': page_pair.games.all()}

        # If no match is found
        return None
        
class Deposit(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)  # Automatically adds current date & time
    game = models.ForeignKey(Games, on_delete=models.CASCADE)  # Foreign key to the Games model
    page = models.CharField(max_length=200)  # Field to store page information (either page1 or page2)
    amount = models.IntegerField()
    bonus = models.IntegerField(default=0)  # Default bonus is 0
    customer = models.CharField(max_length=100)  # Customer field
    agent = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Foreign key to Users (agent)
    signup = models.BooleanField(default=False)  # Checkbox for signup, default to False
    cashtag_uuid = models.CharField(max_length=50)  # Field to store CashTag UUID

    
    def __str__(self):
        return f"Redeem by {self.customer} for game {self.game.name} on page {self.page}"
    
    
class Redeems(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)  # Automatically adds current date & time
    game_user_id = models.CharField(max_length=100)  # ID of the user in the game
    game = models.ForeignKey(Games, on_delete=models.CASCADE)  # Foreign key to the Games model
    page_name = models.CharField(max_length=200)  # Page name (similar to Deposit table)
    amount = models.IntegerField()  # Amount to be redeemed
    tip = models.IntegerField(default=0)  # Tip amount, default is 0
    added_back = models.IntegerField(default=0)  # Amount added back, default is 0
    paid = models.IntegerField(default=0)  # Amount paid, default is 0
    remaining = models.IntegerField(default=0)  # Remaining amount, default is 0
    cashtag_uuid = models.CharField(max_length=50, null=True)  # Field to store CashTag UUID
    agent = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Foreign key to Users (agent)
    status = models.CharField(max_length=100)
    customer_cashtag = models.CharField(max_length=50, null=True)

    comments = models.TextField(null=True, blank=True)  # Optional comments field

    def __str__(self):
        return f"Redeem by {self.agent} for game {self.game.name} on page {self.page_name}"
    
class Updates(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    update = models.JSONField(default=dict)
     

class EODs(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    eod = models.JSONField(default=dict)
    
@receiver(post_save, sender=Redeems)
def update_game_balance_on_redeem(sender, instance, created, **kwargs):
    if instance.status == "Approved":  
        # Check if the GameLoad is not the first one (i.e., initial balance)
        instance.game.balance += instance.amount - instance.added_back
        instance.game.save()
        print(instance.cashtag_uuid)
        cashapp = CashApps.objects.get(cash_tag=instance.cashtag_uuid)
        cashapp.balance -= instance.paid
        cashapp.save()
        
        
@receiver(post_save, sender=Redeems)
def update_cashapp_balance_on_cashout(sender, instance, created, **kwargs):
    if created:
        cashapp = CashApps.objects.get(cash_tag=instance.cashapp)
        cashapp.balance -= instance.amount
        cashapp.save()

            
    
@receiver(post_save, sender=Deposit)
def update_game_balance_on_deposit(sender, instance, created, **kwargs):
    print(instance.signup)
    if created:
        instance.game.balance -= instance.amount - instance.bonus
        instance.game.save()
        if instance.signup == False:
            cashapp = CashApps.objects.get(id=instance.cashtag_uuid)
            cashapp.balance += instance.amount - instance.bonus
            cashapp.save()
            
@receiver(post_save, sender=CashOuts)
def update_cashapp_on_cashout(sender, instance, created, **kwargs):
    if created:
        # Get the related CashApp instance
        cashapp = instance.cashapp
        # Subtract the cashout amount from the balance
        cashapp.balance -= instance.amount
        # Save the updated cashapp balance
        cashapp.save()