from django.db import models

# Create your models here.


def get_airplane_image_folder(instance, filename):
    return "%s/%s" % (instance.id, filename)

class Aircraft(models.Model):
    tail_number = models.CharField(max_length=100, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True)
    aircraft_type = models.CharField(max_length=100, null=True, blank=True)
    # set this to be int, coz the only format for date is Year.
    year_of_production = models.IntegerField(null=True, blank=True)
    images = models.CharField(max_length=1000, null=True, blank=True)
    aircraft_class = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    company_phone = models.CharField(max_length=30, null=True, blank=True)
    company_website = models.CharField(max_length=100, null=True, blank=True)
    ICAO = models.CharField(max_length=10, null=True, blank=True)
    IATA = models.CharField(max_length=10, null=True, blank=True)
    airport_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.serial_number

    class Meta:
        ordering = ['-id']