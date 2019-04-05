from django.db import models

class PdfFile(models.Model):
    file = models.FileField(upload_to="media/")
