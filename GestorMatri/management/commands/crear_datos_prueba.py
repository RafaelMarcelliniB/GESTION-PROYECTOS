from django.core.management.base import BaseCommand
from GestorMatri.models import Estudiante, Curso, Matricula, Calificacion
from django.utils import timezone
from decimal import Decimal


class Command(BaseCommand):
    help = 'Crea datos de prueba para el sistema de matrículas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando datos de prueba...'))
        
        # Crear cursos
        cursos_data = [
            {'codigo': 'MAT101', 'nombre': 'Matemáticas I', 'creditos': 4, 'semestre': 1},
            {'codigo': 'FIS101', 'nombre': 'Física I', 'creditos': 4, 'semestre': 1},
            {'codigo': 'PROG101', 'nombre': 'Programación I', 'creditos': 3, 'semestre': 1},
            {'codigo': 'MAT102', 'nombre': 'Matemáticas II', 'creditos': 4, 'semestre': 2},
            {'codigo': 'FIS102', 'nombre': 'Física II', 'creditos': 4, 'semestre': 2},
            {'codigo': 'PROG102', 'nombre': 'Programación II', 'creditos': 3, 'semestre': 2},
        ]
        
        cursos = []
        for curso_info in cursos_data:
            curso, created = Curso.objects.get_or_create(
                codigo_curso=curso_info['codigo'],
                defaults={
                    'nombre': curso_info['nombre'],
                    'creditos': curso_info['creditos'],
                    'semestre': curso_info['semestre'],
                    'obligatorio': True
                }
            )
            cursos.append(curso)
            if created:
                self.stdout.write(f'Curso creado: {curso.nombre}')
        
        # Crear estudiantes
        estudiantes_data = [
            {'codigo': '2024001', 'nombres': 'Juan Carlos', 'apellidos': 'García López', 'email': 'juan.garcia@universidad.edu'},
            {'codigo': '2024002', 'nombres': 'María Elena', 'apellidos': 'Rodríguez Martínez', 'email': 'maria.rodriguez@universidad.edu'},
            {'codigo': '2024003', 'nombres': 'Carlos André', 'apellidos': 'Sánchez Vega', 'email': 'carlos.sanchez@universidad.edu'},
            {'codigo': '2024004', 'nombres': 'Ana Lucía', 'apellidos': 'Torres Mendoza', 'email': 'ana.torres@universidad.edu'},
            {'codigo': '2024005', 'nombres': 'Luis Fernando', 'apellidos': 'Herrera Silva', 'email': 'luis.herrera@universidad.edu'},
            {'codigo': '2024006', 'nombres': 'Patricia Isabel', 'apellidos': 'Morales Castro', 'email': 'patricia.morales@universidad.edu'},
        ]
        
        estudiantes = []
        for est_info in estudiantes_data:
            estudiante, created = Estudiante.objects.get_or_create(
                codigo_estudiante=est_info['codigo'],
                defaults={
                    'nombres': est_info['nombres'],
                    'apellidos': est_info['apellidos'],
                    'email': est_info['email'],
                    'fecha_ingreso': timezone.now().date(),
                    'activo': True
                }
            )
            estudiantes.append(estudiante)
            if created:
                self.stdout.write(f'Estudiante creado: {estudiante.nombres} {estudiante.apellidos}')
        
        # Crear matrículas y calificaciones
        import random
        
        for estudiante in estudiantes:
            # Cada estudiante se matricula en 3-4 cursos
            cursos_estudiante = random.sample(cursos, random.randint(3, 4))
            
            for curso in cursos_estudiante:
                matricula, created = Matricula.objects.get_or_create(
                    estudiante=estudiante,
                    curso=curso,
                    defaults={
                        'fecha_matricula': timezone.now().date(),
                        'estado': 'MATRICULADO'
                    }
                )
                
                if created:
                    self.stdout.write(f'Matrícula creada: {estudiante.codigo_estudiante} en {curso.codigo_curso}')
                    
                    # Crear una calificación para cada matrícula
                    # Simulamos diferentes rangos de notas para crear variedad
                    if estudiante.codigo_estudiante in ['2024001', '2024002']:  # Estudiantes con buen rendimiento
                        nota = Decimal(str(random.uniform(14, 20)))
                    elif estudiante.codigo_estudiante in ['2024003', '2024004']:  # Estudiantes con rendimiento regular
                        nota = Decimal(str(random.uniform(11, 15)))
                    else:  # Estudiantes con rendimiento bajo
                        nota = Decimal(str(random.uniform(6, 13)))
                    
                    calificacion, cal_created = Calificacion.objects.get_or_create(
                        matricula=matricula,
                        defaults={
                            'nota': round(nota, 2),
                            'fecha_evaluacion': timezone.now().date()
                        }
                    )
                    
                    if cal_created:
                        self.stdout.write(f'Calificación creada: {estudiante.codigo_estudiante} - {curso.codigo_curso}: {calificacion.nota}')
        
        self.stdout.write(self.style.SUCCESS('¡Datos de prueba creados exitosamente!'))
        self.stdout.write(f'Total estudiantes: {Estudiante.objects.count()}')
        self.stdout.write(f'Total cursos: {Curso.objects.count()}')
        self.stdout.write(f'Total matrículas: {Matricula.objects.count()}')
        self.stdout.write(f'Total calificaciones: {Calificacion.objects.count()}')
