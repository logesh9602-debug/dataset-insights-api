from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd

class DatasetInsightView(APIView):
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response(
                {"error": "No file uploaded. Please upload a valid CSV or Excel file."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not (file_obj.name.endswith('.csv') or file_obj.name.endswith('.xlsx')):
            return Response(
                {"error": "Unsupported file format. Only .csv and .xlsx files are allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            if file_obj.name.endswith('.csv'):
                df = pd.read_csv(file_obj)
            else:
                df = pd.read_excel(file_obj)

            if df.empty:
                return Response(
                    {"error": "The uploaded dataset is empty."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            insights = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
                "summary": df.describe(include='all').fillna('').to_dict()
            }
            return Response(insights, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Failed to process file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )