from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0173_jfrog_twist_medium_ingestion_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_settings',
            name='jfrog_twist_medium_s3_bucket',
            field=models.CharField(blank=True, default='', help_text='Existing S3 bucket containing the list of container substrings excluded from Medium ingestion.', max_length=255, verbose_name='Jfrog-Twist Medium exclusion list S3 bucket'),
        ),
        migrations.AddField(
            model_name='system_settings',
            name='jfrog_twist_medium_s3_key',
            field=models.CharField(blank=True, default='', help_text='Object key of a UTF-8 file with one excluded container substring per line.', max_length=1024, verbose_name='Jfrog-Twist Medium exclusion list S3 key'),
        ),
    ]
