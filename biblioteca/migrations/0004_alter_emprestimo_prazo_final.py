# Generated by Django 5.2.4 on 2025-07-19 06:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biblioteca', '0003_remove_emprestimo_data_devolucao_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprestimo',
            name='prazo_final',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 18, 6, 11, 25, 460795, tzinfo=datetime.timezone.utc)),
        ),
    ]
