from django.db import models

# Create your models here.
class xDPI_upload_history(models.Model):
	file_name = models.CharField(max_length=100)
	upload_date = models.DateTimeField(blank=True, null=True)
	file_size = models.BigIntegerField(default=0)
	
	class Meta:
		managed = True
		db_table = 'xDPI_upload_history'