# Generated by Django 2.1.2 on 2018-10-18 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_id', models.CharField(max_length=16)),
                ('title', models.CharField(max_length=64)),
                ('type', models.IntegerField(choices=[(1, '전필'), (2, '전선'), (3, '교양')], default=1)),
                ('professor', models.CharField(max_length=64)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecture.Department')),
            ],
        ),
    ]
