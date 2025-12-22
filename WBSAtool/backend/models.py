import requests
from time import sleep
from django.db import models

from backend import logger
from WBSAtool.settings import NOMINATIM_URL

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

    def get_timeslots(self):
        if not self.is_parent:
            return []
        logger.error(f"Area {self.name} has no parent, returning empty Timeslot List")
        list = []
        for ts in Timeslot.objects.order_by("date", "time_from"):
            list.append({"area": self,
                "timeslot":ts,
                "appointment_max":ts.appointment_max,
                "count":ts.get_count_per_area(self.id),
                "percentage":ts.get_percentage_per_area(self.id)})
        return list


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

    def __str__(self):
        return f"{self.date}_{self.time_from}_{self.time_to}"

    def get_count_per_area(self, area_id):
        qs = Appointment.objects.filter(timeslot=self, street__area__parent_id=area_id, area__isnull=True)
        overwrites = Appointment.objects.filter(timeslot=self, area_id=area_id)
        count = (qs | overwrites).count()
        return count

    def get_percentage_per_area(self, area_id):
        percentage = 100 / self.appointment_max * self.get_count_per_area(area_id)
        return percentage

    def get_all_percentage(self):
        list = []
        for area in Area.objects.filter(is_parent=True):
            list.append({"id":area.id, "name":area.name,
                         "percentage":self.get_percentage_per_area(area.id),
                         "count":self.get_count_per_area(area.id)})
        return list


class Appointment(models.Model):
    is_collected = models.BooleanField(default=False)
    area = models.ForeignKey('Area',
                             default=None,
                             on_delete=models.SET_NULL,
                             null=True)
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
                             blank=True)
    email = models.CharField(max_length=200,
                             blank=True),
    lat = models.CharField(max_length=200,
                             blank=True)
    lon = models.CharField(max_length=200,
                             blank=True)

    def __str__(self):
        return f"{self.contact_name}, {self.street.name} {self.house_number}"

    def save(self, *args, **kwargs):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"}
        params = {
            "street": f"{self.street} {self.house_number}",
            "city": "Karlsruhe",
            "postalcode": "76227",
            "format": "jsonv2"
        }
        for i in range(1,5):
            try:
                r = requests.get(NOMINATIM_URL, params=params, headers=headers)
                if r.status_code != 200:
                    logger.error(f"encountered Error {r.status_code} while getting data from nominatim")
                    logger.error(r.text)
                    break
                result = r.json()[0]
                if "lat" in result:
                    self.lat = result['lat']
                    self.lon = result['lon']
                    break
                else:
                    logger.info(f"No latitude data in Response, trying again")
                    sleep(1)
            except Exception as e:
                logger.error(e, stack_info=True)
                sleep(1)
        super(Appointment, self).save(*args, **kwargs)