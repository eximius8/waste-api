from django.db import models

class LiteratureSource(models.Model):

    

    name = models.CharField(blank=False, max_length=100, unique=True)
    # тип источника book, article и т.п.
    CHOICES = (        
        ('art', 'Статья'),
        ('gost', 'ГОСТ'),          
    )
    source_type = models.CharField(blank=False,
                                   choices=CHOICES,  
                                   max_length=10, 
                                   default="art")
    
    latexpart = models.TextField(blank=False)

    source_url = models.URLField(blank=True, null=True,
                                 max_length=500, verbose_name="Url cсылка на источник (при наличии)")

    def __str__(self):
        return self.name

    
    class Meta:
        verbose_name = "Литературный источник"
        verbose_name_plural = "Литературные источники"