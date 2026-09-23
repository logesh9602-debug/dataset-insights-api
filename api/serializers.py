import os
from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'name', 'file', 'uploaded_at', 'summary_stats']
        read_only_fields = ['summary_stats']

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.csv', '.xls', '.xlsx']
        if ext not in valid_extensions:
            raise serializers.ValidationError("Unsupported file extension. Only .csv, .xls, and .xlsx files are allowed.")
        return value