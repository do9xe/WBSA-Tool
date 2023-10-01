from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


def group_exists(group_name):
    x = Group.objects.filter(name=group_name).count()
    if x == 0:
        return False
    else:
        return True


class Command(BaseCommand):
    help = "Populate the WBSA-Tool database with the default groups for permissions"

    default_group_list = [
        {"name": "Frontend-Admin",
         "permissions": [
             "view_area",
             "view_street",
             "view_timeslot",
             "view_appointment",
             "add_area",
             "add_street",
             "add_timeslot",
             "add_appointment",
             "change_area",
             "change_street",
             "change_timeslot",
             "change_appointment",
             "delete_area",
             "delete_street",
             "delete_timeslot",
             "delete_appointment",
         ]},
        {"name": "Telefonisten",
         "permissions": [
             "view_area",
             "view_street",
             "view_timeslot",
             "view_appointment",
             "add_appointment",
             "add_street",
             "change_appointment",
             "delete_appointment",
         ]},
        {"name": "Fahrzeugführer",
         "permissions": [
             "view_appointment",
             "change_appointment"
         ]},
        {"name": "ReadOnly",
         "permissions": [
             "view_area",
             "view_street",
             "view_timeslot",
             "view_appointment"
         ]},
    ]

    def handle(self, *args, **options):
        self.stdout.write("Beginne das Hinzufügen der Gruppen")

        for default_group in self.default_group_list:
            self.stdout.write(f"Generiere Gruppe {default_group['name']}")
            if not group_exists(default_group['name']):
                NewGroup = Group(name=default_group['name'])
                NewGroup.save()
                for perm in default_group['permissions']:
                    perm = Permission.objects.get(codename=perm).id
                    NewGroup.permissions.add(perm)
                NewGroup.save()
            else:
                self.stdout.write(f"Gruppe {default_group['name']} existiert bereits")

        self.stdout.write("Alle Gruppen erfolgreich hinzugefügt")
