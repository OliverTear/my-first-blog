# Generated by Django 4.1.3 on 2022-11-14 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_book_bookshelf_delete_post_book_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookshelf',
            name='name',
            field=models.CharField(default=1, max_length=100, verbose_name='制作者'),
            preserve_default=False,
        ),
    ]
