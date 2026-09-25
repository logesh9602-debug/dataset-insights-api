import io
from unittest.mock import patch
import pandas as pd
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DatasetInsightsTests(APITestCase):
    def setUp(self):
        self.url = reverse('dataset-insights')

    def test_upload_valid_csv(self):
        """Test uploading a valid CSV file."""
        csv_data = "col1,col2\n1,2\n3,4"
        file = io.BytesIO(csv_data.encode('utf-8'))
        file.name = 'sample.csv'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('row_count', response.data)

    def test_upload_valid_excel(self):
        """Test uploading a valid Excel file."""
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)
        excel_file.name = 'sample.xlsx'

        response = self.client.post(self.url, {'file': excel_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_no_file(self):
        """Test sending a POST request with no file attached."""
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_invalid_file_format(self):
        """Test uploading an unsupported file format."""
        file = io.BytesIO(b"dummy text data")
        file.name = 'sample.txt'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_empty_csv(self):
        """Test uploading an empty CSV file."""
        file = io.BytesIO(b"")
        file.name = 'empty.csv'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('pandas.read_csv')
    def test_upload_internal_server_error(self, mock_read_csv):
        """Test exception handling when parsing fails unexpectedly."""
        mock_read_csv.side_effect = Exception("Simulated parsing error")
        file = io.BytesIO(b"col1,col2\n1,2")
        file.name = 'error.csv'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @patch('pandas.read_excel')
    def test_upload_excel_internal_server_error(self, mock_read_excel):
        """Test generic exception branch during Excel processing."""
        mock_read_excel.side_effect = Exception("Unexpected Excel processing failure")
        
        # Create a dummy excel file input
        file = io.BytesIO(b"dummy excel content")
        file.name = 'sample.xlsx'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)    