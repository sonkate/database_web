# Generated by Django 4.1.3 on 2022-12-03 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Average',
            fields=[
                ('ssn_trainee', models.OneToOneField(db_column='SSN_trainee', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='information.mentorvaluatetrainee')),
                ('averagescore', models.IntegerField(blank=True, db_column='AverageScore', null=True)),
                ('voteep2', models.IntegerField(blank=True, db_column='VoteEp2', null=True)),
                ('voteep3', models.IntegerField(blank=True, db_column='VoteEp3', null=True)),
                ('year', models.TextField(db_column='Year')),
                ('voteep4', models.IntegerField(blank=True, db_column='VoteEp4', null=True)),
                ('voteep5', models.IntegerField(blank=True, db_column='VoteEp5', null=True)),
            ],
            options={
                'db_table': 'average',
                'managed': False,
            },
        ),
    ]
