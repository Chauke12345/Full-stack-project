from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # ----------------------
    # HOME & GAME
    # ----------------------
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),

    # ----------------------
    # PURCHASE & CHECKOUT
    # ----------------------
    path('purchase/<int:game_id>/', views.purchase_game, name='purchase_game'),
    path('checkout/<int:game_id>/', views.checkout, name='checkout'),
    path('play/<int:game_id>/', views.play_online, name='play_online'),

    # ----------------------
    # PLAYLIST
    # ----------------------
    path('playlist/', views.playlist_detail, name='playlist_detail'),
    path('my-playlist/', views.my_playlist, name='my_playlist'),
    path('add-to-playlist/<int:game_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('remove-from-playlist/<int:game_id>/', views.remove_from_playlist, name='remove_from_playlist'),

    # ----------------------
    # RECEIPT
    # ----------------------
    path('receipt/<int:game_id>/', views.download_receipt, name='download_receipt'),

    # ----------------------
    # SUBSCRIBE
    # ----------------------
    path('subscribe/', views.subscribe, name='subscribe'),

    # ----------------------
    # AUTH
    # ----------------------
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    path('signup/', views.signup, name='signup'),
]