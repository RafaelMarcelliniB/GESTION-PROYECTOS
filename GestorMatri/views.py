from django.shortcuts import render
from django.http import HttpResponse
from .models import Estudiante, Curso, Matricula, Calificacion
from django.db.models import Avg, Count


def inicio(request):
    context = {
        'total_estudiantes': Estudiante.objects.filter(activo=True).count(),
        'total_cursos': Curso.objects.count(),
        'total_matriculas': Matricula.objects.filter(estado='MATRICULADO').count(),
    }
    return render(request, 'GestorMatri/inicio.html', context)


def lista_estudiantes(request):
    estudiantes = Estudiante.objects.filter(activo=True).order_by('apellidos')
    return render(request, 'GestorMatri/estudiantes.html', {'estudiantes': estudiantes})


def reporte_rendimiento(request):
    estudiantes = Estudiante.objects.filter(activo=True)
    estudiantes_con_datos = []
    
    for estudiante in estudiantes:
        promedio = estudiante.promedio_general()
        estado = estudiante.rendimiento_estado()
        necesita_tutoria = estudiante.necesita_tutoria()
        
        # Buscar cursos reprobados
        cursos_reprobados = []
        matriculas = Matricula.objects.filter(estudiante=estudiante)
        for matricula in matriculas:
            calificaciones = Calificacion.objects.filter(matricula=matricula)
            for cal in calificaciones:
                if not cal.aprobado():
                    cursos_reprobados.append(matricula.curso.nombre)
        
        estudiantes_con_datos.append({
            'estudiante': estudiante,
            'promedio': round(promedio, 2),
            'estado': estado,
            'necesita_tutoria': necesita_tutoria,
            'cursos_reprobados': cursos_reprobados,
        })
    
    return render(request, 'GestorMatri/reporte.html', {'estudiantes_datos': estudiantes_con_datos})


def recomendaciones(request):
    # Estudiantes que necesitan tutorías
    estudiantes_tutoria = []
    # Estudiantes que deben repetir cursos
    estudiantes_repetir = []
    
    estudiantes = Estudiante.objects.filter(activo=True)
    
    for estudiante in estudiantes:
        if estudiante.necesita_tutoria():
            estudiantes_tutoria.append(estudiante)
        
        # Verificar si tiene cursos reprobados
        matriculas = Matricula.objects.filter(estudiante=estudiante)
        cursos_reprobados = []
        for matricula in matriculas:
            calificaciones = Calificacion.objects.filter(matricula=matricula)
            for cal in calificaciones:
                if not cal.aprobado():
                    cursos_reprobados.append(matricula.curso)
        
        if cursos_reprobados:
            estudiantes_repetir.append({
                'estudiante': estudiante,
                'cursos': cursos_reprobados
            })
    
    context = {
        'estudiantes_tutoria': estudiantes_tutoria,
        'estudiantes_repetir': estudiantes_repetir,
    }
    return render(request, 'GestorMatri/recomendaciones.html', context)
