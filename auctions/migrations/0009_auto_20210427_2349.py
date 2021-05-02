# Generated by Django 3.1.6 on 2021-04-27 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20210426_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='usercommentlist',
            field=models.ManyToManyField(blank=True, related_name='usercomment', to='auctions.AuctionComment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='userwatchlist',
            field=models.ManyToManyField(blank=True, related_name='userwatch', to='auctions.AuctionWatch'),
        ),
    ]
