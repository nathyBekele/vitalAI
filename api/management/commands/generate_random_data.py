import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import AppleHealthStat
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate random users and health data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        for i in range(10): 
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='12345678', 
                    email=f'user{i}@example.com'
                )
                self.stdout.write(self.style.SUCCESS(f'Created user {user.username}'))

        users = User.objects.all()  

        for user in users:
            AppleHealthStat.objects.create(
                user=user,
                date_of_birth=timezone.make_aware(datetime(1989, 8, 1)),  
                height=random.randint(150, 200),
                body_mass=random.randint(50, 100),
                body_fat_percentage=random.randint(15, 30),
                biological_sex=random.choice(["male", "female"]),
                activity_move_mode=random.choice(["activeEnergy", "sedentary"]),
                step_count=random.randint(1000, 15000),
                basal_energy_burned=random.randint(500, 2000),
                active_energy_burned=random.randint(100, 1000),
                flights_climbed=random.randint(0, 10),
                apple_exercise_time=random.randint(0, 120),
                apple_move_time=random.randint(0, 120),
                apple_stand_hour=random.randint(0, 12),
                heart_rate=random.randint(50, 120),
                oxygen_saturation=random.randint(95, 100),
                sleep_analysis=[
                    {
                        "date": (timezone.now() - timedelta(days=j)).strftime("%Y-%m-%d %H:%M"),
                        "sleep_time": random.randint(1800, 28800)  
                    } for j in range(7)
                ]
            )

        self.stdout.write(self.style.SUCCESS('Successfully created random health data for users.'))
