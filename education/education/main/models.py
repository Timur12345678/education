from django.db import models

# Create your models here.

class SiteUser(models.Model):
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    iin = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.last_name+ '' + self.phone