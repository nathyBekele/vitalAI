import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import AppleHealthStat
from django.utils import timezone
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate or update random users and health data'

    def handle(self, *args, **kwargs):
        User = get_user_model()

        for i in range(20): 
            username = f'user{i}'

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': '12345678',
                    'email': f'user{i}@example.com'
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created user {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Updated user {user.username}'))

        users = User.objects.all()  

        for user in users:
            health_stat, created = AppleHealthStat.objects.get_or_create(
                user=user,
                defaults={
                    'dateOfBirth': datetime(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28)),
                    'height': random.randint(150, 200),
                    'bodyMass': random.randint(50, 100),
                    'bodyFatPercentage': random.randint(15, 30),
                    'biologicalSex': random.choice(["male", "female"]),
                    'activityMoveMode': random.choice(["activeEnergy", "sedentary"]),
                    'stepCount': random.randint(5000, 15000),
                    'basalEnergyBurned': random.randint(500, 2000),
                    'activeEnergyBurned': random.randint(100, 1000),
                    'flightsClimbed': random.randint(0, 10),
                    'appleExerciseTime': random.randint(0, 120),
                    'appleMoveTime': random.randint(0, 120),
                    'appleStandHour': random.randint(0, 12),
                    'menstrualFlow': random.choice(["unspecified", None]),
                    'HKWorkoutTypeIdentifier': random.choice([None, "HKWorkoutTypeIdentifier"]),
                    'heartRate': random.randint(50, 120),
                    'oxygenSaturation': random.randint(95, 100),
                    'mindfulSession': {},
                    'sleepAnalysis': [
                        {
                            "date": (timezone.now() - timedelta(days=j)).strftime("%Y-%m-%d %H:%M"),
                            "sleep_time": random.randint(1800, 28800)
                        }
                        for j in range(30)
                    ],
                    'created_at': timezone.now().replace(tzinfo=None) 
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created health data for {user.username}'))
            else:
                health_stat.dateOfBirth = datetime(random.randint(1970, 2000), random.randint(1, 12), random.randint(1, 28))
                health_stat.height = random.randint(150, 200)
                health_stat.bodyMass = random.randint(50, 100)
                health_stat.bodyFatPercentage = random.randint(15, 30)
                health_stat.biologicalSex = random.choice(["male", "female"])
                health_stat.activityMoveMode = random.choice(["activeEnergy", "sedentary"])
                health_stat.stepCount = random.randint(5000, 15000)
                health_stat.basalEnergyBurned = random.randint(500, 2000)
                health_stat.activeEnergyBurned = random.randint(100, 1000)
                health_stat.flightsClimbed = random.randint(0, 10)
                health_stat.appleExerciseTime = random.randint(0, 120)
                health_stat.appleMoveTime = random.randint(0, 120)
                health_stat.appleStandHour = random.randint(0, 12)
                health_stat.menstrualFlow = random.choice(["unspecified", None])
                health_stat.HKWorkoutTypeIdentifier = random.choice([None, "HKWorkoutTypeIdentifier"])
                health_stat.heartRate = random.randint(50, 120)
                health_stat.oxygenSaturation = random.randint(95, 100)
                health_stat.mindfulSession = {}
                health_stat.sleepAnalysis = [
                    {
                        "date": (timezone.now() - timedelta(days=j)).strftime("%Y-%m-%d %H:%M"),
                        "sleep_time": random.randint(1800, 28800)
                    }
                    for j in range(30)
                ]
                health_stat.updated_at = timezone.now().replace(tzinfo=None)  
                health_stat.save()  
                self.stdout.write(self.style.WARNING(f'Updated health data for {user.username}'))

        self.stdout.write(self.style.SUCCESS('Successfully created or updated health data for users.'))
