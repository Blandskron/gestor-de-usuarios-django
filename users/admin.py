from django.contrib import admin

# El modelo User incorporado por Django ya está registrado con un formulario
# seguro para contraseñas, grupos y permisos. Solo personalizamos los títulos.
admin.site.site_header = "Gestor de usuarios — Administración"
admin.site.site_title = "Gestor de usuarios"
admin.site.index_title = "Datos del laboratorio"
