from logging import PlaceHolder
from turtle import textinput
import django_filters
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *
from django.forms.widgets import TextInput

#from django.contrib.auth.models import Group, Permission, User

class CreateUserForm(UserCreationForm):

    #username = forms.CharField(forms.TextInput(max_length=50, attrs={'class': 'form-control', 'placeholder': 'Username'}))
    #email = forms.EmailField(forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    #password1 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    #password2 = forms.CharField(forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': ''}))


    class Meta:
        model =  User
        fields = ('username','email', 'password1', 'password2')
        #labels = {
        #    'username': 'Username',
        #    'email': 'Email',
        #    'password1': 'Contraseña',
        #    'password2' : 'Confirme Contraseña',
        #}

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        #    'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        #    'password2': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Confirme contraseña'}),
        #    #'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Firstname'}),
        #    #'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lastname'}),
        }


class databasefilter(django_filters.FilterSet):
    bunit = django_filters.CharFilter(lookup_expr='icontains', widget= TextInput(attrs={'size':'18', 'class': 'form-control', 'title': 'Area'})) #'placeholder': 'Area'
    bossname = django_filters.CharFilter(lookup_expr='icontains', widget= TextInput(attrs={'size':'18','class': 'form-control', 'title': 'Colaborador'})) #'placeholder': 'Jefe'
    status = django_filters.CharFilter(lookup_expr='icontains', widget= TextInput(attrs={ 'size':'12', 'class': 'form-control', 'title': 'Estado' })) #'placeholder': 'Estatus del contrato'

    class Meta: 
        model = Database
        fields = ['bunit','bossname','contractstartdate','contractenddate','status']

        #widgets = {
        #    'bunit': forms.Select(attrs={'class': 'form-control'}),
        #    'bossname': forms.Select(attrs={'class': 'form-control'}),
        #    #'contractstartdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'select a date', 'type': 'date'}),
        #    #'contractenddate': forms.DateInput( attrs={'class': 'form-control', 'placeholder': 'select a date', 'type': 'date'})
        #}

        filter_overrides = {

            models.DateField:{
                'filter_class': django_filters.DateFilter,
                'extra': lambda f:{
                    'widget' : forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={'class': 'form-control', 
                        'placeholder': 'Select a date',
                        'type': 'date'
                        }),
                },
            },
        }

class dataForm(ModelForm):
    class Meta:
        model = Database
        fields = ['statusrenovacion', 'comentario']
        labels = {
            'statusrenovacion': 'Estado de la renovacion',
            'comentario': 'Agregar comentario de recursos humanos'
        }
        widgets = {
            'statusrenovacion': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Estado de la renovacion'}),
            'comentario' : forms.Textarea(attrs={'class': 'form-control', 'rows':4, 'cols':15})
        }

class EventForm(forms.ModelForm):

    class Meta: 
        model = Event
        fields = ['Empleados','modalidad', 'correlativo', 'plazo_renovacion', 'motivo_cese', 'comentario']
        #labels = {
        #    #'Empleados': 'Nombre del empleado',
        #    'modalidad': 'Modalidad de contratación',
        #    'correlativo' : 'Correlativo de contratación',
        #    'plazo_renovacion': 'Plazo de renovación',
        #    'motivo_cese': 'Motivo de cese',
        #    'comentario': 'Comentario del colaborador'
        #}

        widgets = {
            'Empleados': forms.Select(attrs={'class': 'form-control' }),
            #'Empleados': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'emp_name', 'id': 'Empleadoname'}),#disable:True
            'motivo_cese': forms.Select(attrs={'class': 'form-control'}),
            'plazo_renovacion': forms.Select(attrs={'class': 'form-control', 'placeholder': 'plazo_renovacion'}),
            'modalidad': forms.Select(attrs={'class': 'form-control'}),
            'correlativo': forms.TextInput(attrs={'class': 'form-control' }),
            'comentario' : forms.Textarea(attrs={'class': 'form-control', 'rows':1, 'cols':30}),
            #'fecha_renovacion': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'})
            #'comentario_rrhh': forms.Textarea(attrs={'class': 'form-control', 'rows':4, 'cols':15})
        }

    # Esoy considerando que el nombre con la que se crea la cuenta es identica como esta en la base de datos.
    #https://stackoverflow.com/questions/7299973/django-how-to-access-current-request-user-in-modelform
    def __init__( self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(EventForm,self).__init__(*args, **kwargs)
        if self.user.groups.filter(name="admin").exists():
            self.fields['Empleados'].queryset = Database.objects.all()
        elif self.user.groups.filter(name="usuarios").exists():
            self.fields['Empleados'].queryset = Database.objects.filter(bossname = self.user.username)

    def clean_Empleados(self):
        Empleados = self.cleaned_data.get('Empleados')
        #print(Empleados)
        if (Empleados == " "):
            raise forms.ValidationError("Este campo no debe estar vacio")

        for instance in Event.objects.all():
            #print(instance)
            if instance.Empleados == Empleados:
                raise forms.ValidationError("Ya se ha realizado una renovacion de este empleado")
        return Empleados


    #https://stackoverflow.com/questions/53801805/can-we-use-modelform-to-update-an-existing-instance-of-a-model
    # https://stackoverflow.com/questions/10205657/django-modelform-create-or-update


        #student_boss = Database.objects.filter(bossname = "MarceloGarcia")
    #data = Event.objects.none()
    #for i in range(0,len(student_boss)):
    #    data = data | student_boss[i].event_set.all()
    #self.fields['Empleados'].queryset = Database.objects.filter(bossname = self.user.username )

    #def __init__(self, *args, **kwargs):
    #    current_boss = kwargs.pop('user', None)
    #    super(EventForm, self).__init__(*args, **kwargs)
    #    student_boss = Database.objects.filter(bossname = "MarceloGarcia")
    #    data = Event.objects.none()
    #    for i in range(0,len(student_boss)):
    #        data = data | student_boss[i].event_set.all()
    #    self.fields['Empleados'] = EventForm(queryset = data, required = True)

    #https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django

    #def clean_modalidad(self):
    #    correlativo = self.cleaned_data.get('correlativo')
    #    print(modalidad)
    #    if (correlativo == ""):
    #        raise forms.ValidationError({"Este campo no debe estar vacio"})
#
    #    return correlativo


        #def __init__(self, *args, **kwargs):
        #    super().__init__(*args, **kwargs)
        #    self.fields["Empleados"].disabled = True

        

        #def clean_name(self):
        #    Empleados = self.cleaned_data.get('Empleados')
        #    if (Empleados == ""):
        #        raise forms.ValidationError("Este campo no debe estar vacio")
        #    return Empleados
        
##
    #    for instance in Event.objects.all():
    #        if instance.Empleados == nombre_empleado:
    #            raise forms.ValidationError(" Ya existe una renovacion realizada para este empleado" + nombre_empleado)
    #    return nombre_empleado



        #def __init__(self, *args, **kwargs):
        #    super(EventForm, self).__init__(*args, **kwargs)
        #    instance = getattr(self, 'instance', None)
        #    if instance and instance.pk:
        #        self.fields['Empleados'].widget.attrs['readonly'] = True
#
        #def clean_Empleados(self):
        #    instance = getattr(self, 'instance', None)
        #    if instance and instance.pk:
        #        return instance.Empleados
        #    else:
        #        return self.cleaned_data['Empleados']


        #def __init__(self, *args, **kwargs):
        #    super(EventForm, self).__init__(*args, **kwargs)
        #    instance = getattr(self, 'instance', None)
        #    if instance and instance.id:
        #        self.fields['Empleados'].required = False
        #        self.fields['Empleados'].widget.attrs['disabled'] = 'disabled'
#
        #def clean_Empleados(self):
        #    instance = getattr(self, 'instance', None)
        #    if instance:
        #        return instance.Empleados
        #    else:
        #        return self.cleaned_data.get('Empleados', None)
        



        
