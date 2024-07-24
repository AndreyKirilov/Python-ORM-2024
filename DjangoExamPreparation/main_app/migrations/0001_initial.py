# Generated by Django 5.0.4 on 2024-07-22 10:56

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_banned', models.BooleanField(default=False)),
                ('birth_year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2005)])),
                ('website', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(10)])),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(5)])),
                ('category', models.CharField(choices=[('T', 'Technology'), ('S', 'Science'), ('E', 'Education')], default='Technology', max_length=10)),
                ('authors', models.ManyToManyField(to='main_app.author')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(validators=[django.core.validators.MinLengthValidator(10)])),
                ('published_on', models.DateTimeField(auto_now_add=True)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.article')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.author')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
