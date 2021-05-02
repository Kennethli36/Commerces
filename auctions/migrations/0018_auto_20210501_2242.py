# Generated by Django 3.1.6 on 2021-05-01 22:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20210501_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='usercommentlist',
        ),
        migrations.AddField(
            model_name='auctioncomment',
            name='usercommentlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commenter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctioncomment',
            name='auctioncomments',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctionlisting'),
        ),
    ]
