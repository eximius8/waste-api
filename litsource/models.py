from django.db import models

class LiteratureSource(models.Model):

    name = models.CharField(blank=False, max_length=100, unique=True)
    
    latexpart = models.TextField(blank=False)

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Литературный источник"
        verbose_name_plural = "Литературные источники"