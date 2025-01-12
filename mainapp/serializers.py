from rest_framework import serializers
from .models import Users, Games, CashApps, GameLoads, CashOuts, PagePairs, Deposit, Redeems, Updates, EODs
from django.contrib.auth.models import User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'salary', 'shift', 'type', 'password' ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            salary=validated_data.get('salary', 0),
            shift=validated_data.get('shift', 'Day'),
            type=validated_data.get('type', 'Full-time')
        )
        return user
        
class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = "__all__"
        
        
class CashAppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashApps
        fields = "__all__"
        
        
class GameLoadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLoads
        fields = ['id', 'game', 'amount', 'created_at']
        
        
class CashOutsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashOuts
        fields = ['id', 'cashout_date', 'amount', 'status', 'owner', 'by', 'comment', 'cashapp']
        

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = "__all__"
        


class GamesDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'name']

class PagePairsSerializer(serializers.ModelSerializer):
    games = serializers.PrimaryKeyRelatedField(
        queryset=Games.objects.all(), 
        many=True, 
        required=False
    )
    games_details = GamesDetailsSerializer(source='games', many=True, read_only=True)

    class Meta:
        model = PagePairs
        fields = ['id', 'page1', 'page2', 'games', 'games_details']

    def create(self, validated_data):
        games_data = validated_data.pop('games', [])
        page_pair = PagePairs.objects.create(**validated_data)
        page_pair.games.set(games_data)
        return page_pair

    def update(self, instance, validated_data):
        games_data = validated_data.pop('games', None)
        
        # Only update page1 and page2 if they are being changed to avoid triggering the clean method unnecessarily
        if 'page1' in validated_data:
            instance.page1 = validated_data.get('page1', instance.page1)
        if 'page2' in validated_data:
            instance.page2 = validated_data.get('page2', instance.page2)

        instance.save()

        if games_data is not None:
            instance.games.set(games_data)  # Update the selected games

        return instance
    
    
    
class DepositSerializer(serializers.ModelSerializer):
    game_name = serializers.SerializerMethodField(read_only=True)  # To display the game's name
    agent_name = serializers.CharField(source='agent.username', read_only=True)  # Display the user's username instead of ID

    class Meta:
        model = Deposit
        fields = ['id', 'datetime', 'game', 'game_name', 'amount', 'bonus', 'customer', 'agent', 'agent_name', 'signup', 'page', "cashtag_uuid"]
        extra_kwargs = {
            'game': {'write_only': True},
            'agent': {'write_only': True},  # This is now a reference to Users
        }

    def create(self, validated_data):
        game = validated_data.pop('game')
        agent = validated_data.pop('agent')
        deposit = Deposit.objects.create(game=game, agent=agent, **validated_data)
        return deposit

    # Method to get game name
    def get_game_name(self, obj):
        return obj.game.name if obj.game else None
    
    
    
class RedeemsSerializer(serializers.ModelSerializer):
    game_name = serializers.CharField(source='game.name', read_only=True)  # Display the game name instead of just the ID
    cashtag = serializers.SerializerMethodField()  # Display the CashApp tag based on the UUID

    class Meta:
        model = Redeems
        fields = [
            'id', 'datetime', 'game_user_id', 'game', 'game_name', 
            'page_name', 'amount', 'tip', 'added_back', 'paid', 'remaining', 
            'cashtag_uuid', 'cashtag', 'comments', "agent", "status", "customer_cashtag"
        ]
        extra_kwargs = {
            'game': {'write_only': True},  # Make game field write-only since we display game_name
        }

    # Method to get cashtag based on UUID
    def get_cashtag(self, obj):
        try:
            cashapp = CashApps.objects.get(cash_tag=obj.cashtag_uuid)  # Assuming UUID is unique in CashApps model
            return cashapp.cash_tag
        except CashApps.DoesNotExist:
            return None  # Return None if no matching CashApp is found

    def create(self, validated_data):
        redeem = Redeems.objects.create(**validated_data)
        return redeem
    
class UpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Updates
        fields = "__all__"

class EODsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EODs
        fields = "__all__"