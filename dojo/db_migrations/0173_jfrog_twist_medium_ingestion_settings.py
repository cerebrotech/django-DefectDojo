from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0172_jira_instance_restricted_releases'),
    ]

    operations = [
        migrations.AddField(
            model_name='system_settings',
            name='enable_jfrog_twist_medium_ingestion',
            field=models.BooleanField(default=False, help_text="With this setting turned on, the 'Jfrog-Twist cli Domino Image Scan' parser will ingest Medium severity, fix-available findings for a container when the count of distinct Medium CVEs with a fix available exceeds the threshold below. When off, Medium findings are never ingested for this scan type, regardless of the threshold.", verbose_name='Enable Jfrog-Twist Medium ingestion'),
        ),
        migrations.AddField(
            model_name='system_settings',
            name='jfrog_twist_medium_unique_cve_threshold',
            field=models.IntegerField(blank=True, default=12, help_text="Only used when 'Enable Jfrog-Twist Medium ingestion' is on. A container's Medium severity, fix-available findings are only ingested if the count of distinct CVEs among them exceeds this number.", null=True, verbose_name='Jfrog-Twist Medium unique CVE threshold'),
        ),
    ]
