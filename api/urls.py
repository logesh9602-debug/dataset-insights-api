from django.urls import path
from .views import DatasetInsightsView

urlpatterns = [
    path('insights/', DatasetInsightsView.as_view(), name='dataset-insights'),
]