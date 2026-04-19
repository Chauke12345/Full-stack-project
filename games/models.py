from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


# ----------------------
# GAME MODEL
# ----------------------
class Game(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    description = models.TextField()

    # ✅ FIX: allow empty images (prevents crashes)
    image = models.ImageField(upload_to='games/', blank=True, null=True)

    preview_video = models.URLField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    play_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def is_free(self):
        return self.price == 0

    # ✅ NEW: cleaner ownership check (used in views)
    def is_owned_by(self, user):
        if user.is_authenticated:
            return self.purchases.filter(user=user).exists()
        return False


# ----------------------
# PLAYLIST (ONE PER USER)
# ----------------------
class Playlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='playlist'
    )
    games = models.ManyToManyField(
        Game,
        blank=True,
        related_name='playlists'
    )

    # ✅ FIX: proper display
    def __str__(self):
        return f"{self.user.username}'s Playlist"


# ----------------------
# PURCHASE MODEL
# ----------------------
class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'game'],
                name='unique_user_game_purchase'
            )
        ]
        ordering = ['-purchased_at']

    # ✅ FIX: cleaner output
    def __str__(self):
        return f"{self.user.username} purchased {self.game.title}"


# ----------------------
# SUBSCRIPTION MODEL
# ----------------------
class Subscription(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    is_active = models.BooleanField(default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def activate(self, duration_days=30):
        self.is_active = True
        self.start_date = timezone.now()
        self.end_date = self.start_date + timedelta(days=duration_days)
        self.save()

    def has_expired(self):
        return self.end_date and timezone.now() > self.end_date

    def is_valid(self):
        return self.is_active and not self.has_expired()

    # ✅ NEW: use in views to unlock games
    def can_access_game(self, game):
        return self.is_valid() or game.price == 0

    def __str__(self):
        return f"{self.user.username}'s Subscription"