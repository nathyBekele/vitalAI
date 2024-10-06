from django.db import models
from django.contrib.auth import get_user_model

class AppleHealthStat(models.Model):  # Removed the TimestampedModel for simplicity, but you can add it back if needed
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='apple_health_stat')
    dateOfBirth = models.DateTimeField(null=True, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    bodyMass = models.PositiveSmallIntegerField(null=True, blank=True)
    bodyFatPercentage = models.PositiveSmallIntegerField(null=True, blank=True)
    biologicalSex = models.CharField(max_length=32, null=True, blank=True)
    activityMoveMode = models.CharField(max_length=128, null=True, blank=True)
    stepCount = models.PositiveSmallIntegerField(null=True, blank=True)
    basalEnergyBurned = models.PositiveSmallIntegerField(null=True, blank=True)
    activeEnergyBurned = models.PositiveSmallIntegerField(null=True, blank=True)
    flightsClimbed = models.PositiveSmallIntegerField(null=True, blank=True)
    appleExerciseTime = models.PositiveSmallIntegerField(null=True, blank=True)
    appleMoveTime = models.PositiveSmallIntegerField(null=True, blank=True)
    appleStandHour = models.PositiveSmallIntegerField(null=True, blank=True)
    menstrualFlow = models.CharField(max_length=128, null=True, blank=True)
    HKWorkoutTypeIdentifier = models.CharField(max_length=128, null=True, blank=True)
    heartRate = models.PositiveSmallIntegerField(null=True, blank=True)
    oxygenSaturation = models.PositiveSmallIntegerField(null=True, blank=True)
    mindfulSession = models.JSONField(null=True, blank=True)
    sleepAnalysis = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
