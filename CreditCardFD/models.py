
from django.db import models
class upload1(models.Model):
    file_name=models.CharField(max_length=100)
    uploadfile=models.FileField(upload_to='media/',null=True)
    description=models.TextField(max_length=200,null=True)
    class Meta:
        app_label = 'CreditCardFD'
        db_table = "CreditCardFD_upload1"
    def __str__(self):
        return self.file_name
    def save(self, *args, **kwargs):
        super().save()
    objects = models.Manager()