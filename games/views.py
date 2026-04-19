from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings

from datetime import datetime
import uuid
import os
import random

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from .models import Game, Playlist, Purchase
from .forms import CustomUserCreationForm
from .utils import generate_receipt_pdf


# ----------------------
# HOME PAGE
# ----------------------
def home(request):
    games = Game.objects.all()
    return render(request, 'games/home.html', {'games': games})


# ----------------------
# GAME DETAIL PAGE
# ----------------------
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    owned = False
    if request.user.is_authenticated:
        owned = Purchase.objects.filter(user=request.user, game=game).exists()

    return render(request, 'games/game_detail.html', {
        'game': game,
        'owned': owned
    })


# ----------------------
# PURCHASE → REDIRECT TO CHECKOUT
# ----------------------
@login_required
def purchase_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if Purchase.objects.filter(user=request.user, game=game).exists():
        messages.info(request, "You already own this game.")
        return redirect('game_detail', game_id=game.id)

    return redirect('checkout', game_id=game.id)


# ----------------------
# CHECKOUT (FAKE PAYMENT + EMAIL)
# ----------------------
@login_required
def checkout(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == "POST":
        card_number = request.POST.get("card_number")

        if len(card_number) < 12:
            messages.error(request, "Invalid card number")
            return redirect('checkout', game_id=game.id)

        # Fake success
        if random.randint(1, 10) <= 9:

            Purchase.objects.create(user=request.user, game=game)

            playlist, _ = Playlist.objects.get_or_create(user=request.user)
            playlist.games.add(game)

            # 📧 Send receipt email
            if request.user.email:
                pdf = generate_receipt_pdf(request.user, game)

                email = EmailMessage(
                    subject="Your Game Receipt 🎮",
                    body=f"Hi {request.user.username},\n\nThanks for your purchase!",
                    to=[request.user.email],
                )
                email.attach(f"receipt_{game.id}.pdf", pdf, 'application/pdf')
                email.send()

            messages.success(request, "Payment successful! Receipt sent 🎉")
            return redirect('game_detail', game_id=game.id)

        else:
            messages.error(request, "Payment failed. Try again.")

    return render(request, "games/checkout.html", {"game": game})


# ----------------------
# PLAY ONLINE
# ----------------------
@login_required
def play_online(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    owned = Purchase.objects.filter(user=request.user, game=game).exists()

    if not owned:
        messages.error(request, "You must purchase this game first.")
        return redirect('game_detail', game_id=game.id)

    return redirect(game.play_url)


# ----------------------
# PLAYLIST
# ----------------------
@login_required
def playlist_detail(request):
    playlist, _ = Playlist.objects.get_or_create(user=request.user)
    return render(request, "games/playlist_detail.html", {"playlist": playlist})


@login_required
@require_POST
def add_to_playlist(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    playlist, _ = Playlist.objects.get_or_create(user=request.user)

    owned = Purchase.objects.filter(user=request.user, game=game).exists()

    if not owned:
        messages.error(request, "You must purchase this game first.")
        return redirect("game_detail", game_id=game.id)

    playlist.games.add(game)
    messages.success(request, "Added to playlist!")

    return redirect("playlist_detail")


@login_required
@require_POST
def remove_from_playlist(request, game_id):
    playlist, _ = Playlist.objects.get_or_create(user=request.user)
    game = get_object_or_404(Game, id=game_id)

    playlist.games.remove(game)
    messages.success(request, "Removed from playlist")

    return redirect("playlist_detail")


@login_required
def my_playlist(request):
    return redirect('playlist_detail')


# ----------------------
# SIGNUP (WITH EMAIL)
# ----------------------
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()   # ✅ saves user to DB
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()

    # ✅ THIS WAS MISSING
    return render(request, 'registration/signup.html', {'form': form})




# ----------------------
# SUBSCRIBE
# ----------------------
def subscribe(request):
    request.session['subscribed'] = True
    messages.success(request, "Subscription activated!")
    return redirect('home')


# ----------------------
# DOWNLOAD RECEIPT (PDF)
# ----------------------
@login_required
def download_receipt(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if not Purchase.objects.filter(user=request.user, game=game).exists():
        messages.error(request, "You don't own this game.")
        return redirect('game_detail', game_id=game.id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{game.id}.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()

    transaction_id = str(uuid.uuid4())[:10].upper()
    elements = []

    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'static/images/logo.png')
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=2*inch, height=1*inch))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("<b>GAME STORE RECEIPT</b>", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"User: {request.user.username}", styles['Normal']))
    elements.append(Paragraph(f"Date: {datetime.now()}", styles['Normal']))
    elements.append(Paragraph(f"Transaction ID: {transaction_id}", styles['Normal']))

    elements.append(Spacer(1, 20))

    table = Table([
        ["Item", "Price"],
        [game.title, f"${game.price}"]
    ])

    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Total: ${game.price}", styles['Heading2']))

    doc.build(elements)
    return response

