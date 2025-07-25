from django.db import models
from django.utils import timezone

class OTP(models.Model):
    email=models.EmailField()
    code=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)

    def is_valid(self):
        return timezone.now()-self.created_at<timezone.timedelta(minutes=5)