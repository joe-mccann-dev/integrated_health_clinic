from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
  help = 'Seeds the database with fixture data'

  def handle(self, *args, **options):
    self.stdout.write(self.style.SUCCESS("Initializing database seeding..."))

    try:
      call_command("seed_time_table")
      self.stdout.write(self.style.SUCCESS("Time Table seeded successfully."))

      call_command("loaddata", "seed_practitioners")
      self.stdout.write(self.style.SUCCESS('Practitioner table seeded successfully.'))

      call_command("loaddata", "seed_patients")
      self.stdout.write(self.style.SUCCESS("Patient table seeded successfully."))

      call_command("loaddata", "seed_appointments")
      self.stdout.write(self.style.SUCCESS("Appointment table seeded successfully."))

      self.stdout.write(self.style.SUCCESS("Successfully seeded database."))

      self.stdout.write(self.style.NOTICE("Creating superuser to use admin dashboard"))
      call_command("createsuperuser")
      
    except Exception as e:
      self.stdout.write(self.style.ERROR(f"Error during database seeding: {e}"))