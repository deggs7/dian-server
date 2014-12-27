from django.db import models


class Regstration(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=64, null=False, blank=False)
    table_type = models.ForeignKey("table.TableType", null=False, blank=False, related_name='regstrations')
    queue_number = models.IntegerField("queue number", null=False, blank=False)
    table = models.ForeignKey("table.TableType", null=True, related_name='regstraion')
