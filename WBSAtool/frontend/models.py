from django.db import models


# Create your models here.


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
    area = models.ForeignKey('Area',
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True)

    def __str__(self):
        return f"{self.date}_{self.time_from}"


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
                            null=True)
    phone = models.CharField(max_length=200,
                             null=True)
    email = models.CharField(max_length=200,
                             null=True)

    def __str__(self):
        return f"{self.contact_name}_{self.street.name}_{self.house_number}"
