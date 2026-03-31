# url propias de la aplciacion
from django.urls import path 
from . import views 
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inicio/', views.inicio, name='inicio'),
    path('admin/dashboard/', views.vista_admin, name='vista_admin'),
    path('instructor/dashboard/', views.vista_instructor, name='vista_instructor'),
    path('estudiante/dashboard/', views.vista_estudiante, name='vista_estudiante'),
   
    # Rutas protegidas por rol
    # path('roles/', views.roles, name='roles'),
    # path('usuarios/', views.usuarios, name='usuarios'),

    path('nosotros/', views.nosotros, name='nosotros'),
    # path('roles/', views.roles, name='roles'),
    path('roles/crear', views.crear_rol, name='crear_rol'),
    path('roles/edit/<int:id>/', views.editar_rol, name='editar_rol'),
    path('eliminar_rol/<int:id>/', views.eliminar_rol, name='eliminar_rol'),
    # path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/crear', views.crear_usu, name='crear_usu'),
    path('usuarios/edit/<int:id>/', views.editar_usu, name='editar_usu'),
    path('eliminar_usu/<int:id>/', views.eliminar_usu, name='eliminar_usu'),
    path('cinturones/', views.cinturones, name='cinturones'),
    path('cinturones/crear_cint', views.crear_cint, name='crear_cint'),
    path('cinturones/edit/<int:id>/', views.editar_cint, name='editar_cint'),
    path('eliminar_cint/<int:id>/', views.eliminar_cint, name='eliminar_cint'),
    # path('categorias/', views.categorias, name='categorias'),
    path('categorias/crear_cat', views.crear_cat, name='crear_cat'),
    path('categorias/edit/<int:id>/', views.editar_cat, name='editar_cat'),
    path('eliminar_cat/<int:id>/', views.eliminar_cat, name='eliminar_cat'),
    # path('examenes/', views.examenes, name='examenes'),
    path('examenes/crear_exa', views.crear_exa, name='crear_exa'),
    path('examenes/edit/<int:id>/', views.editar_exa, name='editar_exa'),
    path('eliminar_exa/<int:id>/', views.eliminar_exa, name='eliminar_exa'),
    # path('videos/', views.videos, name='videos'),
    path('videos/crear_vid', views.crear_vid, name='crear_vid'),
    path('videos/edit/<int:id>/', views.editar_vid, name='editar_vid'),
    path('eliminar_vid/<int:id>/', views.eliminar_vid, name='eliminar_vid'),
    # path('resultados/', views.resultados, name='resultados'),
    path('resultados/crear_res', views.crear_res, name='crear_res'),

    path('resultados/edit/<int:id>/', views.editar_res, name='editar_res'),

    path('eliminar_res/<int:id>/', views.eliminar_res, name='eliminar_res'),
    # path('login/', views.login_view, name='login'),
    # path('evaluadores/', views.evaluadores, name='evaluadores'),
    path('evaluadores/crear_eva', views.crear_eva, name='crear_eva'),
    path('evaluadores/edit/<int:id>/', views.editar_eva, name='editar_eva'),
    path('eliminar_eva/<int:id>/', views.eliminar_eva, name='eliminar_eva'),
    path('participantes/', views.participantes, name='participantes'),
    path('participantes/crear_part', views.crear_part, name='crear_part'),
    path('participantes/edit/<int:id>/', views.editar_part, name='editar_part'),
    path('eliminar_part/<int:id>/', views.eliminar_part, name='eliminar_part'),
    path('examenes_categorias/', views.examenes_categoria, name='examenes_categorias'),
    path('examenes_categorias/crear_exa_cat', views.crear_exa_cat, name='crear_exa_cat'),
    path('examenes_categorias/edit/<int:id>/', views.editar_exa_cat, name='editar_exa_cat'),
    path('eliminar_exa_cat/<int:id>/', views.eliminar_exa_cat, name='eliminar_exa_cat'),
    # path('observaciones/', views.observaciones, name='observaciones'),

    path('ajax/cargar-participantes/', views.cargar_participantes, name='ajax_cargar_participantes'),
    path('observaciones/crear_obs', views.crear_obs, name='crear_obs'),
    path('observaciones/edit/<int:id>/', views.editar_obs, name='editar_obs'),

    path('eliminar_obs/<int:id>/', views.eliminar_obs, name='eliminar_obs'),
    path('historiales/', views.historiales, name='historiales'),
    path('historiales/crear_hist', views.crear_hist, name='crear_hist'),
    path('historiales/edit/<int:id>/', views.editar_hist, name='editar_hist'),
    path('eliminar_hist/<int:id>/', views.eliminar_hist, name='eliminar_hist'),
    # path('cinturones_categorias/', views.cinturon_categoria, name='cinturones_categorias'),
    path('cinturones_categorias/crear_cint_cat', views.crear_cint_cat, name='crear_cint_cat'),
    path('cinturones_categorias/edit/<int:id>/', views.editar_cint_cat, name='editar_cint_cat'),
    path('eliminar_cint_cat/<int:id>/', views.eliminar_cint_cat, name='eliminar_cint_cat'),

    #REPORTES
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/usuarios_por_examen/', views.reporte_usuarios_por_examen, name='reporte_usuarios_por_examen'),
    path('reportes/usuarios/', views.reporte_usuarios, name='reporte_usuarios'),
    path('reportes/imprimir_usuarios_por_examen/', views.imprimir_usuarios_por_examen, name='imprimir_usuarios_por_examen'),
    path('reportes/usuarios/', views.reporte_usuarios, name='reporte_usuarios'),
    path('reportes/usuarios/imprimir/', views.imprimir_usuarios, name='imprimir_usuarios'),
    path('reporte/observaciones/', views.reporte_observaciones, name='reporte_observaciones'),
    path('reporte/observaciones/imprimir/', views.imprimir_observaciones, name='imprimir_observaciones'),
    path('reporte/resultados-vision/', views.reporte_resultados, name='reporte_resultados'),
    path('reporte/resultados-vision/imprimir/', views.imprimir_resultados, name='imprimir_resultados'),
    path('reportes/cronograma/', views.reporte_cronograma, name='reporte_cronograma'),
    path('reporte/cronograma/pdf/', views.imprimir_cronograma_pdf, name='imprimir_cronograma_pdf'),
    path('reporte/examenes/', views.reporte_examenes, name='reporte_examenes'),
    path('reporte/examenes/pdf/', views.imprimir_examenes, name='imprimir_examenes'),
    path('reportes/roles/', views.reporte_roles, name='reporte_roles'),
    path('reportes/roles/imprimir/', views.imprimir_roles, name='imprimir_roles'),
    path('reportes/evaluadores/', views.reporte_evaluadores, name='reporte_evaluadores'),
    path('reportes/evaluadores/imprimir/', views.imprimir_evaluadores, name='imprimir_evaluadores'),


    #listas
    path('roles/', views.listar_roles, name='roles'),
    path('usuarios/', views.listar_usuarios, name='usuarios'),
    path('categorias/', views.listar_categorias, name='categorias'),
    path('cinturones_categorias/', views.listar_cronograma, name='cinturones_categorias'),
    path('examenes/',views.listar_examenes, name='examenes'),
    path('observaciones/',views.listar_observaciones, name='observaciones'),
    path('obtener_participantes/', views.obtener_participantes, name='obtener_participantes'),
    path('evaluadores/', views.listar_evaluadores, name='evaluadores'),
    path('videos/', views.listar_videos, name='videos'),
    path('resultados/', views.listar_resultados, name='resultados'),
    path('instructor/', views.vista_instructor, name='vista_instructor'),
    # path('admin/backup/', views.backup_database, name='backup_db'),
    path('admin/backup/', views.backup, name='backup'),
    path('analisis_real/', views.ver_analisis_real, name='ver_analisis_real'),
    path('ver_analisis_real/', views.ver_analisis_real, name='ver_analisis_real'),
    path('analisis/', views.pagina_analisis, name='pagina_analisis'),
    path('video_feed/', views.analizar_video_en_stream, name='video_feed'),
    # Perfil de usuario
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/cambiar-password/', views.cambiar_password, name='cambiar_password'),

    # Autenticación 2FA
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('reenviar-codigo/', views.reenviar_codigo, name='reenviar_codigo'),

    # Gestión de dispositivos en el perfil
    path('perfil/dispositivos/', views.dispositivos_confiables, name='dispositivos_confiables'),
    path('perfil/dispositivos/eliminar/<int:id>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),

    #consumir API de pruebi
    path('prueba-api/', views.prueba_api_externa, name='prueba_api_externa'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
