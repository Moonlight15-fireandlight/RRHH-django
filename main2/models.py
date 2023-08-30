from django.db import models
from .consts import STATUS_OPTIONS, BUNIT_OPTIONS, BOSS_OPTIONS, MOD_OPTIONS, PLZ_OPTIONS, CES_OPTIONS, STAT_RENOVACION  
from datetime import date
from dateutil.relativedelta import relativedelta
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
# Create your models here.

class Database(models.Model):
    name = models.CharField(max_length=50)
    empemail = models.EmailField(max_length=50, blank=True, null=True)
    bunit = models.CharField(max_length=50)
    bmpposition = models.CharField(max_length=50, blank=True, null=True)
    bossname = models.CharField(max_length=50, blank=True, null=True)
    bossmail = models.EmailField(max_length=50)
    contractstartdate = models.DateField(blank=True, null=True)
    contractenddate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    statusrenovacion = models.CharField(max_length=50, choices = STAT_RENOVACION, blank=True, null=True)
    #####
    modalidad = models.CharField(max_length=50, choices=MOD_OPTIONS, blank=True, null=True)
    correlativo = models.CharField(max_length=50, blank=True, null=True)
    plazo_renovacion= models.CharField(max_length=50, choices=PLZ_OPTIONS, blank=True, null=True)
    motivo_cese = models.CharField(max_length=50, choices=CES_OPTIONS, blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)
    #renovacion = models.ForeignKey('Event',on_delete=models.CASCADE, null=True)


# Solo se modifica el status mediante el event -- si lo guarda directamente desde el admin no funciona

    #Cambio el status cuando deje esto pero sucede un error en el view
    def save(self, *args, **kwargs):
        #if self.status == "Por Vencer":
    #    #self.status = self.Contract_status()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'empleado'
        ordering = ('id',)
    
    def __str__(self):
        return self.name
    #self.bossname

@receiver(pre_save, sender = Database)
def generate_dbstat(sender, instance, *args, **kwargs):
    print("pre_status")
    today = date.today()
    days_delta = (instance.contractenddate - today).days
    if days_delta > 30:
        instance.status = "Vigente"
    elif days_delta <= 30 and days_delta >= 0:
        instance.status = "Por vencer"
    else: 
        instance.status = "Vencido"
        
#Esto no se va ejecutar bien, pues necesito que esto sea automatico y las señales necesitan un trigger
#@receiver(post_save, sender = Database)
#def send_email(sender, instance, *args, **kwargs):
#    print("send_email")
#    #template = render_to_string( 'message.html', {'name': request.user.username, 'usuario': database.name, 'hoy': today} )
#    email = EmailMessage(
#        'Aurora app - renovacion de contrato',
#        "Falta renovar!",
#        settings.EMAIL_HOST_USER,
#        ['paul.pillhuaman@unmsm.edu.pe'],#instance.bossmail
#    )
#    if instance.status == "Por vencer":
#        email.send()
    
    #instance.save()
    #instance.status = instance.contractenddate
    #today = date.today()
    #days_delta = (instance.contractenddate - today).days
    #if days_delta > 30:
    #    instance.status = "Vigente"
    #elif days_delta <= 30 and days_delta >= 0:
    #    instance.status = "Por Vencer"
    #else:
    #    instance.status="Vencido"
#post_save.connect(article_post_save, sender=Database)

#https://stackoverflow.com/questions/25386119/whats-the-difference-between-a-onetoone-manytomany-and-a-foreignkey-field-in-d

class Event(models.Model):
    Empleados =  models.ForeignKey('Database', on_delete=models.CASCADE, null=True)
    modalidad = models.CharField(max_length=50, choices=MOD_OPTIONS)
    correlativo = models.CharField(max_length=50, blank=True, null=True)
    plazo_renovacion= models.CharField(max_length=50, choices=PLZ_OPTIONS)
    motivo_cese = models.CharField(max_length=50, choices=CES_OPTIONS)
    comentario = models.TextField(blank=True, null=True)
    comentario_rrhh = models.TextField(blank=True, null=True)
    #Creando una nueva variable para la grafica de n°empleadosxmes
    fecha_renovacion = models.DateField(blank=True, null=True)

#Con esta funcion guardo por default el campo fecha_renovacion igual al dia en que se renueva un contrato
    def save(self, *args, **kwargs):
        today = date.today()
        if not self.fecha_renovacion:
            self.fecha_renovacion = today
        super(Event,self).save(*args,**kwargs)


@receiver(post_save, sender = Event)
def generate_status(sender, instance, *args, **kwargs):
    print('post_save')
    #print(sender, instance)
    today = date.today()

    Empleado = instance.Empleados
    Empleado_pr = instance.plazo_renovacion
    Empleado_ce = Empleado.contractenddate
    newcontractendate = Empleado_ce + relativedelta(months=int(Empleado_pr))
    Empleado.contractenddate = newcontractendate
    #instance.fecha_renovacion = today

    Empleado.save()
    #instance.save()

#@receiver(post_save, sender = Event)
#def generate_status(sender, instance, *args, **kwargs):
#    print('post_save')
#    #print(sender, instance)
#    today = date.today()
#
#    instance.fecha_renovacion = today
#
#    instance.save()



class Empleados(models.Model):
    name = models.CharField(max_length=50)
    empemail = models.EmailField(max_length=50, blank=True, null=True)
    bunit = models.CharField(max_length=50, choices=BUNIT_OPTIONS)
    bmpposition = models.CharField(max_length=50, blank=True, null=True)
    bossname = models.CharField(max_length=50, choices=BOSS_OPTIONS)
    bossmail = models.EmailField(max_length=50)
    contractstartdate = models.DateField(blank=True, null=True)
    contractenddate = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.name















