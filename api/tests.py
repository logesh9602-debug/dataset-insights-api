import io
import pandas as pd
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class DatasetInsightTests(APITestCase):

    def setUp(self):
        self.url = reverse('dataset-insight')

    def test_upload_valid_csv(self):
        """Test uploading a valid CSV dataset."""
        csv_data = "name,age,score\nAlice,24,88\nBob,30,95"
        file = io.BytesIO(csv_data.encode('utf-8'))
        file.name = 'test.csv'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['row_count'], 2)
        self.assertIn('age', response.data['columns'])

    def test_upload_invalid_file_type(self):
        """Test uploading an unsupported file format."""
        file = io.BytesIO(b"dummy text data")
        file.name = 'test.txt'

        response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_no_file(self):
        """Test sending POST request without a file."""
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)