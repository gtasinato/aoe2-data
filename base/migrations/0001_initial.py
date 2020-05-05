# Generated by Django 3.0.5 on 2020-04-27 17:00

from django.db import migrations, models
import picklefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Player name', max_length=50)),
                ('steam_id', models.IntegerField(help_text='Steam id')),
                ('elo', picklefield.fields.PickledObjectField(editable=False, help_text='Dictionary with Elos')),
                ('rank', picklefield.fields.PickledObjectField(editable=False, help_text='Dictionary with ranking')),
            ],
        ),
    ]
