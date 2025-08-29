from django.contrib import admin
from .models import Estudiante, Curso, Matricula, Calificacion


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo_estudiante', 'nombres', 'apellidos', 'email', 'fecha_ingreso', 'activo']
    list_filter = ['activo', 'fecha_ingreso']
    search_fields = ['codigo_estudiante', 'nombres', 'apellidos']
    ordering = ['apellidos', 'nombres']


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo_curso', 'nombre', 'creditos', 'semestre', 'obligatorio']
    list_filter = ['semestre', 'obligatorio']
    search_fields = ['codigo_curso', 'nombre']
    ordering = ['semestre', 'codigo_curso']


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'fecha_matricula', 'estado']
    list_filter = ['estado', 'fecha_matricula', 'curso__semestre']
    search_fields = ['estudiante__codigo_estudiante', 'curso__codigo_curso']
    ordering = ['-fecha_matricula']


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'nota', 'fecha_evaluacion', 'aprobado']
    list_filter = ['fecha_evaluacion']
    search_fields = ['matricula__estudiante__codigo_estudiante', 'matricula__curso__codigo_curso']
    ordering = ['-fecha_evaluacion']
    
    def aprobado(self, obj):
        return obj.aprobado()
    aprobado.boolean = True
    aprobado.short_description = 'Aprobado'
