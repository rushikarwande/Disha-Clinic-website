from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from appointments.models import TimeSlot
import datetime

class Command(BaseCommand):
    help = 'Creates time slots for the next 30 days'

    def handle(self, *args, **kwargs):
        # Delete existing time slots
        TimeSlot.objects.all().delete()
        
        # Get today's date
        today = timezone.now().date()
        
        # Create time slots for the next 30 days
        for i in range(30):
            current_date = today + timedelta(days=i)
            
            # Skip Sundays
            if current_date.weekday() == 6:  # 6 is Sunday
                continue
            
            # Create time slots from 10 AM to 5 PM in 30-minute intervals
            start_time = datetime.time(10, 0)  # 10:00 AM
            end_time = datetime.time(17, 0)    # 5:00 PM
            
            current_time = start_time
            while current_time < end_time:
                # Calculate end time for this slot (30 minutes later)
                slot_end = datetime.datetime.combine(datetime.date(1, 1, 1), current_time) + timedelta(minutes=30)
                slot_end = slot_end.time()
                
                # Create the time slot
                TimeSlot.objects.create(
                    date=current_date,
                    start_time=current_time,
                    end_time=slot_end,
                    is_available=True
                )
                
                # Move to next 30-minute interval
                current_time = slot_end
        
        self.stdout.write(self.style.SUCCESS('Successfully created time slots')) 