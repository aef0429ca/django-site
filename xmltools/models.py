from django.db import models

FORMAT_CHOICES = (("UNKNOWN","UNKNOWN"),
                  ("ZAP", "ZAP"),
                  ("GAIA", "GAIA"),
                  ("LOPES", "LOPES"),
)


class Document(models.Model):
    document = models.FileField(upload_to='documents')
    file_name = models.CharField(max_length=24, blank=True)
    profile_file = models.CharField(max_length=30, blank=True)
    format_guess = models.CharField(max_length = 10, choices=FORMAT_CHOICES, default="0", blank=False)
    url = models.CharField(max_length=300, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
