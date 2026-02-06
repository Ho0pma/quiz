import os
from django.db import models
from django.contrib.auth.models import User


def card_photo_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1] or '.jpg'
    if instance.collection_id:
        username = instance.collection.user.username
        collection_name = instance.collection.name.replace('/', '_').replace('\\', '_').strip() or 'collection'
        n = instance.collection.cards.exclude(photo='').count() + 1
    else:
        username = 'unknown'
        collection_name = 'collection'
        n = 1
    return f'cards/{username}/{collection_name}/{n:04d}{ext}'


class Collection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Card(models.Model):
    question = models.TextField()
    photo = models.ImageField(upload_to=card_photo_upload_to, blank=True, null=True)
    answer = models.TextField()
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='cards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]
