from django.db import models

class Dataset(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary_stats = models.JSONField(blank=True, null=True)

    def test_model_str(self):
        """Test model string representation if DatasetUpload exists."""
        from api.models import DatasetUpload
        upload = DatasetUpload.objects.create(file_name="sample.csv")
        self.assertEqual(str(upload), "sample.csv")