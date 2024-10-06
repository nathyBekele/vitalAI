from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from api.models import AppleHealthStat
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from gpt.generate_ai_response import generate_ai_response


def get_users_with_bad_sleep():
    one_week_ago = timezone.now() - timedelta(days=7)
    users = User.objects.all()
    bad_sleep_users = []

    for user in users[:1]:
        total_sleep = 0

        stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)
        for stat in stats:
            sleep_periods = stat.sleepAnalysis or []
            for period in sleep_periods:
                # print(period.get("sleep_time", 0))
                total_sleep += period.get("sleep_time", 0)

        # print(user.username, total_sleep)
        if total_sleep < 300000:  # 6 hours = 21600 seconds
            bad_sleep_users.append(user)

    return bad_sleep_users


def get_users_with_10k_steps():
    today = timezone.now().date()
    users = User.objects.all()
    step_users = []

    for user in users:
        total_steps_today = AppleHealthStat.objects.filter(
            user=user, created_at__date=today
        ).aggregate(total_steps=Sum('stepCount'))['total_steps'] or 0


        if total_steps_today >= 10000:
            step_users.append(user)

    return step_users



def get_users_with_step_drop():
    today = timezone.now().date()
    this_week_start = today - timedelta(days=today.weekday())  # Start of this week
    last_week_start = this_week_start - timedelta(days=7)      # Start of last week
    last_week_end = this_week_start - timedelta(days=1)        # End of last week

    users = User.objects.all()
    step_drop_users = []

    for user in users:
        this_week_steps = AppleHealthStat.objects.filter(
            user=user, created_at__gte=this_week_start
        ).aggregate(total_steps=Sum('stepCount'))['total_steps'] or 0

        last_week_steps = AppleHealthStat.objects.filter(
            user=user, created_at__range=(last_week_start, last_week_end)
        ).aggregate(total_steps=Sum('stepCount'))['total_steps'] or 0

        if last_week_steps > 0 and this_week_steps < (0.5 * last_week_steps):
            step_drop_users.append(user)

    print("step_drop_users", len(step_drop_users))
    return step_drop_users


class SleepConditionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = get_users_with_bad_sleep()
        responses = []
        one_week_ago = timezone.now() - timedelta(days=7)

        for user in users:
            total_sleep = 0
            days_with_less_than_6_hours = 0

            stats = AppleHealthStat.objects.filter(user=user, created_at__gte=one_week_ago)
            for stat in stats:
                sleep_periods = stat.sleepAnalysis or []
                for period in sleep_periods:
                    sleep_time = period.get("sleep_time", 0)
                    total_sleep += sleep_time
                    if sleep_time < 21600:  # Less than 6 hours
                        days_with_less_than_6_hours += 1

            data = {
                "total_sleep_seconds": total_sleep,
                "total_sleep_hours": total_sleep / 3600,
                "average_sleep_hours": (total_sleep / 3600) / 7,
                "days_with_less_than_6_hours": days_with_less_than_6_hours,
                "analysis": f"You slept less than 6 hours for {days_with_less_than_6_hours} days last week."
            }

            ai_response = generate_ai_response(user, data)

            # print(user.username, ai_response)
            responses.append({"user": user.username, "ai_response": ai_response})

        return Response(responses)


class StepsCondition1View(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = get_users_with_10k_steps()
        responses = []
        today = timezone.now().date()
        yesterday = today - timedelta(days=1)

        # print("Users", len(users))
        for user in users:
            steps_data = AppleHealthStat.objects.filter(
                user=user, created_at__date__in=[today, yesterday]
            ).values('created_at__date').annotate(
                total_steps=Sum('stepCount')
            )

            total_steps_today, total_steps_yesterday = 0, 0

            for data in steps_data:
                if data['created_at__date'] == today:
                    total_steps_today = data['total_steps']
                elif data['created_at__date'] == yesterday:
                    total_steps_yesterday = data['total_steps']

            comparison_to_average = total_steps_today - total_steps_yesterday

            data = {
                "total_steps_today": total_steps_today,
                "comparison_to_average": comparison_to_average,
                "analysis": f"You walked {total_steps_today} steps today, which is {comparison_to_average} steps compared to yesterday."
            }

            ai_response = generate_ai_response(user, data)
            responses.append({"user": user.username, "ai_response": ai_response})

        return Response(responses)


class StepsCondition2View(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = get_users_with_step_drop()
        responses = []
        this_week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())  # Start of this week

        for user in users:
            this_week_steps = AppleHealthStat.objects.filter(
                user=user, created_at__gte=this_week_start
            ).aggregate(total_steps=Sum('stepCount'))['total_steps'] or 0

            last_week_start = this_week_start - timedelta(days=7)
            last_week_end = this_week_start - timedelta(days=1)

            last_week_steps = AppleHealthStat.objects.filter(
                user=user, created_at__range=(last_week_start, last_week_end)
            ).aggregate(total_steps=Sum('stepCount'))['total_steps'] or 0

            percentage_step_drop = (last_week_steps - this_week_steps) / last_week_steps * 100 if last_week_steps else 0

            data = {
                "this_week_steps": this_week_steps,
                "last_week_steps": last_week_steps,
                "percentage_step_drop": percentage_step_drop,
                "analysis": f"Your steps dropped by {percentage_step_drop:.2f}% compared to last week."
            }

            ai_response = generate_ai_response(user, data)
            responses.append({"user": user.username, "ai_response": ai_response})

        return Response(responses)
