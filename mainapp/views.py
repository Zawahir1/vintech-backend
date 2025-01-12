from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Users, Games, CashApps, GameLoads, CashOuts, PagePairs, Deposit, Redeems, Updates, EODs
from .serializers import UsersSerializer, GamesSerializer, CashAppsSerializer, GameLoadsSerializer, CashOutsSerializer, PagePairsSerializer, DepositSerializer, RedeemsSerializer, UpdatesSerializer, EODsSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from datetime import datetime, time, timedelta
from django.db.models import Sum
from django.utils import timezone





# Create your views here.

class UsersApiView(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def get(self, request, *args, **kwargs):
        users = Users.objects.all()
        # Exclude passwords from the response
        serializer = UsersSerializer(users, many=True)
        response_data = serializer.data
        for user in response_data:
            user.pop('password', None)  # Remove the password field from the response
        return Response(response_data, status=status.HTTP_200_OK)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "salary": request.data.get("salary"),
            "shift": request.data.get("shift"),
            "type": request.data.get("type"),
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password": request.data.get("password")
        }
        print(data)
        serializer = UsersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # This will create the user without logging in
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def put(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(Users, id=user_id)
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "pseudo_name": request.data.get("pseudo_name"),
            "salary": request.data.get("salary"),
            "shift": request.data.get("shift"),
            "type": request.data.get("type")
        }
        serializer = UsersSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def delete(self, request, *args, **kwargs):
        user_id = request.data.get('id')
        if not user_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(Users, id=user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class GamesApiView(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        games = Games.objects.all()
        serializer = GamesSerializer(games, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        data = {
            "name": request.data.get("name"),
            "credentials": request.data.get("credentials"),
            "login_link": request.data.get("login_link"),
            "balance": request.data.get("balance")
        }
        serializer = GamesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def put(self, request, *args, **kwargs):
        game_id = request.data.get('id')  # Get 'id' from request data
        if not game_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        game = get_object_or_404(Games, id=game_id)
        data = {
            "name": request.data.get("name"),
            "credentials": request.data.get("credentials"),
            "login_link": request.data.get("login_link"),
            "balance": request.data.get("balance")
        }
        serializer = GamesSerializer(game, data=data, partial=True)  # Use partial=True for updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def delete(self, request, *args, **kwargs):
        game_id = request.data.get('id')  # Get 'id' from request data
        if not game_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        game = get_object_or_404(Games, id=game_id)
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class CashAppsApiView(APIView):
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        cashapps = CashApps.objects.all()
        serializer = CashAppsSerializer(cashapps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        data = {
            "cash_tag": request.data.get("cashTagUUID"),
            "ownership": request.data.get("ownership"),
            "system": request.data.get("system"),
            "status": request.data.get("status"),
            "installation_date": request.data.get("installationDate"),
            "delivery_email": request.data.get("deliveryMail"),
            "delivery_password": request.data.get("deliveryPass"),
            "delivery_recovery": request.data.get("deliveryRecovery"),
            "vintech_email": request.data.get("vintechMail"),
            "vintech_password": request.data.get("vintechPass"),
            "vintech_recovery": request.data.get("vintechRecovery"),
            "verification_date": request.data.get("verificationDate"),
            "balance": request.data.get("balance")
        }
        serializer = CashAppsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def put(self, request, *args, **kwargs):
        cashapp_id = request.data.get('id')  # Get 'id' from request data
        if not cashapp_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        cashapp = get_object_or_404(CashApps, id=cashapp_id)
        data = {
            "cash_tag": request.data.get("cashTagUUID"),
            "ownership": request.data.get("ownership"),
            "system": request.data.get("system"),
            "status": request.data.get("status"),
            "installation_date": request.data.get("installationDate"),
            "delivery_email": request.data.get("deliveryMail"),
            "delivery_password": request.data.get("deliveryPass"),
            "delivery_recovery": request.data.get("deliveryRecovery"),
            "vintech_email": request.data.get("vintechMail"),
            "vintech_password": request.data.get("vintechPass"),
            "vintech_recovery": request.data.get("vintechRecovery"),
            "verification_date": request.data.get("verificationDate"),
            "balance": request.data.get("balance")

        }
        serializer = CashAppsSerializer(cashapp, data=data, partial=True)  # Use partial=True for updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def delete(self, request, *args, **kwargs):
        cashapp_id = request.data.get('id')  # Get 'id' from request data
        if not cashapp_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        cashapp = get_object_or_404(CashApps, id=cashapp_id)
        cashapp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class GameLoadsApiView(APIView):
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        gameloads = GameLoads.objects.all()
        data = []
        for load in gameloads:
            game_data = {
                "id": load.id,
                "game_id": load.game.id,  # Accessing the related game's id
                "game_name": load.game.name,  # Accessing the related game's name
                "amount": load.amount,
                'created_at': load.created_at.strftime("%d-%m-%Y %H:%M:%S")
            }
            data.append(game_data)
        return Response(data, status=status.HTTP_200_OK)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        print(request.data)
        game_name = request.data.get("game_name")
        game = get_object_or_404(Games, name=game_name)
        data = {
            "game": game.id,  # Ensure game ID is assigned correctly
            "amount": request.data.get("amount")
        }
        print(data)
        serializer = GameLoadsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def put(self, request, *args, **kwargs):
        game_name = request.data.get("game_name")
        game = get_object_or_404(Games, name=game_name)
        gameload_id = request.data.get('id')  # Get 'id' from request data
        if not gameload_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        gameload = get_object_or_404(GameLoads, id=gameload_id)
        data = {
            "game": game.id,  # Ensure game ID is assigned correctly
            "amount": request.data.get("amount")
        }
        serializer = GameLoadsSerializer(gameload, data=data, partial=True)  # Use partial=True for updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def delete(self, request, *args, **kwargs):
        gameload_id = request.data.get('id')  # Get 'id' from request data
        if not gameload_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        gameload = get_object_or_404(GameLoads, id=gameload_id)
        gameload.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CashOutsApiView(APIView):
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        cashouts = CashOuts.objects.all()
        data = []
        for cashout in cashouts:
            cashapp_data = {
                "id": cashout.id,
                "cashapp_uuid": cashout.cashapp.cash_tag,  # Assuming 'id' is UUID
                "cashout_date": cashout.cashout_date,
                "amount": cashout.amount,
                "status": cashout.status,
                "owner": cashout.owner,
                "by": cashout.by,
                "comment": cashout.comment,
            }
            data.append(cashapp_data)
        return Response(data, status=status.HTTP_200_OK)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def post(self, request, *args, **kwargs):
        print("posted")
        cashapp_uuid = request.data.get("cashapp_uuid")
        cashapp = get_object_or_404(CashApps, cash_tag=cashapp_uuid)
        data = {
            "cashapp": cashapp.id,
            "cashout_date": request.data.get("cashout_date"),
            "amount": request.data.get("amount"),
            "status": request.data.get("status"),
            "owner": request.data.get("owner"),
            "by": request.data.get("by"),
            "comment": request.data.get("comment")
        }
        serializer = CashOutsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def put(self, request, *args, **kwargs):
        cashapp_uuid = request.data.get("cashapp_uuid")
        cashapp = get_object_or_404(CashApps, cash_tag=cashapp_uuid)
        cashout_id = request.data.get('id')  # Get 'id' from request data
        if not cashout_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        cashout = get_object_or_404(CashOuts, id=cashout_id)
        data = {
            "cashapp": cashapp.id,
            "cashout_date": request.data.get("cashout_date"),
            "amount": request.data.get("amount"),
            "status": request.data.get("status"),
            "owner": request.data.get("owner"),
            "by": request.data.get("by"),
            "comment": request.data.get("comment")
        }
        serializer = CashOutsSerializer(cashout, data=data, partial=True)  # Use partial=True for updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def delete(self, request, *args, **kwargs):
        # cashapp_uuid = request.data.get("cashapp_uuid")
        # cashapp = get_object_or_404(CashApps, id=cashapp_uuid)
        cashout_id = request.data.get('id')  # Get 'id' from request data
        if not cashout_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        cashout = get_object_or_404(CashOuts, id=cashout_id)
        cashout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def signup(request):
    serializer = UsersSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # This will create the user
        user.set_password(request.data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)  # Get or create a token
        return Response({'token': token.key, 'user': serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login(request):
    try:
        password = request.data['password']
        username = request.data['username']

        # Attempt to retrieve the user
        user = get_object_or_404(Users, username=username)

        # Check if the password is correct
        if not user.check_password(raw_password=password):
            print("Incorrect Password")
            return Response({'detail': 'Incorrect Password'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the user is saved and exists in the database
        if not user.pk:
            print("User PK is None, saving user")
            user.save()

        # Attempt to get or create a token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # If there's a problem with the Token creation, it might not be related to the user model directly.
        serializer = UsersSerializer(instance=user)
        return Response({'token': token.key, 'user': serializer.data})

    except Users.DoesNotExist:
        return Response({'detail': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
    except IntegrityError as e:
        # Catching the integrity error to provide more meaningful feedback
        print("Integrity Error:", e)
        return Response({'detail': 'Integrity Error: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        # General exception to catch any other issues
        print("Unexpected Error:", e)
        return Response({'detail': 'An unexpected error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class UniqueGameNamesView(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        # Query all unique game names
        unique_names = Games.objects.values_list('name', "id").distinct()
        
        # Convert unique names to a format suitable for the response
        response_data = [{'name': name, "id": id} for name, id in unique_names]
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class UniquePageGameNamesView(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        try:
            page_name = request.query_params.get("name", "").lower().strip()
            print(page_name)
        except Exception as error:
            print(error)
        result = PagePairs.get_page_id_and_games_by_page_name(page_name)
        if result:
            games = result["games"]  # Assuming get_page_id_and_games_by_page_name returns games
            print(games)
            # Serialize the games queryset
            serialized_games = GamesSerializer(games, many=True)
            return Response(serialized_games.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Page not found or no games associated"}, status=status.HTTP_404_NOT_FOUND)

    

class UniqueCashApps(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        unique_names = CashApps.objects.filter(status="Active").values_list('cash_tag', 'id').distinct()
        
        response_data = [{'name': name, "id":id} for name, id in unique_names]
        
        return Response(response_data, status=status.HTTP_200_OK)
    
class UniquePagePairs(APIView):
    @authentication_classes([SessionAuthentication, TokenAuthentication])
    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        unique_names = PagePairs.objects.values_list('page1', 'page2', "id").distinct()
        
        response_data = [{'page1': page1, 'page2': page2, "id": id} for page1, page2, id in unique_names]
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    
class PagePairsApiView(APIView):
    
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        page_pairs = PagePairs.objects.all()
        serializer = PagePairsSerializer(page_pairs, many=True)

        # Create a list to hold the modified data
        modified_data = []

        for item in serializer.data:
            # Pop the existing 'games' key
            games_ids = item.pop('games', [])

            # Fetch detailed game information
            games_details = Games.objects.filter(id__in=games_ids)
            games_serializer = GamesSerializer(games_details, many=True)

            # Add the detailed games information to the item
            item['games_details'] = games_serializer.data

            # Append to the modified data list
            modified_data.append(item)

        return Response(modified_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PagePairsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        page_pair_id = request.data.get('id')
        if not page_pair_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        page_pair = get_object_or_404(PagePairs, id=page_pair_id)
        serializer = PagePairsSerializer(page_pair, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        page_pair_id = request.data.get('id')
        if not page_pair_id:
            return Response({'detail': 'ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

        page_pair = get_object_or_404(PagePairs, id=page_pair_id)
        page_pair.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class DepositListCreateView(APIView):
    # Retrieve the 5 latest Deposit entries and handle POST to create new ones
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page_name = request.query_params.get('page_name').strip()
        agent_id = request.query_params.get('agent').strip()
        # if page_name and agent_id:
        try:
            Deposits = Deposit.objects.filter(agent=agent_id, page=page_name).order_by('-datetime')[:5]
        # else:
        except:
            # If either page_name or agent_id is missing, return the latest 5 entries without filtering
            Deposits = Deposit.objects.order_by('-datetime')[:5]
        serializer = DepositSerializer(Deposits, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        print(request.data)
        serializer = DepositSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class RedeemsListCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Retrieve the 5 latest Redeems entries and handle POST to create new ones
    def get(self, request):
        # Get query parameters for filtering
        page_name = request.query_params.get('page_name').strip()
        agent_id = request.query_params.get('agent').strip()
 
        print(page_name)
        # Filter Redeems by page_name and agent if both are provided
        # if page_name and agent_id:
        try:
            redeems = Redeems.objects.filter(agent=agent_id, page_name=page_name).order_by('-datetime')[:5]
            for redeem in redeems:
                redeem.datetime = redeem.datetime.strftime("%d-%m-%Y %H:%M:%S")
        # else:
        except:
            # If either page_name or agent_id is missing, return the latest 5 entries without filtering
            redeems = Redeems.objects.order_by('-datetime')[:5]

        serializer = RedeemsSerializer(redeems, many=True)
        
        serialized_data = serializer.data
        for item in serialized_data:
            if 'cashtag_uuid' in item:
                del item['cashtag_uuid']
        return Response(serialized_data)
    
    def post(self, request):
        # Log the incoming data

        # Create a copy of the request data and add 'Pending' status
        data_with_status = request.data.copy()  # Create a mutable copy of the data
        data_with_status['status'] = 'Pending'  # Automatically set status to "Pending"

        # Pass the modified data to the serializer
        serializer = RedeemsSerializer(data=data_with_status)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Log and return errors if the data is invalid
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
# SHIFT_TIMES = {
#     'Morning': (time(8, 0), time(16, 0)),   # 8 AM to 4 PM
#     'Evening': (time(16, 0), time(0, 0)),   # 4 PM to 12 AM
#     'Night': (time(0, 0), time(8, 0)),      # 12 AM to 8 AM
# }

# def get_shift_timeframe(shift):
#     start_time, end_time = SHIFT_TIMES[shift]
#     now = datetime.now()

#     # Create datetime objects for the start and end of the shift
#     shift_start = datetime.combine(now.date(), start_time)
#     if end_time < start_time:
#         shift_end = datetime.combine(now.date(), end_time) + timedelta(days=1)
#     else:
#         shift_end = datetime.combine(now.date(), end_time)

#     return shift_start, shift_end


# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def current_deposits(request):
#     shift = request.GET.get('shift', '').strip()

#     if not shift:
#         return Response({'error': 'Shift parameter is required'}, status=400)

#     shift_start, shift_end = get_shift_timeframe(shift)

#     total_deposits = Deposit.objects.filter(
#         datetime__gte=shift_start,
#         datetime__lte=shift_end,
#     ).aggregate(total=Sum('amount'))['total'] or 0

#     return Response({'total_deposits': total_deposits})

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def current_redeems(request):
#     shift = request.GET.get('shift', '').strip()

#     if not shift:
#         return Response({'error': 'Shift parameter is required'}, status=400)

#     shift_start, shift_end = get_shift_timeframe(shift)

#     total_redeems = Redeems.objects.filter(
#         datetime__gte=shift_start,
#         datetime__lte=shift_end,
#         status="Approved"
#     ).aggregate(total=Sum('amount'))['total'] or 0

#     return Response({'total_redeems': total_redeems})


# class SupervisorRedeemView(APIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     # Retrieve all Redeems entries based on the shift and handle PUT requests for updating
#     def get_shift_times(self, shift):
#         """Helper function to determine the start and end time based on the shift."""
#         now = timezone.localtime(timezone.now())  # Get the current local time
        
#         if shift == 'morning':
#             start_time = now.replace(hour=8, minute=0, second=0)
#             end_time = now.replace(hour=16, minute=0, second=0)
#         elif shift == 'evening':
#             start_time = now.replace(hour=16, minute=0, second=0)
#             end_time = now + timedelta(days=1)
#             end_time = end_time.replace(hour=0, minute=0, second=0)
#         elif shift == 'night':
#             start_time = now.replace(hour=0, minute=0, second=0)
#             end_time = now.replace(hour=8, minute=0, second=0)
#         else:
#             return None, None  # Return None if the shift is invalid

#         return start_time, end_time

#     def get(self, request):
#         # Get shift from request data (can also be sent via query_params if you prefer)
#         shift = request.query_params.get('shift', '').strip().lower()  # 'morning', 'evening', or 'night'
        

#         # Validate shift and agent_id presence

#         start_time, end_time = self.get_shift_times(shift)
    
#         if not start_time or not end_time:
#             return Response({"error": "Invalid shift provided"}, status=status.HTTP_400_BAD_REQUEST)

#         # Filter Redeems by agent and datetime within the shift's time range
#         redeems = Redeems.objects.filter(datetime__range=(start_time, end_time))

#         # serializer = RedeemsSerializer(redeems, many=True)
#         data = []
#         for redeem in redeems:
#             redeem_data = {
#                 "id": redeem.id,
#                 "game_id": redeem.game_user_id,  # Accessing the related game's id
#                 "game_name": redeem.game.name,  # Accessing the related game's name
#                 "cashtag": CashApps.objects.filter(id=redeem.cashtag_uuid)[0].cash_tag,
#                 "total_amount": redeem.amount,
#                 "tip": redeem.tip,
#                 "added_back": redeem.added_back,
#                 "paid": redeem.paid,
#                 "remaining": redeem.remaining,
#                 'datetime': redeem.datetime.strftime("%d-%m-%Y %H:%M:%S"),
#                 "status": redeem.status
#             }
#             data.append(redeem_data)
#         return Response(data)
    
#     def put(self, request):
#         redeem_id = request.data.get("id")
#         try:
#             redeem = Redeems.objects.get(id=redeem_id)
#         except Redeems.DoesNotExist:
#             return Response({"error": "Redeem not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         # Partial update, meaning only provided fields will be updated
#         serializer = RedeemsSerializer(redeem, data=request.data, partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



SHIFT_TIMES = {
    'Morning': (time(8, 0), time(16, 0)),   # 8 AM to 4 PM
    'Evening': (time(16, 0), time(0, 0)),   # 4 PM to 12 AM (Midnight)
    'Night': (time(0, 0), time(8, 0)),      # 12 AM to 8 AM
}

def get_current_shift():
    """Determine the current shift based on the current time."""
    now = timezone.localtime(timezone.now())
    current_time = now.time()

    if SHIFT_TIMES['Morning'][0] <= current_time < SHIFT_TIMES['Morning'][1]:
        return 'Morning'
    elif SHIFT_TIMES['Evening'][0] <= current_time or current_time < SHIFT_TIMES['Evening'][1]:
        return 'Evening'
    else:
        return 'Night'

def get_shift_timeframe():
    """Get the start and end time for the current shift based on current time."""
    shift = get_current_shift()
    start_time, end_time = SHIFT_TIMES[shift]
    now = timezone.localtime(timezone.now())

    # Calculate the start and end time for the shift, adjusting for shifts that cross midnight
    shift_start = timezone.make_aware(datetime.combine(now.date(), start_time))
    if end_time < start_time:
        shift_end = timezone.make_aware(datetime.combine(now.date(), end_time) + timedelta(days=1))
    else:
        shift_end = timezone.make_aware(datetime.combine(now.date(), end_time))

    return shift_start, shift_end



@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_deposits(request):
    shift_start, shift_end = get_shift_timeframe()

    total_deposits = Deposit.objects.filter(
        datetime__gte=shift_start,
        datetime__lte=shift_end,
    ).aggregate(total=Sum('amount'))['total'] or 0

    return Response({'total_deposits': total_deposits})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_redeems(request):
    shift_start, shift_end = get_shift_timeframe()

    total_redeems = Redeems.objects.filter(
        datetime__gte=shift_start,
        datetime__lte=shift_end,
        status="Approved"
    ).aggregate(total=Sum('amount'))['total'] or 0

    return Response({'total_redeems': total_redeems})




class SupervisorRedeemView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shift_start, shift_end = get_shift_timeframe()
        redeems = Redeems.objects.filter(datetime__range=(shift_start, shift_end))

        data = []
        for redeem in redeems:
            cashtag = "null"
            if redeem.cashtag_uuid:
                cashtag = redeem.cashtag_uuid
            redeem_data = {
                "id": redeem.id,
                "game_id": redeem.game_user_id,
                "game_name": redeem.game.name,
                # "cashtag": CashApps.objects.filter(id=redeem.cashtag_uuid)[0].cash_tag,
                "cashtag": cashtag,
                "customer_cashtag": redeem.customer_cashtag,
                "total_amount": redeem.amount,
                "tip": redeem.tip,
                "added_back": redeem.added_back,
                "paid": redeem.paid,
                "remaining": redeem.remaining,
                'datetime': redeem.datetime.strftime("%d-%m-%Y %H:%M:%S"),
                "status": redeem.status,
            }
            data.append(redeem_data)

        return Response(data)
    def put(self, request):
        redeem_id = request.data.get("id")
        print(request.data)
        try:
            redeem = Redeems.objects.get(id=redeem_id)
        except Redeems.DoesNotExist:
            return Response({"error": "Redeem not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.data.get("cashtag"):
            print("cashtag_present")
            redeem.cashtag_uuid = request.data.get("cashtag")
            redeem.save(update_fields=["cashtag_uuid"])
            print(redeem.cashtag_uuid)
        # Partial update, meaning only provided fields will be updated
        serializer = RedeemsSerializer(redeem, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
class UpdatesCreateView(APIView):
    # Retrieve the 5 latest Deposit entries and handle POST to create new ones
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        updates = Updates.objects.all()
        data = []
        for update in updates:
            data.append({
                "agent": update.agent.username,
                "datetime": update.datetime.strftime("%m/%d/%Y %H:%M:%S"),
                "id": update.id,
                "update": update.update
                
            })
        # serializer = UpdatesSerializer(updates, many=True)
        # serialized_data = serializer.data
        # for data in serialized_data:
        #     print(data)
        print(data)
        return Response(data)
    
    def post(self, request):
        page_id = request.data.get("page_id")
        page_name = request.data.get("page_name").lower().strip()
        agent_id = request.data.get("agent_id")
        agent = Users.objects.get(id=agent_id)
        data = {"games": {}, "cashapps": {}}
        
        data["page"] = page_name.title()
        
        
        result = PagePairs.objects.get(id=page_id).games.all()
        if result:
            for game in result:
                data["games"][game.name.title()] = game.balance
        cashapps = CashApps.objects.filter(status="Active")
        for cashapp in cashapps:
            data["cashapps"][cashapp.cash_tag] = cashapp.balance
        try:
            Updates.objects.create(agent=agent, update=data)
            return Response(status=status.HTTP_200_OK)
                
                
        
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    



def get_late_shift():
    """Determine the shift based on current time, considering late entries."""
    now = timezone.localtime(timezone.now())
    current_time = now.time()
    print(current_time)
    
    # Iterate over shifts to determine the correct shift with late logic
    for shift, (start_time, end_time) in SHIFT_TIMES.items():
        if start_time < end_time:
            # Regular shifts (Morning or Night) that don't span midnight
            if start_time <= current_time < end_time:
                shift_start = timezone.make_aware(datetime.combine(now.date(), start_time))
                if now < shift_start + timedelta(hours=1):
                    return get_previous_second_shift(shift)
                return get_previous_shift(shift)
        else:
            # Evening shift that crosses midnight
            if start_time <= current_time or current_time < end_time:
                shift_start = timezone.make_aware(datetime.combine(now.date(), start_time))
                if now < shift_start + timedelta(hours=1):
                    return get_previous_second_shift(shift)
                return get_previous_shift(shift)

    return 'Night'  # Default to Night shift if no match

def get_previous_shift(current_shift):
    """Get the previous shift based on the current shift."""
    shift_order = ['Morning', 'Evening', 'Night']
    current_index = shift_order.index(current_shift)
    previous_index = (current_index - 1) % 3
    return shift_order[previous_index]

def get_previous_second_shift(current_shift):
    """Get the previous shift based on the current shift."""
    shift_order = ['Morning', 'Evening', 'Night']
    current_index = shift_order.index(current_shift)
    previous_index = (current_index - 2) % 3
    return shift_order[previous_index]

class EODsCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        eods = EODs.objects.all()
        data = []
        for eod in eods:
            data.append({
                "agent": eod.agent.username,
                "date": eod.datetime.strftime("%d/%m/%Y"),
                "data": eod.eod
            })
        print(data)
        return Response(data)
    
    
    def post(self, request):
        redeems_done = request.data.get("redeems_done")
        redeems_paid_directly = request.data.get("redeems_paid_directly")
        redeems_refunded = request.data.get("redeems_refunded")
        redeems_added_back_and_refunded = request.data.get("redeems_added_back_and_refunded")
        redeems_refunded_and_paid = request.data.get("redeems_refunded_and_paid")
        redeems_paid_from_preshift = request.data.get("redeems_paid_from_preshift")
        redeems_added_back_and_paid = request.data.get("redeems_added_back_and_paid")
        redeems_pending_from_preshift = request.data.get("redeems_pending_from_preshift")
        
        
        agent_id = request.data.get("agent_id")
        agent = Users.objects.get(id=agent_id)
        
        cashapps_results = CashApps.objects.filter(status="Active")
        

                
        data = {
            "shift": "",
            "cashapps": {},
            "games": {},
            "details": {
                "redeems_done": redeems_done,
                "redeems_paid_directly": redeems_paid_directly,
                "redeems_refunded": redeems_refunded,
                "redeems_added_back_and_refunded": redeems_added_back_and_refunded,
                "redeems_refunded_and_paid": redeems_refunded_and_paid,
                "redeems_paid_from_preshift": redeems_paid_from_preshift,
                "redeems_added_back_and_paid": redeems_added_back_and_paid,
                "redeems_pending_from_preshift": redeems_pending_from_preshift                 
            }
        }
        
        for cashapp in cashapps_results:
            data["cashapps"][cashapp.cash_tag] = {"current_score": cashapp.balance, "previous_score": 0}

        games_results = Games.objects.all()
        for game in games_results:
            data["games"][game.name] = {"current_score": game.balance, "previous_score": 0}

        shift = get_late_shift()
        print(shift)
        now = datetime.now()
        if shift == "Night":
        # For the night shift, it's the same day but starts at 12 AM
            shift_start = datetime.combine(now.date(), SHIFT_TIMES[shift][0])
            shift_end = datetime.combine(now.date(), SHIFT_TIMES[shift][1])
            data["shift"] = "Morning"
        elif shift == "Evening":
            # If the shift is 'Evening', the shift is counted as part of the previous day
            previous_day = now.date() - timedelta(days=1)
            shift_start = datetime.combine(previous_day, SHIFT_TIMES[shift][0])
            shift_end = datetime.combine(previous_day, SHIFT_TIMES[shift][1])
            data["shift"] = "Night"
        else:
            # For 'Morning' and other shifts, use the current day
            shift_start = datetime.combine(now.date(), SHIFT_TIMES[shift][0])
            shift_end = datetime.combine(now.date(), SHIFT_TIMES[shift][1])
            data["shift"] = "Evening"
        
        previous_eod = EODs.objects.filter(datetime__gte=shift_start, datetime__lte=shift_end).order_by('-datetime').first()
        
            
        
        if previous_eod:
            eod_data = previous_eod.eod
            for game, game_data in data['games'].items():
                if eod_data["games"][game]["current_score"]:
                    data["games"][game]["previous_score"] = eod_data["games"][game]["current_score"]
            
            for cashapp, cashapp_data in data["cashapps"].items():
                if eod_data["cashapps"][cashapp]["current_score"]:
                    data["cashapps"][cashapp]["previous_score"] = eod_data["cashapps"][cashapp]["current_score"]  
            
        else:
            previous_eod = EODs.objects.all().order_by('-datetime').first()

            if previous_eod:
                eod_data = previous_eod.eod
                for game, game_data in data['games'].items():
                    if eod_data["games"][game]["current_score"]:
                        data["games"][game]["previous_score"] = eod_data["games"][game]["current_score"]
                
                for cashapp, cashapp_data in data["cashapps"].items():
                    if eod_data["cashapps"][cashapp]["current_score"]:
                        data["cashapps"][cashapp]["previous_score"] = eod_data["cashapps"][cashapp]["current_score"]
                    pass
            else:
                pass
        
        EODs.objects.create(eod=data, agent=agent)
        return Response(status=status.HTTP_200_OK)

    
    
    
