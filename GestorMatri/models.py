from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Estudiante(models.Model):
    codigo_estudiante = models.CharField(max_length=10, unique=True, verbose_name="Código")
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField()
    fecha_ingreso = models.DateField(default=timezone.now)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo_estudiante} - {self.nombres} {self.apellidos}"
    
    def promedio_general(self):
        # Obtener todas las calificaciones del estudiante a través de sus matrículas
        matriculas = self.matricula_set.all()
        calificaciones = []
        for matricula in matriculas:
            cals = matricula.calificacion_set.all()
            calificaciones.extend(cals)
        
        if calificaciones:
            return float(sum(c.nota for c in calificaciones) / len(calificaciones))
        return 0
    
    def rendimiento_estado(self):
        promedio = self.promedio_general()
        if promedio >= 16:
            return "Excelente"
        elif promedio >= 14:
            return "Bueno"
        elif promedio >= 11:
            return "Regular"
        else:
            return "Bajo"
    
    def necesita_tutoria(self):
        return self.promedio_general() < 13
    
    class Meta:
        verbose_name_plural = "Estudiantes"


class Curso(models.Model):
    codigo_curso = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6)])
    semestre = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    obligatorio = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.codigo_curso} - {self.nombre}"
    
    class Meta:
        verbose_name_plural = "Cursos"


class Matricula(models.Model):
    ESTADO_CHOICES = [
        ('MATRICULADO', 'Matriculado'),
        ('RETIRADO', 'Retirado'),
        ('COMPLETADO', 'Completado'),
    ]
    
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_matricula = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='MATRICULADO')
    
    def __str__(self):
        return f"{self.estudiante.codigo_estudiante} - {self.curso.codigo_curso}"
    
    class Meta:
        unique_together = ['estudiante', 'curso']
        verbose_name_plural = "Matrículas"


class Calificacion(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE)
    nota = models.DecimalField(max_digits=4, decimal_places=2, 
                              validators=[MinValueValidator(0), MaxValueValidator(20)])
    fecha_evaluacion = models.DateField(auto_now_add=True)
    
    def aprobado(self):
        return self.nota >= 11
    
    def __str__(self):
        return f"{self.matricula} - {self.nota}"
    
    class Meta:
        verbose_name_plural = "Calificaciones"
