from django.db import models
import requests


class Area(models.Model):
    name = models.CharField(max_length=200)
    is_parent = models.BooleanField(default=False)
    parent = models.ForeignKey('Area',
                               limit_choices_to={'is_parent': True},
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=200)
    area = models.ForeignKey('Area',
                             limit_choices_to={'is_parent': False},
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)

    def __str__(self):
        return self.name


class Timeslot(models.Model):
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()

    def __str__(self):
        return f"{self.date}_{self.time_from}_{self.time_to}"


class Appointment(models.Model):
    contact_name = models.CharField(max_length=200)
    street = models.ForeignKey('Street',
                               on_delete=models.CASCADE,
                               null=True)
    house_number = models.CharField(max_length=200)
    timeslot = models.ForeignKey('Timeslot',
                                 on_delete=models.CASCADE,
                                 null=True)
    text = models.CharField(max_length=200,
                            null=True,
                            blank=True)
    phone = models.CharField(max_length=200,
                             null=True,
                             blank=True)
    email = models.CharField(max_length=200,
                             null=True,
                             blank=True)
    lat = models.CharField(max_length=200,
                             null=True,
                             blank=True)
    lon = models.CharField(max_length=200,
                             null=True,
                             blank=True)

    def __str__(self):
        return f"{self.contact_name}, {self.street.name} {self.house_number}"

    def save(self, *args, **kwargs):
        if (self.lat == None) or (self.lon == None):
            url = "https://nominatim.openstreetmap.org/search.php"
            params = {
                "street": f"{self.street} {self.house_number}",
                "city": "Karlsruhe",
                "postalcode": "76227",
                "format": "jsonv2"
            }
            r = requests.get(url, params=params)
            result = r.json()[0]
            self.lat = result['lat']
            self.lon = result['lon']
        super(Appointment, self).save(*args, **kwargs)
