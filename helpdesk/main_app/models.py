from django.db import models
import numpy as np
'''from import_export import resources
from import_export.admin import ImportExportModelAdmin'''

SENIORITY_LEVELS = (
    ("M", 'Management'),
    (0.75, 'Senior'),
    (0.5, 'Regular'),
    (0.25, 'Junior')
)

FILED_AGAINST = (
    (1, 'Systems'),
    ("AL", 'Access/Login'),
    (0.5, 'Software'),
    (0.25, 'Hardware')
)
TICKET_TYPE = (
    (1, 'Issue'),
    (0, 'Request')
)
SEVERITY_LEVELS = (
    (1, 'Critical'),
    (0.75, 'Major'),
    (0.50, 'Minor'),
    (0.25, 'Normal'),
    (0, 'Unclassified')
)

# Create your models here.

class Employee(models.Model):
    id_number = models.CharField(max_length=4, primary_key=True)
    name = models.CharField(max_length=30)
    seniority = models.CharField(max_length=30, choices=SENIORITY_LEVELS)

    def __str__(self):
        return f'{self.id_number}: {self.name}, rank {self.seniority}'

class Ticket(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    filedAgainst = models.CharField(max_length=30, choices=FILED_AGAINST)
    ticketType = models.CharField(max_length=30, choices=TICKET_TYPE)
    severity = models.CharField(max_length=30, severity=SEVERITY_LEVELS)
    daysOpen = models.IntegerField(default=0, blank=True, null=True)
    priority = models.FloatField(default=1, blank=True, null=True)

    

    def getPriority(self):
        if self.daysOpen <= 14:
            urgency = (self.daysOpen/14)*0.15
        else:
            urgency = 0.15
        
        # Weighted scoring system
        sn = float(self.employee.seniority)*0.2
        fa = float(self.filedAgainst)*0.3
        tt = float(self.ticketType)*0.05
        sv = float(self.severity)*0.3

        self.priority = np.ceil((sn+fa+tt+sv+urgency)*4)
        self.save()

    def __str__(self):
        return f'{self.employee.name}: {self.filedAgainst}'