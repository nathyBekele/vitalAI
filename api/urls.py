from django.urls import path
from .views import SleepConditionView, StepsCondition1View, StepsCondition2View

urlpatterns = [
    path('sleep-condition/', SleepConditionView.as_view(), name='sleep-condition'),
    path('steps-condition-1/', StepsCondition1View.as_view(), name='steps-condition-1'),
    path('steps-condition-2/', StepsCondition2View.as_view(), name='steps-condition-2'),
]

