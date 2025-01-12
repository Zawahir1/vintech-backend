from django.urls import path, include, re_path
from .views import (UsersApiView, GamesApiView, GameLoadsApiView, CashAppsApiView, CashOutsApiView,UniqueGameNamesView,UpdatesCreateView, EODsCreateView, UniquePageGameNamesView,UniqueCashApps, SupervisorRedeemView, current_deposits, current_redeems, PagePairsApiView,DepositListCreateView, RedeemsListCreateView, UniquePagePairs, login, signup)


urlpatterns = [
    path('users/', UsersApiView.as_view()),
    path('games/', GamesApiView.as_view()),
    path('gameloads/', GameLoadsApiView.as_view()),
    path('cashapps/', CashAppsApiView.as_view()),
    path('cashouts/', CashOutsApiView.as_view()),
    path("get-games/", UniqueGameNamesView.as_view()),
    path("get-page-games/", UniquePageGameNamesView.as_view()),
    path("get-pagepairs/", UniquePagePairs.as_view()),
    path("get-cashapps/", UniqueCashApps.as_view()),
    path('pagepairs/', PagePairsApiView.as_view(), name='pagepairs'),
    path('deposit/', DepositListCreateView.as_view(), name='Deposit-list-create'),
    path('redeems/', RedeemsListCreateView.as_view(), name='Redeem-list-create'),
    path('get-redeems/', SupervisorRedeemView.as_view(), name='Supervisor-Redeem-list-create'),
    path('current-deposits/', current_deposits, name="Current-Deposits"),
    path('current-redeems/', current_redeems, name="Current-Redeems"),
    path("updates/", UpdatesCreateView.as_view(), name="updates"),
    path("eods/", EODsCreateView.as_view(), name="eods"),
    re_path('login', login),
    re_path('signup', signup),
]
