# Generated by Django 2.2.7 on 2019-11-30 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jeerer_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardmodel',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jeerer_app.CardModel'),
        ),
    ]