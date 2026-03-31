from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Rol, Usuario, Cinturon, Categoria, Examen, Video, Resultado, Evaluador, Participante, ExamenCategoria, Observacion, Historial, CinturonCategoria
from .forms import RolForm, UsuarioForm, CinturonForm, CategoriaForm, ExamenForm, VideoForm, ResultadoForm, EvaluadorForm, ParticipanteForm, ExamenCategoriaForm, ObservacionForm, HistorialForm, CinturonCategoriaForm
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from django.conf import settings
import os
from django.utils.timezone import now 
from django.shortcuts import redirect

def instructor_home(request):
    return render(request, 'instructor/home.html')

def inicio(request):
     return render(request, 'admin/paginas/inicio.html')
# Create your views here.
#solicitud y renderizado de nosotros.html
def nosotros(request):
    return render(request, 'admin/paginas/nosotros.html')

def roles(request):
    roles= Rol.objects.all() 
    return render(request, 'admin/roles/index.html', {'roles': roles})

def crear_rol(request):
    formulario = RolForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('roles')
    return render(request, 'admin/roles/crear.html', {'formulario': formulario})

def editar_rol(request, id):
    rol = Rol.objects.get(id=id)
    formulario = RolForm(request.POST or None, request.FILES or None, instance=rol)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('roles')
    return render(request, 'admin/roles/edit.html', {'formulario': formulario})

def eliminar_rol(request, id):
    rol = Rol.objects.get(id=id)
    rol.delete()
    return redirect('roles')



def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admin/usuarios/index.html', {'usuarios': usuarios})

def crear_usu(request):
    formulario = UsuarioForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('usuarios')
    return render(request, 'admin/usuarios/crear.html', {'formulario': formulario})

def editar_usu(request, id):
    usuario = Usuario.objects.get(id=id)
    formulario = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('usuarios')
    return render(request, 'admin/usuarios/edit.html', {'formulario': formulario})

def eliminar_usu(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    return redirect('usuarios')


def cinturones(request):
    cinturones = Cinturon.objects.all()
    return render(request, 'admin/cinturones/index.html', {'cinturones': cinturones})

def crear_cint(request):
    formulario = CinturonForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('cinturones')
    return render(request, 'admin/cinturones/crear.html', {'formulario': formulario})

def editar_cint(request, id):
    cinturon = Cinturon.objects.get(id=id)
    formulario = CinturonForm(request.POST or None, request.FILES or None, instance=cinturon)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('cinturones')
    return render(request, 'admin/cinturones/edit.html', {'formulario': formulario})

def eliminar_cint(request, id):
    cinturon = Cinturon.objects.get(id=id)
    cinturon.delete()
    return redirect('cinturones')



def categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'admin/categorias/index.html', {'categorias': categorias})

def crear_cat(request):
    formulario = CategoriaForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('categorias')
    return render(request, 'admin/categorias/crear.html', {'formulario': formulario})

def editar_cat(request, id):
    categoria = Categoria.objects.get(id=id)
    formulario = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('categorias')
    return render(request, 'admin/categorias/edit.html', {'formulario': formulario})

def eliminar_cat(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    return redirect('categorias')



def examenes(request):
    examenes = Examen.objects.all()
    return render(request, 'admin/examenes/index.html', {'examenes': examenes})

def crear_exa(request):
    formulario = ExamenForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('examenes')
    return render(request, 'admin/examenes/crear.html', {'formulario': formulario})

def editar_exa(request, id):
    examen = Examen.objects.get(id=id)
    formulario = ExamenForm(request.POST or None, request.FILES or None, instance=examen)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('examenes')
    return render(request, 'admin/examenes/edit.html', {'formulario': formulario})

def eliminar_exa(request, id):
    examen = Examen.objects.get(id=id)
    examen.delete()
    return redirect('examenes')


def videos(request):
    videos = Video.objects.all()
    return render(request, 'admin/videos/index.html', {'videos': videos})

def crear_vid(request):
    formulario = VideoForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('videos')
    return render(request, 'admin/videos/crear.html', {'formulario': formulario})

def editar_vid(request, id):
    video = Video.objects.get(id=id)
    formulario = VideoForm(request.POST or None, request.FILES or None, instance=video)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('videos')
    return render(request, 'admin/videos/edit.html', {'formulario': formulario})

def eliminar_vid(request, id):
    video = Video.objects.get(id=id)
    video.delete()
    return redirect('videos')

def resultados(request):
    resultados = Resultado.objects.all()
    return render(request, 'admin/resultados/index.html', {'resultados': resultados})

def crear_res(request):
    formulario = ResultadoForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('resultados')
    return render(request, 'admin/resultados/crear.html', {'formulario': formulario})

def editar_res(request, id):
    resultado = Resultado.objects.get(id=id)
    formulario = ResultadoForm(request.POST or None, request.FILES or None, instance=resultado)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('resultados')
    return render(request, 'admin/resultados/edit.html', {'formulario': formulario})

def eliminar_res(request, id):
    resultado = Resultado.objects.get(id=id)
    resultado.delete()
    return redirect('resultados')


import hashlib
from django.shortcuts import render, redirect
from libreria.models import Usuario
from django.db import connection

def login_view(request):
    error = None
    if request.method == 'POST':
        correo = request.POST.get('usuario')  # sigue siendo 'usuario' en el formulario
        password = request.POST.get('password')

        # Hash como está en tu BD
        # hash_password = hashlib.sha256(password.encode('utf-8')).digest()

        try:
            usuario = Usuario.objects.raw('''
                SELECT * FROM USUARIOS 
                WHERE EMAIL_USU = %s
            ''', [correo])

            usuario = list(usuario)
            if usuario:
                usuario = usuario[0]
                request.session['usuario_id'] = usuario.id
                request.session['rol'] = usuario.rol.nombre.lower()

                if usuario.rol.nombre.lower() == 'administrador':
                    return redirect('inicio')  # o tu página de admin
                elif usuario.rol.nombre.lower() == 'instructores':
                    return redirect('instructor_home')
                elif usuario.rol.nombre.lower() == 'alumnos':
                    return redirect('vista_estudiante')
                else:
                    error = "Rol no reconocido"
            else:
                error = "Correo o contraseña incorrectos"

        except Exception as e:
            error = f"Ocurrió un error: {e}"

    return render(request, 'login.html', {'error': error})


def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('usuario_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def rol_requerido(rol_esperado):
    def decorador(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get('rol') != rol_esperado:
                return redirect('sin_permiso')  # o una página de acceso denegado
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador

def logout_view(request):
    request.session.flush()
    return redirect('login')

@login_required_custom
@rol_requerido('administrador')
def vista_admin(request):
    return render(request, 'admin/roles.html')  # o lo que tengas

@login_required_custom
@rol_requerido('instructor')
def vista_instructor(request):
    return render(request, 'vista_instructor.html')

@login_required_custom
@rol_requerido('estudiante')
def vista_estudiante(request):
    return render(request, 'vista_estudiante.html')


# @login_required(login_url='login')
# def inicio(request):
#     if request.user.username != 'presidente':
#         messages.error(request, "No tienes permiso para acceder a esta sección.")
#         return redirect('login')
#     return render(request, 'inicio.html') 


def evaluadores(request):
    evaluadores = Evaluador.objects.all()
    return render(request, 'admin/evaluadores/index.html', {'evaluadores': evaluadores})

def crear_eva(request):
    formulario = EvaluadorForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('evaluadores')
    return render(request, 'admin/evaluadores/crear.html', {'formulario': formulario})

def editar_eva(request, id):
    evaluador = Evaluador.objects.get(id=id)
    formulario = EvaluadorForm(request.POST or None, request.FILES or None, instance=evaluador)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('evaluadores')
    return render(request, 'admin/evaluadores/edit.html', {'formulario': formulario})

def eliminar_eva(request, id):
    evaluador = Evaluador.objects.get(id=id)
    evaluador.delete() 
    return redirect('evaluadores')


def participantes(request):
    participantes = Participante.objects.all()
    return render(request, 'admin/participantes/index.html', {'participantes': participantes})

def crear_part(request):
    formulario = ParticipanteForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('participantes')
    return render(request, 'admin/participantes/crear.html', {'formulario': formulario})

def editar_part(request, id):
    participante = Participante.objects.get(id=id)
    formulario = ParticipanteForm(request.POST or None, request.FILES or None, instance=participante)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('participantes')
    return render(request, 'admin/participantes/edit.html', {'formulario': formulario})

def eliminar_part(request, id):
    participante = Participante.objects.get(id=id)
    participante.delete() 
    return redirect('participantes')

def examenes_categoria(request):
    examenes_categoria = ExamenCategoria.objects.all()
    return render(request, 'admin/examenes_categorias/index.html', {'examenes_categorias': examenes_categoria})

def crear_exa_cat(request):
    formulario = ExamenCategoriaForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('examenes_categorias')
    return render(request, 'admin/examenes_categorias/crear.html', {'formulario': formulario})

def editar_exa_cat(request, id):
    examen_categoria = ExamenCategoria.objects.get(id=id)
    formulario = ExamenCategoriaForm(request.POST or None, request.FILES or None, instance=examen_categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('examenes_categorias')
    return render(request, 'admin/examenes_categorias/edit.html', {'formulario': formulario})

def eliminar_exa_cat(request, id):
    examen_categoria = ExamenCategoria.objects.get(id=id)
    examen_categoria.delete() 
    return redirect('examenes_categorias')

def observaciones(request):
    observaciones = Observacion.objects.all()
    return render(request, 'admin/observaciones/index.html', {'observaciones': observaciones})

def cargar_participantes(request):
    examen_id = request.GET.get('examen_id')
    participantes = Participante.objects.filter(examen_id=examen_id).select_related('usuario')
    data = [{'id': p.id, 'nombre': str(p)} for p in participantes]
    return JsonResponse(data, safe=False)

def crear_obs(request):
    if request.method == 'POST':
        formulario = ObservacionForm(request.POST, request.FILES)
        examen_id_post = request.POST.get('examen')
        if examen_id_post:
            formulario.fields['participante'].queryset = Participante.objects.filter(examen_id=examen_id_post)
        if formulario.is_valid():
            formulario.save()
            return redirect('observaciones')
    else:
        formulario = ObservacionForm()

        examen_id = request.GET.get('examen')
        if examen_id:
            formulario.fields['participante'].queryset = Participante.objects.filter(examen_id=examen_id)

    return render(request, 'admin/observaciones/crear.html', {'formulario': formulario})


def editar_obs(request, id):
    observacion = Observacion.objects.get(id=id)
    formulario = ObservacionForm(request.POST or None, request.FILES or None, instance=observacion)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('observaciones')
    return render(request, 'observaciones/edit.html', {'formulario': formulario})

def eliminar_obs(request, id):
    observacion = Observacion.objects.get(id=id)
    observacion.delete() 
    return redirect('observaciones')

def historiales(request):
    historiales = Historial.objects.all()
    return render(request, 'admin/historiales/index.html', {'historiales': historiales})

def crear_hist(request):
    formulario = HistorialForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('historiales')
    return render(request, 'admin/historiales/crear.html', {'formulario': formulario})


def editar_hist(request, id):
    historial = Historial.objects.get(id=id)
    formulario = HistorialForm(request.POST or None, request.FILES or None, instance=historial)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('historiales')
    return render(request, 'admin/historiales/edit.html', {'formulario': formulario})

def eliminar_hist(request, id):
    historial = Historial.objects.get(id=id)
    historial.delete() 
    return redirect('historiales')

def cinturon_categoria(request):
    cinturon_categoria = CinturonCategoria.objects.all()
    return render(request, 'admin/cinturones_categorias/index.html', {'cinturon_categoria': cinturon_categoria})


def crear_cint_cat(request):
    formulario = CinturonCategoriaForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('cinturones_categorias')
    return render(request, 'admin/cinturones_categorias/crear.html', {'formulario': formulario})    


def editar_cint_cat(request, id):
    cinturon_categoria = CinturonCategoria.objects.get(id=id)
    formulario = CinturonCategoriaForm(request.POST or None, request.FILES or None, instance=cinturon_categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('cinturones_categorias')
    return render(request, 'admin/cinturones_categorias/edit.html', {'formulario': formulario})

def eliminar_cint_cat(request, id):
    cinturon_categoria = CinturonCategoria.objects.get(id=id)
    cinturon_categoria.delete() 
    return redirect('cinturones_categorias')



# REPORTES
def reportes(request):
    return render(request, 'admin/reportes/index.html')  # o el HTML que quieras mostrar

def reporte_usuarios(request):
    usuarios = Usuario.objects.all()

    contexto = {
        "usuarios": usuarios,
        "fecha_actual": date.today(),
    }
    return render(request, "admin/reportes/usuarios.html", contexto)


def imprimir_usuarios(request):
    usuarios = Usuario.objects.all()

    template = get_template("admin/reportes/PDF_usu.html")
    contexto = {
        "usuarios": usuarios,
        "fecha_actual": date.today(),
        "request": request,
        # Si vas a usar logo, puedes agregarlo:
        # "logo_path": os.path.join(settings.STATIC_ROOT, "img", "logo.png"),
    }

    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response


def reporte_observaciones (request):
    examen_id = request.GET.get('examen')
    examenes = Examen.objects.all()
    observaciones = []

    if examen_id:
        observaciones = Observacion.objects.filter(examen_id=examen_id).select_related('usuario')

    contexto = {
        'examenes': examenes,
        'observaciones' : observaciones,
                

    }   

def reporte_usuarios_por_examen(request):
    examen_id = request.GET.get('examen')
    examenes = Examen.objects.all()
    participantes = []

    if examen_id:
        participantes = Participante.objects.filter(examen_id=examen_id).select_related('usuario')

    contexto = {
        'examenes': examenes,
        'participantes': participantes,
        'examen_id': examen_id,
        'fecha_actual': date.today(), 
    }

    return render(request, 'admin/reportes/usuarios_por_examen.html', contexto)



def imprimir_usuarios_por_examen(request):
    examen_id = request.GET.get('examen')
    participantes = []

    if examen_id:
        participantes = Participante.objects.filter(examen_id=examen_id).select_related('usuario')

    template = get_template("admin/reportes/PDF_part.html")
    contexto = {
        "participantes": participantes,
        "fecha_actual": date.today(),
        "request": request,
    }

    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response


from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa

def reporte_examenes(request):
    query = request.GET.get('buscar', '')
    examenes = Examen.objects.filter(nombre__icontains=query) if query else Examen.objects.all()
    return render(request, 'admin/reportes/examenes.html', {'examenes': examenes, 'buscar': query})

def imprimir_examenes(request):
    query = request.GET.get('buscar', '')
    examenes = Examen.objects.filter(nombre__icontains=query) if query else Examen.objects.all()
    template = get_template("admin/reportes/PDF_exa.html")
    contexto = {
        "examenes": examenes,
        "fecha_actual": date.today(),
        "request": request,
    }
    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response
