from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout #averiguar sobre esto
from django.contrib import messages
#from main.consts import BUNIT_OPTIONS
from .models import Database, Empleados, Event
from django.contrib.auth.models import Group, Permission, User
#from .filters import databasefilter
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, EventForm, databasefilter, dataForm
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from dateutil.relativedelta import relativedelta
from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .tasks import send_mail_task
from django.db.models import Count, Q
from django.forms import modelformset_factory
import calendar
#Problemas

# Como mostrar los datos guardados en un enlace (listo)
# Como encontrar los status y estado de la renovacion y donde mostrarlo (listo - consultar)
# Como eliminar los cambios hechos que se muestran (listo)
# Retroceder de pagina en pagina (show_changes) (listo)
# Mensjae para el caso de subscribir (listo)
# Correo informativo para rrhh (listo) 
# Crear cuentas por roles.. (listo)
# Mandar el mensaje cuando esta cerca el vencimiento de contrato ...(listo)
# Poner un numero a los nombres de show_changes (listo)
# Arreglar ese filtro 
# Agregar los decoradores 
# El orden al retroceder
# En update uno no debe ser capaz de modificar el nombre
# Prohibir que renueve dos veces
# Agregar un check en show_changes (listo)
# Los administradores tienen que tener la posibilidad de eliminar un queryset directo de contratos (no)
# Verificar los botones de retroceder 
#Para prohibir el acceso desde home a loginpage o register es necesario una autenticacion
# Arreglar los mensajes al realizar una accion
# Como dockerizar o levantar esta app a produccion
# Cuando un usuario haga una renovacion el admin electrodata debe verlo 


#Porque al momento de actualizar me aparece un mensaje de advertencia

#Registro de los nuevos usuarios
#https://realpython.com/manage-users-in-django-admin/

@unauthenticated_user
def loginpage(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home', username = username)
        else:
            messages.info(request, "El usuario o contraseña es incorrecto") 

    context = {}
    return render(request, 'login.html', context)

@unauthenticated_user
def registerpage(request):
    
    register = CreateUserForm()
    if request.method == 'POST':
        register = CreateUserForm(request.POST)
        if register.is_valid():
            register.save()
            user = register.cleaned_data.get('username')
            messages.success(request,'Cuenta fue creada por' + "" + user) #Muestra un mensaje sobre la cuenta en el login

            return redirect('loginpage')

    context = {'register': register}
    return render(request, 'register.html', context)

def logoutuser(request):
    logout(request)
    return redirect('loginpage')

#agregar decorador del registerpage
#User.objects.filter(group__name="admin")

#@allowed_users(allowed_roles=['admin'])
@login_required(login_url='loginpage')
def home(request, username = None):

    if request.user.groups.filter(name="admin").exists():

        all_status = ['Vigente','Por vencer','Vencido']

        #boss_table = Database.objects.values('bossname').distinct()
        #bunit_table = Database.objects.values('bunit').distinct()
        #name = Database.objects.values('name').count()

        num_empleados = Database.objects.values('name').distinct().count() #Numero total de empleados 
        num_jefes = Database.objects.values('bossname').distinct().count() 
        #Contratos Vencidos, por renovar y Vigentes
        contr_vencidos = Database.objects.filter(status="Vencido").count() #numero de contratos vencidos
        contr_porvencer = Database.objects.filter(status="Por vencer").count() #numero de contratos por vencer
        contr_vigente = Database.objects.filter(status="Vigente").count() #numero de contratos vigentes
        contr_renovad = Event.objects.all().count() #numero de contratos renovados

        all_status = ['Vigente','Por vencer','Vencido']

        bunit_count = Database.objects.values("bunit")
        queryset = Database.objects.values("bunit").annotate(st_pven=Count("status",filter=Q(status="Por vencer"))).annotate(st_venc=Count("status",filter=Q(status="Vencido"))).annotate(st_vig=Count("status",filter=Q(status="Vigente")))
        empsearch = Database.objects.values("bunit").annotate(num_empleados=Count("id"))

        # Como selected poner por default a Administracion y Finanzas
        # N° renovaciones x mes

        querydate = Event.objects.values("fecha_renovacion").annotate(feb=Count("fecha_renovacion", filter=Q(fecha_renovacion__month = 1)))

        today = date.today()

        #month_today = today.month()
        month_today = 5
        graph_mon = []
        #for n in calendar.month_name[1:month_today]:
        #    mons.append(n)

        months= ["","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        for n in range(1,month_today+1):
            graph_mon.append(months[n])


        #print(mons)
        count_renov = []

        for i in range(1, month_today):
            contr_mes = Event.objects.filter(fecha_renovacion__month = i).count()
            count_renov.append(contr_mes)

        #print(count_renov)

        # https://stackoverflow.com/questions/1317714/how-can-i-filter-a-date-of-a-datetimefield-in-django
        # https://stackoverflow.com/questions/14077799/django-filter-by-specified-month-and-year-in-date-range

        context = {'all_status':all_status, 'num_empleados':num_empleados, 'queryset' : queryset, 'empsearch': empsearch, 
        'contr_renovad':contr_renovad, 'contr_vencidos': contr_vencidos, 'contr_porvencer': contr_porvencer, 'contr_vigente': contr_vigente, 'count_renov':count_renov, 'graph_mon':graph_mon }

        return render(request,'home.html', context)
    
    elif request.user.groups.filter(name="usuarios").exists():

        #count_usuario = Database.objects.filter(bossname = request.user.username)
        #num_empleados_usuario = count_usuario.objects.values('name').distinct().count()
#
        #usuario_contrvenc = count_usuario.objects.filter(status="Vencido").count()
        #usuario_contrpven = count_usuario.objects.filter(status="Por vencer").count()
        #usuario_contrvign = count_usuario.objects.filter(status="Vigente").count()
#
        context = { }

        return render(request,'home.html',context)


#def test(request):
#Reconocer que el valor del item.name es igual al del eventform
#Foreignkey entre los valores despegables y el database model

#@allowed_users(allowed_roles=['admin','usuarios'])

@login_required(login_url='loginpage')
def contratos(request):
    # Los de recursos humanos van renovar? 
    #data = Database.objects.filter(bossname = request.user.username)
    #if request.user.groups.filter(name="usuarios").exists(): 
    #    data = Database.objects.filter(bossname = request.user.username)
    #    for i in range(0,len(data)):
    #        x_id = data[i].id # Empleado Fitz
    #        Do = Database.objects.get(pk = x_id)
    #        De = Do.event_set.all() #Todos los que ha sido renovados
##
    #        if De!= Event.objects.none(): #Si De no es un query vacio
    #            x_cs = Do.contractenddate
    #            x_pr = De[i].plazo_renovacion #Supongamos que solamente se va renovar de una misma peronsa una sola vez
    #            renovacion_value = int(x_pr)
    #            new_emp_contractend = x_cs.date() + relativedelta(months=renovacion_value)
    #            Do.contractenddate = new_emp_contractend 
    #            Do.save()
    #        else:
    #            print("No se ha renovado para el jefe")

    if request.user.groups.filter(name="admin").exists(): 
        data = Database.objects.all()
        myFilter = databasefilter(request.GET, queryset = data)
        filter = myFilter.qs

        #context = { 'myFilter': myFilter, 'filter': filter }
    elif request.user.groups.filter(name="usuarios").exists(): 
        data_user = Database.objects.filter(bossname = request.user.username)
        myFilter = databasefilter(request.GET, queryset = data_user)
        filter = myFilter.qs

        #context = { 'myFilter': myFilter, 'filter': filter }
    # Para los usuarios limitar a 20 querys
    p = Paginator(filter,30)
    page = request.GET.get('page')
    print(page)
    pagination = p.get_page(page)
    #num = "a" * pagination.paginator.num_pages
    try:
        pagination = p.get_page(page)
    except PageNotAnInteger:
        pagination = p.page(1)
    except EmptyPage:
        pagination = p.page(p.num_pages)

    num = pagination.paginator.num_pages
    #print(num)
    nums = []
    for i in range(1,num+1):
        nums.append(i)

    context = { 'myFilter': myFilter, 'filter': filter , 'pagination': pagination, "nums": nums}


    return render(request, 'contratos.html', context) 


#@allowed_users(allowed_roles=['admin','usuarios'])

#agregar el numero de renovaciones /
@login_required(login_url='loginpage')
def renovacion(request): #events
    today = date.today()
    submitted = False
    if request.method == 'POST':
        
        form = EventForm(request.POST, user=request.user)
        #form.cleanet_data['fecha_renovacion'] = date.today()
        #template = render_to_string( 'message.html', {'name': request.user.username, 'usuario': "Marcelo", 'hoy': today} )
        #email_addres = 'paul.pillhuaman@unmsm.edu.pe'
        #event = database.event_set.all()

        #form = EventForm(initial={'Empleados': name_emp})
        if form.is_valid():
            #form.cleanet_data['fecha_renovacion'] = date.today()
            form.save()
            return HttpResponseRedirect('/contratos?submitted=True')
            #send_mail_task.delay(email_addres,template)
            #email.fail_silently = False
        #else:
        #    form = EventForm() #Eventform 
        #    print("Not valid")
        #    #if 'submitted' in request.GET:
        #    #    submitted = True
    else:
        form = EventForm(user=request.user)
        if 'submitted' in request.GET:
            print("submitted")
            submitted = True

    
    context ={'form':form, 'submitted': submitted}

    return render(request, 'event.html', context)

# 'name_emp':name_emp, 'empemail_emp':empemail_emp, 'bmpposition_emp':bmpposition_emp, 'bossname_emp':bossname_emp, 'bossmail_emp':bossmail_emp, 'contractenddate': contractenddate, 'contractstartdate': contractstartdate, 'database': database

    #request.post.get()

#def send_emails():

# Crear pagination aqui
#allowed_users(allowed_roles=['admin','usuarios'])
@login_required(login_url='loginpage')
def renovaciones(request): #show_changes

    #data = Database.objects.all()
    #datupd = data.filter(plazo_renovacion="3 MESES")
    #event = Event.objects.all()
    #Empleado = Event.objects.values('Empleados').distinct()
    #print(request.user.username)
    #context = {'Empleado': Empleado, 'event': event}

    if request.user.groups.filter(name="admin").exists():
        data = Event.objects.all().order_by('id')
        Empleado = Event.objects.values('Empleados')
        #context = {'Empleado': Empleado, 'event': event}
        #context = { 'data': data}
    
    elif request.user.groups.filter(name="usuarios").exists():
        data_all = Database.objects.filter(bossname = request.user.username).order_by('id')
        data = Event.objects.none() #Declara un query vacio 
        for i in range(0,len(data_all)):
            data = data | data_all[i].event_set.all()
            #data = data_all[0].event_set.all() | data_all[1].event_set.all() | data_all[2].event_set.all()
        #context = { 'data': data }
    
    p = Paginator(data, 9)
    page = request.GET.get('page')
    pagination = p.get_page(page)

    try:
        pagination = p.get_page(page)
    except PageNotAnInteger:
        pagination = p.page(1)
    except EmptyPage:
        pagination = p.page(p.num_pages)

    num = pagination.paginator.num_pages

    nums = []
    for i in range(1,num+1):
        nums.append(i)

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST.get('actionname')
            if action == 'delete':
                id_list = request.POST.getlist('idcheckbox')
                for id in id_list:
                    event = Event.objects.get(pk = id)
                    name_delete = event.Empleados
                    name = str(name_delete)
                    event.delete()
                    messages.success(request, 'Se eliminó la renovacion de:'+ " " + name )
                #print("funciona")
                return redirect('renovaciones')

    context = { 'data': data, 'pagination': pagination, 'nums':nums}

    return render(request, 'show_changes.html', context)

 #https://stackoverflow.com/questions/431628/how-can-i-combine-two-or-more-querysets-in-a-django-view
#urls dinamicas

#@allowed_users(allowed_roles=['admin'])
#allowed_users(allowed_roles=['admin','usuarios'])
def actualizar(request, event_id): #update_event
    
    event = Event.objects.get( pk= event_id )
    name = str(event.Empleados)
    #name = str(event)
    form = EventForm(request.POST or None, instance = event, user = request.user)
    if 'update' in request.POST:
        #upd_name = request.POST.get('Empleados')
        upd_modalidad = request.POST.get('modalidad')
        upd_correlativo = request.POST.get('correlativo')
        upd_plazrenvoca = request.POST.get('plazo_renovacion')
        upd_mtvcese = request.POST.get('motivo_cese')
        upd_coments = request.POST.get('comentario')
        #event.update(Empleado = upd_name, modalidad = upd_modalidad, correlativo = upd_correlativo, 
        #plazo_renovacion = upd_plazrenvoca, motivo_cese = upd_mtvcese, comentario = upd_coments )
        
        #sE pueda prohibir el modificar el nombre del empleado

        Event.objects.update(modalidad = upd_modalidad, correlativo = upd_correlativo, plazo_renovacion = upd_plazrenvoca, 
        motivo_cese = upd_mtvcese, comentario = upd_coments)
        messages.success(request, 'Has actualizado la renovacion de:'+ " " + name)
#
        return redirect('renovaciones')
    
    context = {'event': event, 'form':form }
    return render(request, 'update_event.html', context)

    #form = EventForm(request.POST or None, instance = event, user = request.user) 
    ##name = form.get('Empleados')
    #if form.is_valid():
    #    form.save()
    #    name_update = form.cleaned_data.get('Empleados')
    #    name_str = str(name_update)
    #    messages.success(request, 'Has actualizado la renovacion de:'+ " " + name_str)
#
    #    return redirect('show_changes')
#
    ##instance what i put in the form ?
    #context = {'event': event, 'form':form, 'event':event }
    #return render(request, 'update_event.html', context)

@allowed_users(allowed_roles=['admin'])
def actualizarrrhh(request, event_id): #update_rrhh

    Eo = Event.objects.get(pk=event_id)
    databaseid = Eo.Empleados.id
    Do = Database.objects.get(pk = databaseid)
    form = dataForm(request.POST or None, instance = Do)
    if form.is_valid():
        form.save()

        return redirect('renovaciones')

    context = {'form': form, 'databaseid': databaseid}
    return render(request, 'editar_admin.html', context)

#@allowed_users(allowed_roles=['admin'])
#def delete_event(request, event_id):
#    event = Event.objects.get(pk = event_id)
#    name_delete = event.Empleados
#    name = str(name_delete)
#    event.delete()
#    messages.success(request, 'Has eliminado la renovacion de:'+ " " + name )
#    return redirect('show_changes')

@login_required(login_url='loginpage') # Esto principalmente te bloquea la entrada a comosiones desde el loginpage
def comisiones(request):
    return render(request, 'comisiones.html')

@login_required(login_url='loginpage')
def constancias(request):
    return render(request, 'constancias.html')

#def second(render):
#    return render()