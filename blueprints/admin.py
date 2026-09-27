"""
Panel de administrador: aprobar o rechazar el registro de profesionales
antes de que aparezcan públicamente (cargo "administrador").
"""
from flask import Blueprint, render_template, redirect, url_for, flash

from utilidades import exigir_admin, cliente_sesion

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@exigir_admin
def panel():
    sb_admin = cliente_sesion()

    pendientes = sb_admin.table("profesionales").select(
        "*, perfiles(nombre, telefono)"
    ).eq("estado", "pendiente").order("creado_en").execute()

    aprobados = sb_admin.table("profesionales").select(
        "id", count="exact"
    ).eq("estado", "aprobado").execute()

    servicios = sb_admin.table("servicios").select("id", count="exact").execute()

    return render_template(
        "admin/panel.html",
        pendientes=pendientes.data,
        total_aprobados=aprobados.count or 0,
        total_servicios=servicios.count or 0,
    )


@admin_bp.route("/profesionales/<profesional_id>/aprobar", methods=["POST"])
@exigir_admin
def aprobar(profesional_id):
    sb_admin = cliente_sesion()
    sb_admin.table("profesionales").update({"estado": "aprobado"}).eq(
        "id", profesional_id
    ).execute()
    flash("Profesional aprobado. Ya aparece en el listado público.", "success")
    return redirect(url_for("admin.panel"))


@admin_bp.route("/profesionales/<profesional_id>/rechazar", methods=["POST"])
@exigir_admin
def rechazar(profesional_id):
    sb_admin = cliente_sesion()
    sb_admin.table("profesionales").update({"estado": "rechazado"}).eq(
        "id", profesional_id
    ).execute()
    flash("Registro de profesional rechazado.", "success")
    return redirect(url_for("admin.panel"))
