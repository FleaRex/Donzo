# Generated by Django 2.2.7 on 2019-11-30 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jeerer_app', '0006_boardmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardmodel',
            name='board',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='jeerer_app.BoardModel'),
            preserve_default=False,
        ),
    ]
