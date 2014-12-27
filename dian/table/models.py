from django.db import models


class TableType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    min_seats = models.IntegerField("min seats", default=1)
    max_seats = models.IntegerField("max seats", default=1)


class Table(models.Model):
    TABLE_STATUS = (
        ('dining', 'Dining'),
        ('waiting', 'Waiting'),
        ('booked', 'Booked'),
        ('initial', 'Initial')
    )
    id = models.AutoField(primary_key=True)
    table_number = models.CharField(max_length=255, blank=False, null=False)
    table_type = models.ForeignKey(TableType, null=False, related_name='tables')
    status = models.CharField(max_length=12, choices=TABLE_STATUS, default=TABLE_STATUS[-1][0])