import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DatasetInsightsView(APIView):
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response(
                {"error": "No file uploaded."},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.FILES['file']

        if not (file_obj.name.endswith('.csv') or file_obj.name.endswith('.xlsx')):
            return Response(
                {"error": "Unsupported file format. Please upload a .csv or .xlsx file."},
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

            summary = {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "missing_values": df.isnull().sum().to_dict(),
            }
            return Response(summary, status=status.HTTP_200_OK)

        except pd.errors.EmptyDataError:
            return Response(
                {"error": "The uploaded dataset is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred while processing the file: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )