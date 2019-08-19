# Generated by Django 2.2.1 on 2019-08-19 13:32

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_add_image_gallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtail.core.fields.StreamField([('heading', wagtail.core.blocks.CharBlock(classname='full title')), ('paragraph', wagtail.core.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('decimal', wagtail.core.blocks.DecimalBlock()), ('date', wagtail.core.blocks.DateBlock()), ('datetime', wagtail.core.blocks.DateTimeBlock()), ('gallery', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(classname='full title')), ('images', wagtail.core.blocks.StreamBlock([('image', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock())]))]))]))]),
        ),
    ]
