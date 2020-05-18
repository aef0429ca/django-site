from django.db import models
from django.contrib.auth.models import User

FORMAT_CHOICES = (("UNKNOWN","UNKNOWN"),
                  ("ZAP", "ZAP"),
                  ("GAIA", "GAIA"),
                  ("LOPES", "LOPES"),
)


class Document(models.Model):
    # format_guess should be a session var only kept for a short while. Not stored in db.
    # format_valid should be the validated format, if successfully validated 
    document = models.FileField(upload_to='documents')
    file_name = models.CharField(max_length=24, blank=True)
    profile_file = models.CharField(max_length=60, blank=True)
    format_guess = models.CharField(max_length = 10, choices=FORMAT_CHOICES, default="0", blank=False)
    format_valid = models.CharField(max_length = 10, default="INVALID", blank=False)
    url = models.CharField(max_length=300, default='')
    # user = models.IntegerField(default=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
