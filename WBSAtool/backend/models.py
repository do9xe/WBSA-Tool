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
    osm_imported = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Timeslot(models.Model):
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    appointment_max = models.IntegerField()
    appointment_count = models.IntegerField(default=0)
    is_full = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date}_{self.time_from}_{self.time_to}"

    def update_count(self):
        self.appointment_count = Appointment.objects.filter(timeslot=self).count()
        if self.appointment_count >= self.appointment_max:
            self.is_full = True
        else:
            self.is_full = False
        self.save()

    def get_percentage(self):
        percentage = 100 / self.appointment_max * self.appointment_count
        return percentage


class Appointment(models.Model):
    is_collected = models.BooleanField(default=False)
    contact_name = models.CharField(max_length=200)
    street = models.ForeignKey('Street',
                               on_delete=models.CASCADE,
                               null=True)
    house_number = models.CharField(max_length=200)
    timeslot = models.ForeignKey('Timeslot',
                                 on_delete=models.CASCADE,
                                 null=True)
    text = models.CharField(max_length=2000,
                            blank=True,
                            default="")
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
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        params = {
            "street": f"{self.street} {self.house_number}",
            "city": "Karlsruhe",
            "postalcode": "76227",
            "format": "jsonv2"
        }
        for i in range(1,5):
            try:
                r = requests.get(url, params=params, headers=headers)
                result = r.json()[0]
                if "lat" in result:
                    self.lat = result['lat']
                    self.lon = result['lon']
                    super(Appointment, self).save(*args, **kwargs)
                    break
                elif i == 5:
                    super(Appointment, self).save(*args, **kwargs)
                    break
            except:
                continue
