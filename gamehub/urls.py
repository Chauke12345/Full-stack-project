"""
URL configuration for gamehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from games import views


urlpatterns = [

    # =========================
    # 🔧 ADMIN
    # =========================
    path('admin/', admin.site.urls),

    # =========================
    # 🏠 HOME & GAME
    # =========================
    path('', views.home, name='home'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),

    # =========================
    # 💳 PURCHASE & CHECKOUT
    # =========================
    path('purchase/<int:game_id>/', views.purchase_game, name='purchase_game'),
    path('checkout/<int:game_id>/', views.checkout, name='checkout'),
    path('play/<int:game_id>/', views.play_online, name='play_online'),

    # =========================
    # 📃 PLAYLIST
    # =========================
    path('playlist/', views.playlist_detail, name='playlist_detail'),
    path('playlist/add/<int:game_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('playlist/remove/<int:game_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('my-playlist/', views.my_playlist, name='my_playlist'),

    # =========================
    # 🧾 RECEIPTS
    # =========================
    path('receipt/<int:game_id>/', views.download_receipt, name='download_receipt'),

    # =========================
    # ⭐ SUBSCRIBE
    # =========================
    path('subscribe/', views.subscribe, name='subscribe'),

    # =========================
    # 🔐 AUTHENTICATION
    # =========================
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),

    path('signup/', views.signup, name='signup'),

]

# =========================
# 🖼️ MEDIA FILES (DEV ONLY)
# =========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)