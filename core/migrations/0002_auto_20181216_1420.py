# Generated by Django 2.1.3 on 2018-12-16 06:20

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FragmentTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Slug')),
                ('idf', models.DecimalField(decimal_places=16, default=0, max_digits=32)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='FragmentTagM2M',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField(db_index=True, verbose_name='Object id')),
                ('tf', models.DecimalField(decimal_places=16, default=0, max_digits=32)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='core_fragmenttagm2m_tagged_items', to='contenttypes.ContentType', verbose_name='Content type')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='m2m_fragments', to='core.FragmentTag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='requestfragment',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='core.FragmentTagM2M', to='core.FragmentTag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='trainingfragment',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='core.FragmentTagM2M', to='core.FragmentTag', verbose_name='Tags'),
        ),
    ]
