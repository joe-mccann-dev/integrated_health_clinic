from django.core.management.base import BaseCommand
from datetime import time
from appointments.models import TimeTable

class Command(BaseCommand):
  def handle(self, *args, **options):
    interval_range = range(1, 145)
    minutes = 0
    hours = 0
    for n in interval_range:
      t = time(hours, minutes, 0)
      time_str = t.strftime('%H:%M')
      interval_obj = TimeTable(n, time_str)
      interval_obj.save()
      minutes += 10
      if minutes == 60:
        hours += 1
        minutes = 0
        
    self.stdout.write(
      self.style.SUCCESS('Successfully seeded TimeTable with 10 minute intervals')
    )