from django.urls import path
from .views import DatasetInsightView

urlpatterns = [
    path('insights/', DatasetInsightView.as_view(), name='dataset-insight'),
]