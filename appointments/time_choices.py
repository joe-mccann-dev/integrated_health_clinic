from datetime import timedelta

# represent availability blocks with starting interval id
# and ending interval id
# TIME_CHOICES = [
#   (1, '00:00:00'),
#   (2, '00:00:10'),
#   etc...
# ]
TIME_CHOICES = [(i + 1, str(timedelta(minutes=i * 10))) for i in range(144)]
