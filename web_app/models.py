from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=150, blank=False)
    likes = models.PositiveIntegerField(default=0)
    video = models.FileField(upload_to="videos/", null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name="liked")

    def __str__(self):
        return f"{self.title} (uploaded by {self.user.username})"

    @property
    def num_of_likes(self):
        return self.liked.all().count()