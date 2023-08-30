#from .models import Database
#
#data = Database.objects.all()
#bunit_table = Database.objects.values("bunit").distinct()
#boss_table = Database.objects.values("bossname").distinct()

STATUS_OPTIONS = (
    ('vigente','VIGENTE'),
    ('vencido','VENCIDO'),
    ('por vencer', 'POR VENCER'),
)

QC = "QUINTA CATEGORIA"
RH = "RECIBO POR HONORARIOS"
Ppp = "PRACTICAS PRE PROFESIONALES"
Pp = "PRACTICAS PROFESIONALES"

MOD_OPTIONS = (
    (QC , 'Quinta Categoria'),
    (RH, 'Recibo por honorarios'),
    (Ppp,'Practicas pre profesionales'),
    (Pp, 'Practicas profesionales'),
)
PLZ_OPTIONS  = (
    ('1', '1 mes'),
    ('2', '2 meses'),
    ('3', '3 meses' ),
    ('4', '4 meses'),
    ('5', '5 meses'),
    ('6','6 meses'),
    ('12', '12 meses'),
    ('0', 'No renovar'),
)

PP = "PERIODO DE PRUEBA"
TCSJI = "TERMINO DE CONTRATO A SOLICITUD DEL JEFE INMEDIATO"
TCSC = "TERMINO DE CONTRATO A SOLICITUD DEL COLABORADOR"
RN = "RENUNCIA"
MD = "MUTUO DISENSO"

CES_OPTIONS = (
    (PP, 'Periodo de prueba'),
    (TCSJI, 'Termino de contrato a solicitud del jefe inmediato'),
    (TCSC, 'Termino de contrato a solicitu del colaborador'),
    (RN, 'Renuncia'),
    (MD, 'Mutuo disenso'),
)

PEND = "Pendiente"
EC = "Enviado por el colaborador"
FC = "Firmado por el colaborador"
CS = "Cese"
IF = "Indefinido"

STAT_RENOVACION = (
    (PEND, 'PENDIENTE'),
    (EC, "ENVIADO POR EL COLABORADOR"),
    (FC, "FIRMADO POR EL COLABORADOR"),
    (CS, "CESE"),
    (IF, "INDEFINIDO"),
)


BUNIT_OPTIONS = (('Administración y Finanzas', 'Administración y Finanzas'), ('Antamina', 'Antamina'), ('Arquitecto de Implementación', 'Arquitecto de Implementación'), 
('Brocal Operaciones', 'Brocal Operaciones'), ('Buenaventura', 'Buenaventura'), ('Buenaventura Servicios', 'Buenaventura Servicios'), ('CHINALCO', 'CHINALCO'), 
('Contabilidad y Finanzas', 'Contabilidad y Finanzas'), ('Coordinador de Soluciones IT-OT', 'Coordinador de Soluciones IT-OT'), ('Coordinador de TI - Goldfields', 'Coordinador de TI - Goldfields'), 
('Coordinadora de Compensaciones y Bienestar', 'Coordinadora de Compensaciones y Bienestar'), ('Coordinadora de Facturación y Cobranza', 'Coordinadora de Facturación y Cobranza'), 
('Coordinadora de NOC/SOC', 'Coordinadora de NOC/SOC'), ('DC', 'DC'), ('Desarrollo TI', 'Desarrollo TI'), ('Dirección Comercial', 'Dirección Comercial'), 
('Director de Marketing y estrategia comercial', 'Director de Marketing y estrategia comercial'), ('Encargado de Servicios Generales', 'Encargado de Servicios Generales'), 
('Estrategia, Control y Calidad', 'Estrategia, Control y Calidad'), ('Facturación', 'Facturación'), ('Gerencia de Cuentas', 'Gerencia de Cuentas'), ('Gerencia de Servicios', 'Gerencia de Servicios'), 
('Gerencia de Unidad de Negocio', 'Gerencia de Unidad de Negocio'), ('Gerencia General', 'Gerencia General'), ('Gerente Comercial', 'Gerente Comercial'), ('Gerente de Mineria', 'Gerente de Mineria'), 
('Gerente de Operaciones', 'Gerente de Operaciones'), ('Gerente de UN Integración', 'Gerente de UN Integración'), ('Gerente de UN Seguridad', 'Gerente de UN Seguridad'), 
('Gerente de Venta', 'Gerente de Venta'), ('Gestión de Operaciones', 'Gestión de Operaciones'), ('Gestión de Proyectos', 'Gestión de Proyectos'), ('Gestión de Servicios', 'Gestión de Servicios'), 
('Gestión del Talento Humano', 'Gestión del Talento Humano'), ('Gestor de Servicios', 'Gestor de Servicios'), ('Gestor del Talento Humano', 'Gestor del Talento Humano'), 
('GESTOR ESTRATÉGICO', 'GESTOR ESTRATÉGICO'), ('Gestor General Proyectos Minería', 'Gestor General Proyectos Minería'), ('Gold Fields Operaciones', 'Gold Fields Operaciones'), 
('Hudbay Operaciones', 'Hudbay Operaciones'), ('Implementación e Ingeniería', 'Implementación e Ingeniería'), ('Jefe de Contabilidad y Finanzas', 'Jefe de Contabilidad y Finanzas'), 
('Jefe de Implementación e Ingeniería', 'Jefe de Implementación e Ingeniería'), ('Jefe de Logística y Servicios Generales', 'Jefe de Logística y Servicios Generales'), 
('Jefe de Marketing', 'Jefe de Marketing'), ('Jefe de PMO', 'Jefe de PMO'), ('Jefe de Service Desk', 'Jefe de Service Desk'), ('Logística y Servicios Generales', 'Logística y Servicios Generales'), 
('Marketing', 'Marketing'), ('Minera Cerro Verde', 'Minera Cerro Verde'), ('MINSUR', 'MINSUR'), ('NOC/SOC', 'NOC/SOC'), 
('Oficina de Dirección de Proyectos', 'Oficina de Dirección de Proyectos'), ('Pan America', 'Pan America'), ('Proyectos Minería', 'Proyectos Minería'), ('QUIMPAC', 'QUIMPAC'), 
('Residentes', 'Residentes'), ('Service Desk', 'Service Desk'), ('Soluciones de nube y servicios digitales', 'Soluciones de nube y servicios digitales'), ('Soluciones IT - OT', 'Soluciones IT - OT'), 
('SUMMA GOLD', 'SUMMA GOLD'), ('Supervisor de Chinalco', 'Supervisor de Chinalco'), ('Supervisor de Cuenta - Buenaventura', 'Supervisor de Cuenta - Buenaventura'), 
('Supervisor de Proyecto - Buenaventura', 'Supervisor de Proyecto - Buenaventura'), ('Supervisor de Proyectos - Goldfields', 'Supervisor de Proyectos - Goldfields'), 
('Supervisor de Proyectos 1', 'Supervisor de Proyectos 1'), ('Supervisor de TI - Goldfields', 'Supervisor de TI - Goldfields'), ('Supervisor de TI - Hudbay.', 'Supervisor de TI - Hudbay.'), 
('Team Leader de Desarrollo TI', 'Team Leader de Desarrollo TI'))

BOSS_OPTIONS = (('ALEJANDRO RIVADENEYRA REATEGUI', 'ALEJANDRO RIVADENEYRA REATEGUI'), ('SUSAN AREVALO TICLLA', 'SUSAN AREVALO TICLLA'), ('PEDRO HUAROTO MAMANI', 'PEDRO HUAROTO MAMANI'), 
('EFRAIN VALVERDE BEGAZO', 'EFRAIN VALVERDE BEGAZO'), ('ELMER DEZA SAAVEDRA', 'ELMER DEZA SAAVEDRA'), ('ZUMIKO RIVADENEYRA GONZALES', 'ZUMIKO RIVADENEYRA GONZALES'), 
('SERGIO LEON LEYVA', 'SERGIO LEON LEYVA'), ('DANIEL PEREZ JULCA', 'DANIEL PEREZ JULCA'), ('TERESA RAMOS MORIN', 'TERESA RAMOS MORIN'), ('MILAGROS ROMERO BALLON', 'MILAGROS ROMERO BALLON'), 
('LESLY JIMENEZ ', 'LESLY JIMENEZ '), ('DIEGO NUÑEZ MARROQUIN', 'DIEGO NUÑEZ MARROQUIN'), ('PERCY TORRES BENITES', 'PERCY TORRES BENITES'), ('CHRISTIAM GUTIERREZ DIAZ', 'CHRISTIAM GUTIERREZ DIAZ'), 
('RODOLFO VILCHEZ PORTILLA', 'RODOLFO VILCHEZ PORTILLA'), ('FELIX SANDOVAL ZEVALLOS', 'FELIX SANDOVAL ZEVALLOS'), ('EDUARDO PONCE PAZ', 'EDUARDO PONCE PAZ'), ('JOSE VENERO SALCEDO', 'JOSE VENERO SALCEDO'), 
('ANGELA PEREZ CHAVEZ', 'ANGELA PEREZ CHAVEZ'), ('LIZBETH TULLUME GARNIQUE', 'LIZBETH TULLUME GARNIQUE'), ('ABEL PAREDES  INOCENTE', 'ABEL PAREDES  INOCENTE'), 
('LEANDRA MASIAS DONAYRE', 'LEANDRA MASIAS DONAYRE'), ('ROGER CHAUCA ZEA', 'ROGER CHAUCA ZEA'), ('ZANDRA VALDIVIEZO VALLE', 'ZANDRA VALDIVIEZO VALLE'), ('GINA PASTOR NORIEGA', 'GINA PASTOR NORIEGA'), 
('TOBIAS DIAZ CHACON', 'TOBIAS DIAZ CHACON'), ('MAYRA CATACORA DÍAZ', 'MAYRA CATACORA DÍAZ'), ('OSMAR LOYA OLIVERA', 'OSMAR LOYA OLIVERA'), ('CESAR CUYA ESCRIBA', 'CESAR CUYA ESCRIBA'), 
('ROJER RODRIGUEZ VASQUEZ', 'ROJER RODRIGUEZ VASQUEZ'), ('GHANIER MIRANDA REYES', 'GHANIER MIRANDA REYES'), ('DIEGO ESTRAVER ALVARADO', 'DIEGO ESTRAVER ALVARADO'), 
('JONATHAN CHAMPI MEDINA', 'JONATHAN CHAMPI MEDINA'), ('JIMMY QUISPE ROMERO', 'JIMMY QUISPE ROMERO'))


#all_bosses = []
#for boss in boss_table:
#    for key, value in boss.items():
#        all_bosses.append(value)
#
#BOSS_OPTIONS = [None]*len(all_bosses)
#
#for i,j in zip(all_bosses,range(len(all_bosses))):
#    BOSS_OPTIONS[j] = (i,i)
#
#all_bunit = []
#for bunit in bunit_table:
#    for key, value in bunit.items():
#        all_bunit.append(value)
#
#BUNIT_OPTIONS = [None]*len(all_bunit)
#
#for i,j in zip(all_bunit,range(len(all_bunit))):
#    BUNIT_OPTIONS[j] = (i,i) 