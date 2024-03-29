# Generated by Django 2.2.6 on 2019-10-03 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('published_date', models.SmallIntegerField()),
                ('page_count', models.SmallIntegerField()),
                ('language', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='IndustryIdentifiersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry_identifiers_type', models.CharField(max_length=16)),
                ('industry_identifiers_id', models.IntegerField()),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='industry', to='Books_manager.BookModel')),
            ],
        ),
        migrations.CreateModel(
            name='ImageLinksModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('small_thumbnail', models.CharField(max_length=128)),
                ('thumbnail', models.CharField(max_length=128)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='Books_manager.BookModel')),
            ],
        ),
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.TextField()),
                ('authors', models.ManyToManyField(to='Books_manager.BookModel')),
            ],
        ),
    ]
