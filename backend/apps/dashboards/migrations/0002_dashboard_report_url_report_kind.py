from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("dashboards", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboard",
            name="report_url",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="dashboard",
            name="report_kind",
            field=models.CharField(
                choices=[
                    ("QLIK", "Qlik Sense"),
                    ("WEB", "Web app"),
                    ("BOT", "Telegram bot"),
                ],
                default="QLIK",
                max_length=20,
            ),
        ),
    ]
