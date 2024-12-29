from django.db import models
import numpy as np

# Create your models here.
 
'''SENIORITY_LEVELS = (
    (1, 'Management'),
    (0.75, 'Senior'),
    (0.5, 'Regular'),
    (0.25, 'Junior')
)

FILED_AGAINST = (
    (1, 'Systems'),
    (0.75, 'Access/Login'),
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
)'''

SENIORITY_LEVELS = {'Management':1,'Senior':0.75,'Regular':0.5,'Junior':0.25}
FILED_AGAINST = {'Systems':1,'Access/Login':0.75,'Software':0.5,'Hardware':0.25}
TICKET_TYPE = {'Issue':1,'Request':0}
SEVERITY_LEVELS = {'Critical':1,'Major':0.75,'Minor':0.50,'Normal':0.25,'Unclassified':0}


# Create your models here.

class Employee(models.Model):
    id_number = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=30)
    seniority = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.pk} - {self.id_number}: {self.name}, rank {self.seniority}'

class Ticket(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    filedAgainst = models.CharField(max_length=30)
    ticketType = models.CharField(max_length=30)
    severity_level = models.CharField(max_length=30, blank=True, null=True)
    daysOpen = models.IntegerField(default=0, blank=True, null=True)
    priority = models.FloatField(default=1, blank=True, null=True)
    
    def getPriority(self):
        if self.daysOpen <= 14:
            urgency = (self.daysOpen/14)*0.15
        else:
            urgency = 0.15
        
        # Weighted scoring system
        sn = float(SENIORITY_LEVELS[self.employee.seniority])*0.2
        fa = float(FILED_AGAINST[self.filedAgainst])*0.2
        tt = float(TICKET_TYPE[self.ticketType])*0.05
        sv = float(SEVERITY_LEVELS[self.severity_level])*0.4

        self.priority = np.ceil((sn+fa+tt+sv+urgency)*4)
        self.save()

    def __str__(self):
        return f'{self.pk} - {self.employee.name}: {self.filedAgainst}, {self.ticketType}, {self.severity_level}'