from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ConversationHistory(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user", null=True, blank = True)
    token = models.CharField(max_length = 64, unique = True)
    content = models.JSONField()
    summary_text = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null = True, blank = True)