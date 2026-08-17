from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0171_jira_labels_per_product_and_engagement'),
    ]

    operations = [
        migrations.AddField(
            model_name='jira_instance',
            name='restricted_releases',
            field=models.CharField(blank=True, help_text="Comma-separated list of Domino release values (e.g. R2024.3,R2024.4) to show in the JIRA finding-group release table. Leave empty to show every release found on the group's findings.", max_length=2000, null=True, verbose_name='Restricted Releases'),
        ),
    ]
