import django_filters
from dataclasses import field
import django
#from django.forms import ModelForm, MultipleChoiceField, forms
import django_filters
from django_filters import DateFilter, CharFilter, DateFromToRangeFilter
from django.forms.widgets import NumberInput,DateInput
from django_filters.widgets import RangeWidget,CSVWidget,DateRangeWidget
from django import forms
from .models import *

class databasefilter(django_filters.FilterSet):

    class Meta: 
        model = Database
        #fields = {
        #    'bossname': ['exact'], 'bunit': ['exact'],
        #    'status': ['exact']
        #    }

        fields = ['bunit','bossname','status','contractstartdate','contractenddate']
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


