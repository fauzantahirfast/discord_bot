# Generated by Django 4.2.17 on 2024-12-24 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvatardecorationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.IntegerField()),
                ('asset', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccountDetails',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('avatar', models.CharField(max_length=100)),
                ('discriminator', models.CharField(max_length=100)),
                ('public_flags', models.IntegerField()),
                ('flags', models.IntegerField()),
                ('banner', models.CharField(max_length=100)),
                ('accent_color', models.BigIntegerField()),
                ('global_name', models.CharField(max_length=100)),
                ('premium_type', models.IntegerField()),
                ('avatar_decoration_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.avatardecorationdata')),
            ],
        ),
    ]