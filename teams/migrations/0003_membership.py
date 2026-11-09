from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_rename_membership_memberships'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Memberships',
            new_name='Membership',
        ),
    ]
