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
from django.core.paginator import Paginator
from django.contrib import messages
import subprocess
import datetime
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.management import call_command
from io import StringIO
from datetime import datetime
from django.db.models import Prefetch
from collections import defaultdict
import json
from django.db.models import Count
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.http import HttpResponse

import threading

import cv2
import mediapipe as mp
from django.http import StreamingHttpResponse
import cv2
import mediapipe as mp
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import unquote



from .vision.analisis_videos import analizar_video_en_stream



def nosotros(request):
    return render(request, 'admin/paginas/nosotros.html')

@login_required
def roles(request):
    roles= Rol.objects.all() 
    roles = Rol.objects.order_by('id')
    return render(request, 'admin/roles/index.html', {'roles': roles})

@login_required
def crear_rol(request):
    formulario = RolForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        messages.success(request, f'✓ Rol {formulario.cleaned_data["nombre"]} creado correctamente') 
        return redirect('roles')
    return render(request, 'admin/roles/crear.html', {'formulario': formulario})

@login_required
def editar_rol(request, id):
    rol = Rol.objects.get(id=id)
    formulario = RolForm(request.POST or None, request.FILES or None, instance=rol)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Rol editado correctamente.') 
        return redirect('roles')
    return render(request, 'admin/roles/edit.html', {'formulario': formulario})
    
@login_required
def eliminar_rol(request, id):
    rol = Rol.objects.get(id=id)
    rol.delete()
    messages.success(request, 'Rol eliminado correctamente.')
    return redirect('roles')




@login_required
def usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'admin/usuarios/index.html', {'usuarios': usuarios})

@login_required
def crear_usu(request):
    formulario = UsuarioForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()

        messages.success(request, f'✓ Usuario {formulario.cleaned_data["nombre"]} creado correctamente')    
        
        return redirect('usuarios')
    return render(request, 'admin/usuarios/crear.html', {'formulario': formulario})


@login_required
def editar_usu(request, id):
    usuario = Usuario.objects.get(id=id)
    formulario = UsuarioForm(request.POST or None, request.FILES or None, instance=usuario)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, f'✓ Usuario {usuario.nombre} actualizado correctamente')
        return redirect('usuarios')
    return render(request, 'admin/usuarios/edit.html', {'formulario': formulario})

@login_required
def eliminar_usu(request, id):
    usuario = Usuario.objects.get(id=id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado correctamente.')
    return redirect('usuarios')


@login_required
def cinturones(request):
    cinturones = Cinturon.objects.all()
    cinturones = Cinturon.objects.order_by('id')

    return render(request, 'admin/cinturones/index.html', {'cinturones': cinturones})

@login_required
def crear_cint(request):
    formulario = CinturonForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('cinturones')
    return render(request, 'admin/cinturones/crear.html', {'formulario': formulario})

@login_required
def editar_cint(request, id):
    cinturon = Cinturon.objects.get(id=id)
    formulario = CinturonForm(request.POST or None, request.FILES or None, instance=cinturon)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('cinturones')
    return render(request, 'admin/cinturones/edit.html', {'formulario': formulario})

@login_required
def eliminar_cint(request, id):
    cinturon = Cinturon.objects.get(id=id)
    cinturon.delete()
    return redirect('cinturones')


@login_required
def categorias(request):
    categorias = Categoria.objects.all()  
    return render(request, 'admin/categorias/index.html', {'categorias': categorias})

@login_required
def crear_cat(request):
    formulario = CategoriaForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        messages.success(request, 'Categoría creada correctamente.')
        return redirect('categorias')
    return render(request, 'admin/categorias/crear.html', {'formulario': formulario})

@login_required
def editar_cat(request, id):
    categoria = Categoria.objects.get(id=id)
    formulario = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Categoría editada correctamente.')
        return redirect('categorias')
    return render(request, 'admin/categorias/edit.html', {'formulario': formulario})

@login_required
def eliminar_cat(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.delete()
    messages.success(request, 'Categoría eliminada correctamente.')

    return redirect('categorias')


@login_required
def examenes(request):
    # examenes = Examen.objects.all()
    examenes = Examen.objects.order_by('id')
    return render(request, 'admin/examenes/index.html', {'examenes': examenes})

@login_required
def crear_exa(request):
    formulario = ExamenForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid():
        fecha = formulario.cleaned_data['fecha']
        
        # 1. Validar que la fecha no sea anterior a hoy
        if fecha < timezone.now().date():
            formulario.add_error('fecha', 'No se puede seleccionar una fecha anterior a hoy.')

        # 2. Validar que no exista ya un examen con esa fecha
        elif Examen.objects.filter(fecha=fecha).exists():
            formulario.add_error('fecha', 'Ya existe un examen en esta fecha.')

        else:
            formulario.save()
            messages.success(request, 'Examen creado correctamente.')
            return redirect('examenes')

    
    return render(request, 'admin/examenes/crear.html', {'formulario': formulario})

@login_required
def editar_exa(request, id):
    examen = Examen.objects.get(id=id)
    formulario = ExamenForm(request.POST or None, request.FILES or None, instance=examen)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Examen editado correctamente.')
        return redirect('examenes')
    return render(request, 'admin/examenes/edit.html', {'formulario': formulario})

@login_required
def eliminar_exa(request, id):
    examen = Examen.objects.get(id=id)
    examen.delete()
    messages.success(request, 'Examen eliminado correctamente.')
    return redirect('examenes')


@login_required
def videos(request):
    videos = Video.objects.all()
    return render(request, 'admin/videos/index.html', {'videos': videos})

@login_required
def crear_vid(request):
    if request.method == 'POST':
        formulario = VideoForm(request.POST, request.FILES)
        if formulario.is_valid():
            observacion = formulario.cleaned_data['observacion']

            # Validación: ¿ya existe un video para esta observación?
            ya_existe = Video.objects.filter(observacion=observacion).exists()
            if ya_existe:
                formulario.add_error('observacion', 'Ya existe un video para esta observación.')
            else:
                video = formulario.save(commit=False)
                video.fecha = date.today()  # Establece la fecha aquí
                video.save()
                messages.success(request, 'Video cargado correctamente.')
                return redirect('videos')
    else:
        formulario = VideoForm()

    return render(request, 'admin/videos/crear.html', {'formulario': formulario})

@login_required
def editar_vid(request, id):
    video = Video.objects.get(id=id)
    if request.method == 'POST':
        formulario = VideoForm(request.POST, request.FILES, instance=video)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Video editado correctamente.')
            return redirect('videos')
    else:
        formulario = VideoForm(instance=video)
    return render(request, 'admin/videos/edit.html', {'formulario': formulario})

@login_required
def eliminar_vid(request, id):
    video = Video.objects.get(id=id)
    video.delete()
    messages.success(request, 'Video eliminado correctamente.')
    return redirect('videos')

@login_required
def resultados(request):
    resultados = Resultado.objects.all()
    return render(request, 'admin/resultados/index.html', {'resultados': resultados})

@login_required
def crear_res(request):
    formulario = ResultadoForm(request.POST or None, request.FILES or None)
    
    videos_dict = {
        video.id: video.archivo.url
        for video in Video.objects.all()
        if video.archivo
    }

    if formulario.is_valid():
        fecha = formulario.cleaned_data['fecha']
        
        # 1. Validar que la fecha no sea anterior a hoy
        if fecha < timezone.now().date():
            formulario.add_error('fecha', 'No se puede seleccionar una fecha anterior a hoy.')

        video = formulario.cleaned_data['video']
        if Resultado.objects.filter(video=video).exists():
            messages.error(request, f"Ya existe un análisis para el video '{video}'.")
        else:
            formulario.save()
            messages.success(request, 'Resultado creado correctamente.')
            return redirect('resultados')

    return render(request, 'admin/resultados/crear.html', {
        'formulario': formulario,
        'videos_json': json.dumps(videos_dict),
    })


@login_required
def editar_res(request, id):
    resultado = Resultado.objects.get(id=id)
    formulario = ResultadoForm(request.POST or None, request.FILES or None, instance=resultado)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('resultados')
    return render(request, 'admin/resultados/edit.html', {'formulario': formulario})

@login_required
def eliminar_res(request, id):
    resultado = Resultado.objects.get(id=id)
    resultado.delete()
    messages.success(request, 'Resultado eliminado correctamente.')

    return redirect('resultados')


import hashlib
from django.shortcuts import render, redirect
from libreria.models import Usuario
from django.db import connection


@login_required
def rol_requerido(rol_esperado):
    def decorador(view_func):
        def wrapper(request, *args, **kwargs):
            if request.session.get('rol') != rol_esperado:
                return redirect('sin_permiso')  # o una página de acceso denegado
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador


@login_required
def evaluadores(request):
    evaluadores = Evaluador.objects.all()
    return render(request, 'admin/evaluadores/index.html', {'evaluadores': evaluadores})

@login_required
def crear_eva(request):
    formulario = EvaluadorForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        messages.success(request, 'Evaluador creado correctamente.')
        return redirect('evaluadores')
    return render(request, 'admin/evaluadores/crear.html', {'formulario': formulario})

@login_required
def editar_eva(request, id):
    evaluador = Evaluador.objects.get(id=id)
    formulario = EvaluadorForm(request.POST or None, request.FILES or None, instance=evaluador)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Evaluador editado correctamente.')
        return redirect('evaluadores')
    return render(request, 'admin/evaluadores/edit.html', {'formulario': formulario})

@login_required
def eliminar_eva(request, id):
    evaluador = Evaluador.objects.get(id=id)
    evaluador.delete() 
    messages.success(request, 'Evaluador eliminado correctamente.')
    return redirect('evaluadores')


@login_required
def participantes(request):
    query = request.GET.get('q', '').strip()
    examen_id = request.GET.get('examen', '').strip()

    examenes = Examen.objects.all().order_by('fecha')

    participantes = Participante.objects.none()
    examen_seleccionado = None

    if examen_id:
        examen_seleccionado = Examen.objects.filter(id=examen_id).first()
        participantes = Participante.objects.select_related('examen').filter(examen_id=examen_id).order_by('id')

        if query:
            participantes = participantes.filter(usuario__nombre__icontains=query)

    context = {
        'query': query,
        'examen_id': examen_id,
        'participantes': participantes,
        'examenes': examenes,
        'examen_seleccionado': examen_seleccionado,
    }

    return render(request, 'admin/participantes/index.html', context)



@login_required
def crear_part(request):
    formulario = ParticipanteForm(request.POST or None, request.FILES or None)    
    if request.method == 'POST':
        if formulario.is_valid():
            usuario = formulario.cleaned_data['usuario']
            examen = formulario.cleaned_data['examen']

            # Verifica si ya existe este participante con ese examen
            if Participante.objects.filter(usuario=usuario, examen=examen).exists():
                messages.error(request, f"El usuario '{usuario}' ya está registrado para el examen '{examen}'.")
            else:
                formulario.save()
                messages.success(request, 'Participante creado correctamente.')
                return redirect('participantes')

    return render(request, 'admin/participantes/crear.html', {
        'formulario': formulario
    })


@login_required
def editar_part(request, id):
    participante = Participante.objects.get(id=id)
    formulario = ParticipanteForm(request.POST or None, request.FILES or None, instance=participante)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Participante editado correctamente.')
        return redirect('participantes')
    return render(request, 'admin/participantes/edit.html', {'formulario': formulario})

@login_required
def eliminar_part(request, id):
    participante = Participante.objects.get(id=id)
    participante.delete() 
    messages.success(request, 'Participante eliminado correctamente.')
    return redirect('participantes')

@login_required
def examenes_categoria(request):
    examenes_categoria = ExamenCategoria.objects.all()
    return render(request, 'admin/examenes_categorias/index.html', {'examenes_categorias': examenes_categoria})

@login_required
def crear_exa_cat(request):
    formulario = ExamenCategoriaForm(request.POST or None)

    if request.method == 'POST':
        if formulario.is_valid():
            examen = formulario.cleaned_data['examen']
            crear_todas = formulario.cleaned_data.get('crear_todas', False)

            if crear_todas:
                # Validar: ¿ya hay alguna categoría registrada para este examen?
                ya_tiene_categorias = ExamenCategoria.objects.filter(examen=examen).exists()
                if ya_tiene_categorias:
                    messages.error(request, 'Este examen ya tiene categorías asignadas.')
                else:
                    # Crear todas las categorías para este examen
                    categorias = Categoria.objects.all()
                    for cat in categorias:
                        ExamenCategoria.objects.create(examen=examen, categoria=cat)
                    messages.success(request, 'Se asignaron todas las categorías correctamente.')
                    return redirect('examenes_categorias')
            else:
                # Validar que no exista ya esa combinación examen-categoría
                categoria = formulario.cleaned_data['categoria']
                ya_existe = ExamenCategoria.objects.filter(examen=examen, categoria=categoria).exists()
                if ya_existe:
                    formulario.add_error('categoria', 'Esta categoría ya fue asignada a este examen.')
                else:
                    formulario.save()
                    messages.success(request, 'Categoría asignada correctamente.')
                    return redirect('examenes_categorias')

    return render(request, 'admin/examenes_categorias/crear.html', {'formulario': formulario})

@login_required
def editar_exa_cat(request, id):
    examen_categoria = ExamenCategoria.objects.get(id=id)
    formulario = ExamenCategoriaForm(request.POST or None, request.FILES or None, instance=examen_categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('examenes_categorias')
    return render(request, 'admin/examenes_categorias/edit.html', {'formulario': formulario})

@login_required
def eliminar_exa_cat(request, id):
    examen_categoria = ExamenCategoria.objects.get(id=id)
    examen_categoria.delete() 
    return redirect('examenes_categorias')

@login_required
def observaciones(request):
    observaciones = Observacion.objects.all()
    return render(request, 'admin/observaciones/index.html', {'observaciones': observaciones})

@login_required
def cargar_participantes(request):
    examen_id = request.GET.get('examen_id')
    participantes = Participante.objects.filter(examen_id=examen_id).select_related('usuario')
    data = [{'id': p.id, 'nombre': str(p)} for p in participantes]
    return JsonResponse(data, safe=False)

@login_required
def crear_obs(request):
    if request.method == 'POST':
        formulario = ObservacionForm(request.POST, request.FILES)
        examen_id_post = request.POST.get('examen')
        if examen_id_post:
            formulario.fields['participante'].queryset = Participante.objects.filter(examen_id=examen_id_post)

        if formulario.is_valid():
            participante = formulario.cleaned_data['participante']
            categoria = formulario.cleaned_data['categoria']

            # Validación: ¿ya existe una observación con ese participante y esa categoría?
            existe = Observacion.objects.filter(participante=participante, categoria=categoria).exists()
            if existe:
                formulario.add_error(None, 'Este participante ya tiene una observación en esta categoría.')
            else:
                formulario.save()
                messages.success(request, 'Observación creada correctamente.')
                return redirect('observaciones')
    else:
        formulario = ObservacionForm()
        examen_id = request.GET.get('examen')
        if examen_id:
            formulario.fields['participante'].queryset = Participante.objects.filter(examen_id=examen_id)

    return render(request, 'admin/observaciones/crear.html', {'formulario': formulario})

@login_required
def editar_obs(request, id):
    observacion = Observacion.objects.get(id=id)
    formulario = ObservacionForm(request.POST or None, request.FILES or None, instance=observacion)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Observación editada correctamente.')
        return redirect('observaciones')
    return render(request, 'admin/observaciones/edit.html', {'formulario': formulario})

@login_required
def eliminar_obs(request, id):
    observacion = Observacion.objects.get(id=id)
    observacion.delete() 
    messages.success(request, 'Observación eliminada correctamente.')
    return redirect('observaciones')

@login_required
def historiales(request):
    historiales = Historial.objects.all()
    return render(request, 'admin/historiales/index.html', {'historiales': historiales})

@login_required
def crear_hist(request):
    formulario = HistorialForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        return redirect('historiales')
    return render(request, 'admin/historiales/crear.html', {'formulario': formulario})

@login_required
def editar_hist(request, id):
    historial = Historial.objects.get(id=id)
    formulario = HistorialForm(request.POST or None, request.FILES or None, instance=historial)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('historiales')
    return render(request, 'admin/historiales/edit.html', {'formulario': formulario})

@login_required
def eliminar_hist(request, id):
    historial = Historial.objects.get(id=id)
    historial.delete() 
    return redirect('historiales')

@login_required
def cinturon_categoria(request):
    cinturon_categoria = CinturonCategoria.objects.all()
    return render(request, 'admin/cinturones_categorias/index.html', {'cinturon_categoria': cinturon_categoria})

@login_required
def crear_cint_cat(request):
    formulario = CinturonCategoriaForm(request.POST or None, request.FILES or None)    
    if formulario.is_valid():
        formulario.save()
        messages.success(request, 'Item creado correctamente.')
        return redirect('cinturones_categorias')
    
    return render(request, 'admin/cinturones_categorias/crear.html', {'formulario': formulario})    

@login_required
def editar_cint_cat(request, id):
    cinturon_categoria = CinturonCategoria.objects.get(id=id)
    formulario = CinturonCategoriaForm(request.POST or None, request.FILES or None, instance=cinturon_categoria)
    if formulario.is_valid() and request.POST:
        formulario.save()
        messages.success(request, 'Item editado correctamente.')
        return redirect('cinturones_categorias')
    return render(request, 'admin/cinturones_categorias/edit.html', {'formulario': formulario})

@login_required
def eliminar_cint_cat(request, id):
    cinturon_categoria = CinturonCategoria.objects.get(id=id)
    cinturon_categoria.delete() 
    return redirect('cinturones_categorias')



# REPORTES
@login_required
def reportes(request):
    return render(request, 'admin/reportes/index.html')  

@login_required
def reporte_roles(request):
    estado = request.GET.get('estado', '').strip()
    roles = Rol.objects.all()
    

    if estado == 'activo':
        roles = roles.filter(estado=True)
    elif estado == 'inactivo':
        roles = roles.filter(estado=False)
    
    contexto = {
        "estado": estado,
        'roles': roles,
        "fecha_actual": date.today(),

    }
    return render(request, "admin/reportes/roles.html", contexto)

@login_required
def imprimir_roles(request):
    estado = request.GET.get('estado', '').strip()
    roles = Rol.objects.all()

    if estado == 'activo':
        roles = roles.filter(estado=True)
    elif estado == 'inactivo':
        roles = roles.filter(estado=False)

    
    
    template = get_template("admin/reportes/pdf_roles.html")
    contexto = {
        "estado": estado,
        'roles': roles,
        "fecha_actual": date.today(),

    }
    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response

@login_required
def reporte_usuarios(request):
    estado = request.GET.get('estado', '').strip()
    usuarios = Usuario.objects.all()
    filtro_rol = request.GET.get('rol', '')
    filtro_cinturon = request.GET.get('cinturon', '')

    if estado == 'activo':
        usuarios = usuarios.filter(est_usu=True)
    elif estado == 'inactivo':
        usuarios = usuarios.filter(est_usu=False)


    if filtro_rol:
        usuarios = usuarios.filter(rol_id=filtro_rol)

    if filtro_cinturon:
        usuarios = usuarios.filter(cinturon_id=filtro_cinturon)

    roles = Rol.objects.all()
    cinturones = Cinturon.objects.all()

    contexto = {
        "usuarios": usuarios,
        "estado": estado,
        'roles': roles,
        'cinturones': cinturones,
        'filtro_rol': filtro_rol,
        'filtro_cinturon': filtro_cinturon,
        "fecha_actual": date.today(),
    }
    return render(request, "admin/reportes/usuarios.html", contexto)


@login_required
def imprimir_usuarios(request):
    estado = request.GET.get('estado', '').strip()
    filtro_rol = request.GET.get('rol', '')
    filtro_cinturon = request.GET.get('cinturon', '')

    usuarios = Usuario.objects.all()

    if estado == 'activo':
        usuarios = usuarios.filter(est_usu=True)
    elif estado == 'inactivo':
        usuarios = usuarios.filter(est_usu=False)

    if filtro_rol:
        usuarios = usuarios.filter(rol_id=filtro_rol)

    if filtro_cinturon:
        usuarios = usuarios.filter(cinturon_id=filtro_cinturon)

    roles = Rol.objects.all()
    cinturones = Cinturon.objects.all()

    template = get_template("admin/reportes/PDF_usu.html")
    contexto = {
        "usuarios": usuarios,
        "fecha_actual": date.today(),
        'roles': roles,
        'cinturones': cinturones,
        'filtro_rol': filtro_rol,
        'filtro_cinturon': filtro_cinturon,
        "request": request,
        # si se usa logo se agrega esto
        # "logo_path": os.path.join(settings.STATIC_ROOT, "img", "logo.png"),
        
    }

    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response

@login_required
def reporte_examenes(request):
    estado = request.GET.get('estado')
    filtro_año = request.GET.get('año')

    examenes = Examen.objects.all()

    if estado == 'activo':
        examenes = examenes.filter(est_exa=True)
    elif estado == 'inactivo':
        examenes = examenes.filter(est_exa=False)

    if filtro_año:
        examenes = examenes.filter(fecha__year=filtro_año)

    años = Examen.objects.dates('fecha', 'year', order='DESC').distinct()

    return render(request, 'admin/reportes/examenes.html', {
        'examenes': examenes,
        'estado': estado,
        'filtro_año': filtro_año,
        'años': [año.year for año in años],
        'fecha_actual': date.today()
    })

@login_required
def imprimir_examenes(request):
    estado = request.GET.get('estado')
    filtro_año = request.GET.get('año')

    # ✅ Limpiar strings "None"
    if estado == 'None':
        estado = None
    if filtro_año == 'None':
        filtro_año = None

    examenes = Examen.objects.all()

    if estado == 'activo':
        examenes = examenes.filter(est_exa=True)
    elif estado == 'inactivo':
        examenes = examenes.filter(est_exa=False)

    if filtro_año:
        examenes = examenes.filter(fecha__year=filtro_año)

    años = Examen.objects.dates('fecha', 'year', order='DESC').distinct()

    template = get_template("admin/reportes/pdf_examenes.html")
    contexto = {
        'examenes': examenes,
        'estado': estado,
        'filtro_año': filtro_año,
        'años': [año.year for año in años],
        'fecha_actual': date.today()
    }

    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response

@login_required
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
        'fecha_actual': date.today(),  # Aquí añades la fecha
    }

    return render(request, 'admin/reportes/usuarios_por_examen.html', contexto)


@login_required
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


@login_required
def reporte_observaciones(request):
    observaciones = Observacion.objects.select_related('participante__usuario', 'categoria', 'evaluador')

    examen_id = request.GET.get('examen')
    categoria_id = request.GET.get('categoria')
    tipo = request.GET.get('tipo')

    if examen_id:
        observaciones = observaciones.filter(participante__examen__id=examen_id)
    if categoria_id:
        observaciones = observaciones.filter(categoria__id=categoria_id)
    if tipo:
        observaciones = observaciones.filter(tipo__icontains=tipo)

    context = {
        'observaciones': observaciones,
        'examenes': Examen.objects.all(),
        'categorias': Categoria.objects.all(),
        'fecha_actual': datetime.now().strftime('%d/%m/%Y')
    }
    return render(request, 'admin/reportes/observaciones.html', context)

@login_required
def imprimir_observaciones(request):
    observaciones = Observacion.objects.select_related('participante__usuario', 'categoria', 'evaluador')

    examen_id = request.GET.get('examen')
    categoria_id = request.GET.get('categoria')
    tipo = request.GET.get('tipo')

    if examen_id:
        observaciones = observaciones.filter(participante__examen__id=examen_id)
    if categoria_id:
        observaciones = observaciones.filter(categoria__id=categoria_id)
    if tipo:
        observaciones = observaciones.filter(tipo__icontains=tipo)

    template = get_template('admin/reportes/pdf_observaciones.html')
    context = {
        'observaciones': observaciones,
        'fecha_actual': datetime.now().strftime('%d/%m/%Y'),
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

@login_required
def reporte_resultados(request):
    resultados = Resultado.objects.select_related(
        'video__observacion__participante__usuario',
        'video__observacion__participante__examen',
        'video__observacion__categoria'
    )

    examenes = Examen.objects.all()
    categorias = Categoria.objects.all()

    examen_id = request.GET.get('examen')
    categoria_id = request.GET.get('categoria')

    if examen_id:
        resultados = resultados.filter(
            video__observacion__participante__examen__id=examen_id
        )
    if categoria_id:
        resultados = resultados.filter(
            video__observacion__categoria__id=categoria_id
        )

    return render(request, 'admin/reportes/resultados_vision.html', {
        'resultados': resultados,
        'examenes': examenes,
        'categorias': categorias
    })

@login_required
def imprimir_resultados(request):
    resultados = Resultado.objects.select_related(
        'video__observacion__participante__usuario',
        'video__observacion__participante__examen',
        'video__observacion__categoria'
    )

    examen_id = request.GET.get('examen')
    categoria_id = request.GET.get('categoria')

    if examen_id:
        resultados = resultados.filter(
            video__observacion__participante__examen__id=examen_id
        )
    if categoria_id:
        resultados = resultados.filter(
            video__observacion__categoria__id=categoria_id
        )

    template = get_template('admin/reportes/pdf_resultados.html')
    context = {
        'resultados': resultados,
        'fecha_actual': datetime.now().strftime('%d/%m/%Y'),
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@login_required
def reporte_cronograma(request):
    cronograma = CinturonCategoria.objects.filter(estado=True)
    cinturones = Cinturon.objects.all()
    categorias = Categoria.objects.all()

    cinturon_id = request.GET.get('cinturon')
    categoria_id = request.GET.get('categoria')

    if cinturon_id:
        cronograma = cronograma.filter(cinturon__id=cinturon_id)
    if categoria_id:
        cronograma = cronograma.filter(categoria__id=categoria_id)

    return render(request, 'admin/reportes/cronograma.html', {
        'cronograma': cronograma,
        'cinturones': cinturones,
        'categorias': categorias
    })



import io
@login_required
def imprimir_cronograma_pdf(request):
    cronograma = CinturonCategoria.objects.filter(estado=True)
    cinturon_id = request.GET.get('cinturon')
    categoria_id = request.GET.get('categoria')

    if cinturon_id:
        cronograma = cronograma.filter(cinturon__id=cinturon_id)
    if categoria_id:
        cronograma = cronograma.filter(categoria__id=categoria_id)

    template_path = 'admin/reportes/pdf_cronograma.html'
  
    context = {
        'cronograma': cronograma,
        'fecha_actual': date.today(),
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="cronograma_examenes.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('UTF-8')), dest=response, encoding='UTF-8')

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    return response

@login_required
def reporte_evaluadores(request):
    estado = request.GET.get('estado', '').strip()
    examen_id = request.GET.get('examen', '').strip()
    orden = request.GET.get('orden', '').strip()

    evaluadores = Evaluador.objects.all()

    if estado == 'activo':
        evaluadores = evaluadores.filter(estado=True)
    elif estado == 'inactivo':
        evaluadores = evaluadores.filter(estado=False)

    filtro_obs = Q()
    if examen_id:
        filtro_obs = Q(observacion__participante__examen_id=examen_id)

    evaluadores = evaluadores.annotate(
        total_observaciones=Count('observacion', filter=filtro_obs)
    )

    if orden == 'mas':
        evaluadores = evaluadores.order_by('-total_observaciones')
    elif orden == 'menos':
        evaluadores = evaluadores.order_by('total_observaciones')

    # 🔍 Traer observaciones filtradas por examen (si se aplica)
    observaciones = Observacion.objects.select_related('evaluador', 'participante', 'participante__usuario')

    if examen_id:
        observaciones = observaciones.filter(participante__examen_id=examen_id)

    contexto = {
        "estado": estado,
        "examen_id": examen_id,
        "orden": orden,
        "evaluadores": evaluadores,
        "examenes": Examen.objects.all(),
        "fecha_actual": date.today(),
        "observaciones": observaciones,  # extra 
    }
    return render(request, "admin/reportes/evaluadores.html", contexto)


@login_required
def imprimir_evaluadores(request):
    estado = request.GET.get('estado', '').strip()
    examen_id = request.GET.get('examen', '').strip()
    orden = request.GET.get('orden', '').strip()

    evaluadores = Evaluador.objects.all()

    if estado == 'activo':
        evaluadores = evaluadores.filter(estado=True)
    elif estado == 'inactivo':
        evaluadores = evaluadores.filter(estado=False)

    filtro_observaciones = Q()
    if examen_id:
        filtro_observaciones = Q(observacion__participante__examen_id=examen_id)

    evaluadores = evaluadores.annotate(
        total_observaciones=Count('observacion', filter=filtro_observaciones)
    )

    if orden == 'mas':
        evaluadores = evaluadores.order_by('-total_observaciones')
    elif orden == 'menos':
        evaluadores = evaluadores.order_by('total_observaciones')

    # ⚠️ NUEVO: Obtener las observaciones filtradas
    observaciones = Observacion.objects.select_related('participante__usuario', 'evaluador', 'categoria').all()
    if examen_id:
        observaciones = observaciones.filter(participante__examen_id=examen_id)

    template = get_template("admin/reportes/pdf_evaluadores.html")
    contexto = {
        "estado": estado,
        "evaluadores": evaluadores,
        "examen_id": examen_id,
        "orden": orden,
        "fecha_actual": date.today(),
        "observaciones": observaciones,  # ⚠️ Agregado al contexto
    }
    html = template.render(contexto)
    response = HttpResponse(content_type="application/pdf")
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Error al generar PDF", status=500)
    return response


@login_required
def listar_roles(request):
   
    
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    roles = Rol.objects.all().order_by('id')

    if query:
        roles = roles.filter(nombre__icontains=query)

    if estado == 'activo':
        roles = roles.filter(estado=True)
    elif estado == 'inactivo':
        roles = roles.filter(estado=False)

    paginator = Paginator(roles, 10)
    page_number = request.GET.get('page')
    roles_page = paginator.get_page(page_number)

    context = {
        'roles': roles_page,
        'query': query,
        'estado': estado,
        'paginator': paginator,
    }
    return render(request, 'admin/roles/index.html', context)


# def listar_usuarios(request):
#     query = request.GET.get('q', '').strip()
#     estado = request.GET.get('estado', '').strip()
#     filtro_rol = request.GET.get('rol', '')
#     filtro_cinturon = request.GET.get('cinturon', '')

#     usuarios = Usuario.objects.all()
#     usuarios = Usuario.objects.order_by('id')

#     if query:
#         usuarios = usuarios.filter(nombre__icontains=query)

#     if estado == 'activo':
#         usuarios = usuarios.filter(est_usu=True)
#     elif estado == 'inactivo':
#         usuarios = usuarios.filter(est_usu=False)

#     if filtro_rol:
#         usuarios = usuarios.filter(rol_id=filtro_rol)

#     if filtro_cinturon:
#         usuarios = usuarios.filter(cinturon_id=filtro_cinturon)

#     roles = Rol.objects.all()
#     cinturones = Cinturon.objects.all()

#     context = {
#         'usuarios': usuarios,
#         'query': query,
#         'estado': estado,
#         'roles': roles,
#         'cinturones': cinturones,
#         'filtro_rol': filtro_rol,
#         'filtro_cinturon': filtro_cinturon,
#         'total': usuarios.count()
#     }
#     return render(request, 'admin/usuarios/index.html', context)

@login_required
def listar_usuarios(request):
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    filtro_rol = request.GET.get('rol', '').strip()
    filtro_cinturon = request.GET.get('cinturon', '').strip()

    # ✅ UNA SOLA LÍNEA - Encadenar order_by
    usuarios = Usuario.objects.all().order_by('id')

    # Aplicar filtros
    if query:
        usuarios = usuarios.filter(nombre__icontains=query)

    if estado == 'activo':
        usuarios = usuarios.filter(est_usu=True)
    elif estado == 'inactivo':
        usuarios = usuarios.filter(est_usu=False)

    if filtro_rol:
        usuarios = usuarios.filter(rol_id=filtro_rol)

    if filtro_cinturon:
        usuarios = usuarios.filter(cinturon_id=filtro_cinturon)

    # Cargar opciones de filtros
    roles = Rol.objects.all()
    cinturones = Cinturon.objects.all()

    context = {
        'usuarios': usuarios,
        'query': query,
        'estado': estado,
        'roles': roles,
        'cinturones': cinturones,
        'filtro_rol': filtro_rol,
        'filtro_cinturon': filtro_cinturon,
        'total': usuarios.count()
    }
    
    return render(request, 'admin/usuarios/index.html', context)

@login_required
def listar_categorias(request):
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    categorias = Categoria.objects.all()
    categorias = Categoria.objects.order_by('id')

    # buscar x nombre
    if query:
        categorias = categorias.filter(nombre__icontains=query)

    # filtro x estado
    if estado == 'activo':
        categorias = categorias.filter(estado=True)
    elif estado == 'inactivo':
        categorias = categorias.filter(estado=False)

    paginator = Paginator(categorias, 10)  # 10 por pag
    page_number = request.GET.get('page')
    categorias_page = paginator.get_page(page_number)

    context = {
        'categorias': categorias_page,
        'query': query,
        'estado': estado,
        'paginator': paginator,
        'total': categorias.count()
    }
    return render(request, 'admin/categorias/index.html', context)

@login_required
def listar_cronograma(request):
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    filtro_categoria = request.GET.get('categoria', '')
    filtro_cinturon = request.GET.get('cinturon', '')

    cat_cint = CinturonCategoria.objects.all()
    cat_cint = CinturonCategoria.objects.order_by('id')

    if query:
        cat_cint = cat_cint.filter(nombre__icontains=query)

    if estado == 'activo':
        cat_cint = cat_cint.filter(estado=True)
    elif estado == 'inactivo':
        cat_cint = cat_cint.filter(estado=False)

    if filtro_categoria:
        cat_cint = cat_cint.filter(categoria_id=filtro_categoria)

    if filtro_cinturon:
        cat_cint = cat_cint.filter(cinturon_id=filtro_cinturon)

    categorias = Categoria.objects.all()
    cinturones = Cinturon.objects.all()

    context = {
        'cinturones_categorias': cat_cint,
        'query': query,
        'estado': estado,
        'categorias': categorias,
        'cinturones': cinturones,
        'filtro_categoria': filtro_categoria,
        'filtro_cinturon': filtro_cinturon,
        'total': cat_cint.count()
    }
    return render(request, 'admin/cinturones_categorias/index.html', context)

@login_required
def listar_examenes(request):
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    fecha_filtro = request.GET.get('fecha')
    anio_filtro = request.GET.get('anio')

    examenes = Examen.objects.all()
    examenes = Examen.objects.order_by('id')

    # Búsqueda por codigo
    if query:
        examenes = examenes.filter(codigo__icontains=query)

    # Filtro por estado (True o False)
    if estado == 'activo':
        examenes = examenes.filter(est_exa=True)
    elif estado == 'inactivo':
        examenes = examenes.filter(est_exa=False)

    #buscar por fecha y año

    if fecha_filtro:
        examenes = examenes.filter(fecha=fecha_filtro)
    elif anio_filtro:
        examenes = examenes.filter(fecha__year=anio_filtro)


    paginator = Paginator(examenes, 10)  # 10 por página
    page_number = request.GET.get('page')
    examenes_page = paginator.get_page(page_number)

    context = {
        'examenes': examenes_page,
        'query': query,
        'estado': estado,
        'paginator': paginator,
        'fecha_filtro': fecha_filtro,
        'anio_filtro': anio_filtro,
        
    }
    
    return render(request, 'admin/examenes/index.html', context)

@login_required
def listar_observaciones(request):
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    filtro_categoria = request.GET.get('categoria', '')
    filtro_examen = request.GET.get('examen', '')

    observaciones = Observacion.objects.all()
    observaciones = Observacion.objects.order_by('id')

    # Búsqueda por nombre
    if query:
        observaciones = observaciones.filter(nombre__icontains=query)

    # Filtro por estado (True o False)
    if estado == 'activo':
        observaciones = observaciones.filter(estado=True)
    elif estado == 'inactivo':
        observaciones = observaciones.filter(estado=False)

    if filtro_categoria:
        observaciones = observaciones.filter(categoria_id=filtro_categoria)

    if filtro_examen:
        observaciones = observaciones.filter(participante__examen_id=filtro_examen)


    categorias = Categoria.objects.all()
    examenes = Examen.objects.all()

    paginator = Paginator(observaciones, 10)  # 10 por página
    page_number = request.GET.get('page')
    observaciones_page = paginator.get_page(page_number)


    context = {
        'observaciones': observaciones_page,
        'query': query,
        'estado': estado,
        'paginator': paginator,
        'categorias': categorias,
        'examenes': examenes, 
        'total': observaciones.count()
    }

    return render(request, 'admin/observaciones/index.html', context)

@login_required
def obtener_participantes(request):
    examen_id = request.GET.get('examen_id')
    participantes = Participante.objects.filter(examen_id=examen_id)
    data = {p.id: str(p) for p in participantes}
    return JsonResponse(data)

@login_required
def listar_evaluadores(request):
    query = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()

    evaluadores = Evaluador.objects.all()
    evaluadores = Evaluador.objects.order_by('id')

    # Búsqueda por nombre desde usuario
    if query:
        evaluadores = evaluadores.filter(usuario__nombre__icontains=query)

    # Filtro por estado (True o False)
    if estado == 'activo':
        evaluadores = evaluadores.filter(estado=True)
    elif estado == 'inactivo':
        evaluadores = evaluadores.filter(estado=False)

    paginator = Paginator(evaluadores, 10)  # 10 por página
    page_number = request.GET.get('page')
    evaluadores_page = paginator.get_page(page_number)

    context = {
        'evaluadores': evaluadores_page,
        'query': query,
        'estado': estado,
        'paginator': paginator,
    }
    return render(request, 'admin/evaluadores/index.html', context)

@login_required
def listar_videos(request):
    query = request.GET.get('q', '')
    estado = request.GET.get('estado', '')
    fecha_filtro = request.GET.get('fecha')
    anio_filtro = request.GET.get('anio')

    videos = Video.objects.all()
    videos = Video.objects.order_by('id')

    # Búsqueda por codigo
    if query:
        videos = videos.filter(codigo__icontains=query)

    # Filtro por estado (True o False)
    if estado == 'activo':
        videos = videos.filter(est_analisis=True)
    elif estado == 'inactivo':
        videos = videos.filter(est_analisis=False)

    #buscar por fecha y año

    if fecha_filtro:
        videos = videos.filter(fecha=fecha_filtro)
    elif anio_filtro:
        videos = videos.filter(fecha__year=anio_filtro)


    paginator = Paginator(videos, 10)  # 10 por página
    page_number = request.GET.get('page')
    videos_page = paginator.get_page(page_number)

    context = {
        'videos': videos_page,
        'query': query,
        'estado': estado,
        'paginator': paginator,
        'fecha_filtro': fecha_filtro,
        'anio_filtro': anio_filtro,
        
    }
    
    return render(request, 'admin/videos/index.html', context)

@login_required
def listar_resultados(request):
    orden = request.GET.get('orden', '')
    estado = request.GET.get('estado', '').strip()
    errores = request.GET.get('errores', '').strip()

    # resultados = Resultado.objects.all()
    resultados = Resultado.objects.order_by('id')
    # Filtro por errores
    if errores == 'mayores3':
        resultados = resultados.filter(errores__gt=3)

    # Filtro por estado
    if estado == 'activo':
        resultados = resultados.filter(estado=True)
    elif estado == 'inactivo':
        resultados = resultados.filter(estado=False)

    # Orden por puntuación
    if orden == 'mayor':
        resultados = resultados.order_by('-puntaje')
    elif orden == 'menor':
        resultados = resultados.order_by('puntaje')
    else:
        resultados = resultados.order_by('id')  # orden por defecto

    paginator = Paginator(resultados, 10)  # 10 resultados por página
    page_number = request.GET.get('page')
    resultados_page = paginator.get_page(page_number)

    context = {
        'resultados': resultados_page,
        'orden': orden,
        'estado': estado,
        'paginator': paginator,
        'errores': errores,
        'total': resultados.count()
    }

    return render(request, 'admin/resultados/index.html', context)



#buckupe 
# @login_required
# def backup_database(request):
#     # Ajusta estos datos con los de tu configuración real
#     if not request.user.usuario.rol.nombre == "Administrador":
#         return HttpResponseForbidden("No tienes permiso para hacer el backup.")

#     db_name = 'nombre_de_tu_base'
#     db_user = 'tu_usuario'
#     db_password = 'tu_contraseña'
#     db_host = 'localhost'
#     db_port = '5432'

#     fecha = datetime.datetime.now().strftime('%Y%m%d_%H%M')
#     nombre_archivo = f"backup_{fecha}.sql"

#     try:
#         comando = [
#             'pg_dump',
#             '-h', db_host,
#             '-p', db_port,
#             '-U', db_user,
#             '-F', 'p',  # formato texto plano (.sql)
#             db_name
#         ]
        
#         # Define variable de entorno para la contraseña
#         env = {'PGPASSWORD': db_password}

#         resultado = subprocess.run(comando, env=env, capture_output=True, check=True)
#         contenido_backup = resultado.stdout

#         response = HttpResponse(contenido_backup, content_type='application/sql')
#         response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
#         return response

#     except subprocess.CalledProcessError as e:
#         return HttpResponse(f"Error al realizar el backup: {e.stderr.decode()}", status=500)


def backup(request):
    
    output = StringIO()
    call_command('dumpdata', format='json', indent=2, stdout=output)
    response = HttpResponse(output.getvalue(), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=backup.json'
    return response




mp_pose = mp.solutions.pose

# def analizar_video(ruta=None):
#     pose = mp_pose.Pose()
#     cap = cv2.VideoCapture(0 if not ruta else ruta)  # usa cámara si no hay ruta

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Conversión de color para Mediapipe
#         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         results = pose.process(frame_rgb)

#         # Dibujar puntos del cuerpo
#         mp.solutions.drawing_utils.draw_landmarks(
#             frame,
#             results.pose_landmarks,
#             mp_pose.POSE_CONNECTIONS
#         )

#         cv2.imshow("Análisis en tiempo real", frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):  # presiona Q para cerrar
#             break

#     cap.release()
#     cv2.destroyAllWindows()

# def ver_analisis_real(request):
#     ruta = request.GET.get('video')
#     if ruta:
#         analizar_video(ruta)  # <--- Ejecuta directamente
#         return HttpResponse("Análisis completado. Cierra la ventana para continuar.")
#     else:
#         return HttpResponse("No se proporcionó un video.")
    






mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def calcular_angulo(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    angulo = np.degrees(
        np.arctan2(c[1]-b[1], c[0]-b[0]) -
        np.arctan2(a[1]-b[1], a[0]-b[0])
    )
    angulo = abs(angulo)
    if angulo > 180:
        angulo = 360 - angulo
    return angulo


def generar_video(ruta_video):
    cap = cv2.VideoCapture(ruta_video)
    pose = mp_pose.Pose()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = pose.process(rgb)
        mp_drawing.draw_landmarks(frame, resultados.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if resultados.pose_landmarks:
            landmarks = resultados.pose_landmarks.landmark

            hombro = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            codo = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            muñeca = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            angulo_codo = calcular_angulo(hombro, codo, muñeca)

            cv2.putText(frame, f"Codo: {int(angulo_codo)}°",
                        tuple(np.multiply(codo, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

from .vision.analisis_videos import analizar_video_en_stream

@login_required
def ver_analisis_real(request):
    ruta = request.GET.get('video')
    if ruta:
        # Decodificar la URL 
        ruta = unquote(ruta)
        # Obtener la ruta completa del archivo
        ruta_completa = os.path.join(settings.MEDIA_ROOT, ruta.replace('/media/', ''))
        
        try:
            return StreamingHttpResponse(
                analizar_video_en_stream(ruta_completa),
                content_type='multipart/x-mixed-replace; boundary=frame'
            )
        except Exception as e:
            return HttpResponse(f"Error al analizar el video: {str(e)}")
    else:
        return HttpResponse("No se proporcionó un video.")


from django.shortcuts import render

def pagina_analisis(request):
    ruta = request.GET.get("video")
    return render(request, "vision/analisis.html", {"ruta": ruta})


from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.translation import gettext as _


# @login_required
# def inicio(request):
#     # Redirige/renderiza según el rol del usuario (con guardas por si no tiene rol)
#     rol_obj = getattr(request.user, 'rol', None)
#     rol_nombre = rol_obj.nombre.lower() if rol_obj and getattr(rol_obj, 'nombre', None) else ''

#     if rol_nombre == 'administrador':
#         return render(request, 'admin/paginas/inicio.html')
#     elif rol_nombre == 'instructor':
#         return render(request, 'instructor/paginas/inicio.html')
#     elif rol_nombre == 'estudiante':
#         return render(request, 'estudiante/paginas/inicio.html')
#     else:
#         messages.error(request, _('No tienes permiso para acceder.'))
#         logout(request)
#         return redirect('login')

from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from .models import CodigoVerificacion, DispositivoConfiable
import secrets
from libreria.utils import get_client_ip, get_device_name
# def get_client_ip(request):
#     """Obtiene la IP real del cliente"""
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

# def get_device_name(request):
#     """Genera un nombre legible para el dispositivo"""
#     user_agent = request.META.get('HTTP_USER_AGENT', '')
    
#     if 'Windows' in user_agent:
#         device = 'Windows PC'
#     elif 'Mac' in user_agent:
#         device = 'Mac'
#     elif 'Linux' in user_agent:
#         device = 'Linux PC'
#     elif 'iPhone' in user_agent:
#         device = 'iPhone'
#     elif 'Android' in user_agent:
#         device = 'Android'
#     else:
#         device = 'Dispositivo desconocido'
    
#     if 'Chrome' in user_agent:
#         browser = 'Chrome'
#     elif 'Firefox' in user_agent:
#         browser = 'Firefox'
#     elif 'Safari' in user_agent and 'Chrome' not in user_agent:
#         browser = 'Safari'
#     elif 'Edge' in user_agent:
#         browser = 'Edge'
#     else:
#         browser = 'Navegador'
    
#     return f"{device} - {browser}"

def login_view(request):
    """Login con verificación en 2 pasos"""
    if request.user.is_authenticated:
        return redirect('inicio')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        usuario = authenticate(request, email=email, password=password)
        
        if usuario is not None:
            # Verificar si este dispositivo es confiable
            token_dispositivo = request.COOKIES.get('dispositivo_confiable')
            ip_cliente = get_client_ip(request)
            
            dispositivo_confiable = None
            if token_dispositivo:
                try:
                    dispositivo_confiable = DispositivoConfiable.objects.get(
                        token=token_dispositivo,
                        usuario=usuario,
                        activo=True
                    )
                    # Actualizar último uso
                    dispositivo_confiable.save()
                except DispositivoConfiable.DoesNotExist:
                    pass
            
            # Si el dispositivo es confiable, login directo
            if dispositivo_confiable:
                login(request, usuario)
                messages.success(request, f'¡Bienvenido de nuevo, {usuario.nombre}!')
                return redirect('inicio')
            
            # Si no es confiable, enviar código de verificación
            # Generar código
            codigo = CodigoVerificacion.generar_codigo()
            
            # Guardar código en BD
            CodigoVerificacion.objects.create(
                usuario=usuario,
                codigo=codigo,
                ip_address=ip_cliente
            )
            
            # Enviar email
            try:
                send_mail(
                    subject='Código de Verificación - Sistema Karate',
                    message=f'''
Hola {usuario.nombre},

Tu código de verificación es: {codigo}

Este código expirará en 5 minutos.

Si no intentaste iniciar sesión, ignora este mensaje.

---
Sistema de Gestión de Karate
Asociación Departamental de La Paz
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[usuario.email],
                    fail_silently=False,
                )
                
                # Guardar el ID del usuario en sesión
                request.session['usuario_pendiente_2fa'] = usuario.id
                request.session['ip_2fa'] = ip_cliente
                
                messages.info(request, f'📧 Hemos enviado un código de verificación a {usuario.email}')
                return redirect('verificar_codigo')
                
            except Exception as e:
                messages.error(request, f'Error al enviar el código: {str(e)}')
                return redirect('login')
        else:
            messages.error(request, '❌ Email o contraseña incorrectos')
    
    return render(request, 'registration/login.html')

def verificar_codigo(request):
    """Vista para verificar el código de 2FA"""
    # Verificar que hay un usuario pendiente de verificación
    usuario_id = request.session.get('usuario_pendiente_2fa')
    if not usuario_id:
        messages.error(request, 'Sesión expirada. Inicia sesión nuevamente.')
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuario no encontrado.')
        return redirect('login')
    
    if request.method == 'POST':
        codigo_ingresado = request.POST.get('codigo', '').strip()
        confiar_dispositivo = request.POST.get('confiar_dispositivo') == 'on'
        
        # Buscar código válido
        try:
            codigo_obj = CodigoVerificacion.objects.filter(
                usuario=usuario,
                codigo=codigo_ingresado,
                usado=False
            ).latest('creado')
            
            if codigo_obj.esta_vigente():
                # Código correcto y vigente
                codigo_obj.usado = True
                codigo_obj.save()
                
                # Hacer login
                login(request, usuario, backend='libreria.backends.SHA256AuthBackend')
                
                # Si marcó "confiar en este dispositivo"
                response = redirect('inicio')
                if confiar_dispositivo:
                    token = DispositivoConfiable.generar_token()
                    DispositivoConfiable.objects.create(
                        usuario=usuario,
                        token=token,
                        nombre_dispositivo=get_device_name(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        ip_address=get_client_ip(request)
                    )
                    # Guardar token en cookie (30 días)
                    response.set_cookie(
                        'dispositivo_confiable',
                        token,
                        max_age=30*24*60*60,  # 30 días
                        httponly=True,
                        secure=not settings.DEBUG  # True en producción
                    )
                    messages.success(request, f'✓ ¡Bienvenido, {usuario.nombre}! Este dispositivo ahora es confiable.')
                else:
                    messages.success(request, f'✓ ¡Bienvenido, {usuario.nombre}!')
                
                # Limpiar sesión
                del request.session['usuario_pendiente_2fa']
                if 'ip_2fa' in request.session:
                    del request.session['ip_2fa']
                
                return response
            else:
                messages.error(request, '⏱️ El código ha expirado. Solicita uno nuevo.')
        except CodigoVerificacion.DoesNotExist:
            messages.error(request, '❌ Código incorrecto. Intenta de nuevo.')
    
    return render(request, 'registration/verificar_codigo.html', {
        'email': usuario.email,
        'nombre': usuario.nombre
    })


def reenviar_codigo(request):
    """Reenviar código de verificación"""
    usuario_id = request.session.get('usuario_pendiente_2fa')
    if not usuario_id:
        messages.error(request, 'Sesión expirada.')
        return redirect('login')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
        
        # Generar nuevo código
        codigo = CodigoVerificacion.generar_codigo()
        
        CodigoVerificacion.objects.create(
            usuario=usuario,
            codigo=codigo,
            ip_address=get_client_ip(request)
        )
        
        # Enviar email
        send_mail(
            subject='Nuevo Código de Verificación - Sistema Karate',
            message=f'''
Hola {usuario.nombre},

Tu nuevo código de verificación es: {codigo}

Este código expirará en 5 minutos.

---
Sistema de Gestión de Karate
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[usuario.email],
            fail_silently=False,
        )
        
        messages.success(request, '📧 Nuevo código enviado a tu email')
    except Exception as e:
        messages.error(request, f'Error al reenviar código: {str(e)}')
    
    return redirect('verificar_codigo')


def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('login')

@login_required(login_url='login')
def inicio(request):
    """Vista principal que redirige según el rol del usuario"""
    if not hasattr(request.user, 'rol') or not request.user.rol:
        messages.error(request, 'No tienes un rol asignado.')
        logout(request)
        return redirect('login')

    rol_nombre = request.user.rol.nombre.lower()

    if rol_nombre == 'administrador':
        return render(request, 'admin/paginas/inicio.html', {'user': request.user})
    elif rol_nombre == 'instructor':
        return render(request, 'instructor/inicio_instructor.html', {'user': request.user})
    elif rol_nombre == 'estudiante':
        return render(request, 'estudiante/paginas/inicio.html', {'user': request.user})
    else:
        messages.error(request, 'Rol no reconocido.')
        return redirect('logout')



# funciones para verificar roles
def es_admin(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol.nombre.lower() == 'administrador'

def es_instructor(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol.nombre.lower() == 'instructor'

def es_estudiante(user):
    return user.is_authenticated and hasattr(user, 'rol') and user.rol.nombre.lower() == 'estudiante'

# Decorador personalizado para proteger vistas por rol
def rol_required(allowed_roles):
    def decorator(view_func):
        @login_required(login_url='login')
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, 'rol') or not request.user.rol:
                messages.error(request, 'No tienes un rol asignado.')
                return redirect('login')
            
            if request.user.rol.nombre.lower() in [r.lower() for r in allowed_roles]:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'No tienes permiso para acceder a esta sección.')
            return redirect('inicio')
        return _wrapped_view
    return decorator



@login_required
@user_passes_test(es_admin)
def vista_admin(request):
    return render(request, 'admin/inicio.html')

@login_required
@user_passes_test(es_instructor)
def vista_instructor(request):
    return render(request, 'instructor/dashboard.html')

@login_required
@user_passes_test(es_estudiante)
def vista_estudiante(request):
    return render(request, 'estudiante/dashboard.html')


@login_required
def perfil(request):
    """Vista del perfil del usuario"""
    return render(request, 'admin/perfil/perfil.html', {
        'user': request.user
    })

@login_required
def editar_perfil(request):
    """Vista para editar información personal"""
    usuario = request.user
    
    if request.method == 'POST':
        # Actualizar solo campos permitidos
        usuario.celular = request.POST.get('celular')
        usuario.direccion = request.POST.get('direccion')
        usuario.observacion = request.POST.get('observacion', '')
        
        try:
            usuario.save()
            messages.success(request, '✓ Información actualizada correctamente')
            return redirect('perfil')
        except Exception as e:
            messages.error(request, f'Error al actualizar: {str(e)}')
    
    return render(request, 'admin/perfil/editar.html', {'user': usuario})

@login_required
def cambiar_password(request):
    """Vista para cambiar contraseña"""
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmacion = request.POST.get('password_confirmacion')
        
        # Verificar contraseña actual
        if not request.user.check_password(password_actual):
            messages.error(request, '✗ La contraseña actual es incorrecta')
            return redirect('cambiar_password')
        
        # Verificar que las nuevas coincidan
        if password_nueva != password_confirmacion:
            messages.error(request, '✗ Las contraseñas nuevas no coinciden')
            return redirect('cambiar_password')
        
        # Verificar longitud
        if len(password_nueva) < 8:
            messages.error(request, '✗ La contraseña debe tener al menos 8 caracteres')
            return redirect('cambiar_password')
        
        # Cambiar contraseña
        import hashlib
        request.user.password = hashlib.sha256(password_nueva.encode()).digest()
        request.user.save()
        
        messages.success(request, '✓ Contraseña cambiada correctamente. Por seguridad, vuelve a iniciar sesión.')
        logout(request)
        return redirect('login')
    
    return render(request, 'admin/perfil/cambiar_password.html')



@login_required
def dispositivos_confiables(request):
    """Ver y gestionar dispositivos confiables"""
    dispositivos = DispositivoConfiable.objects.filter(
        usuario=request.user,
        activo=True
    ).order_by('-ultimo_uso')
    
    return render(request, 'admin/perfil/dispositivos.html', {
        'dispositivos': dispositivos
    })

@login_required
def eliminar_dispositivo(request, id):
    """Eliminar un dispositivo confiable"""
    try:
        dispositivo = DispositivoConfiable.objects.get(
            id=id,
            usuario=request.user
        )
        dispositivo.activo = False
        dispositivo.save()
        messages.success(request, '✓ Dispositivo eliminado correctamente')
    except DispositivoConfiable.DoesNotExist:
        messages.error(request, 'Dispositivo no encontrado')
    
    return redirect('dispositivos_confiables')



# consumi api
import requests
from django.http import JsonResponse

def prueba_api_externa(request):
    response = requests.get('https://jsonplaceholder.typicode.com/todos/1')
    data = response.json()
    return JsonResponse(data)