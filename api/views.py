import pandas as pd
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Dataset
from .serializers import DatasetSerializer

class DatasetViewSet(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

    def perform_create(self, serializer):
        dataset_instance = serializer.save()
        file_path = dataset_instance.file.path

        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith(('.xls', '.xlsx')):
                df = pd.read_excel(file_path)
            else:
                return

            # Compute dataset insights
            summary = {
                "total_rows": int(df.shape[0]),
                "total_columns": int(df.shape[1]),
                "duplicate_rows": int(df.duplicated().sum()),
                "columns": list(df.columns),
                "data_types": {col: str(dtype) for col, dtype in df.dtypes.to_dict().items()},
                "missing_values": df.isnull().sum().to_dict(),
                "summary_statistics": df.describe().to_dict()
            }

            dataset_instance.summary_stats = summary
            dataset_instance.save()

        except Exception as e:
            dataset_instance.summary_stats = {"error": f"Failed to analyze file: {str(e)}"}
            dataset_instance.save()