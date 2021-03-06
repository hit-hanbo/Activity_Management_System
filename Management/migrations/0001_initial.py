# Generated by Django 2.1 on 2018-09-01 15:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('group', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MyActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mytime', models.IntegerField(max_length=20)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Management.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_zh', models.CharField(max_length=20)),
                ('stu_id', models.CharField(max_length=20, unique=True)),
                ('phone_num', models.CharField(max_length=20)),
                ('time_volunteer', models.IntegerField()),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='myactivity',
            name='person',
            field=models.ManyToManyField(to='Management.Volunteer'),
        ),
    ]
