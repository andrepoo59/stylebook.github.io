
"""HU-04 Registro de proveedor (profesional del establecimiento)
HU-07 Consultar proveedor (perfil público del profesional)"""
"""
HU-04 Registro de proveedor (profesional del establecimiento)
HU-07 Consultar proveedor (perfil público del profesional)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from supabase_client import sb
from utilidades import exigir_sesion, cliente_sesion

profesionales_bp = Blueprint("profesionales", __name__)


@profesionales_bp.route("/profesionales")
def listar():
    """HU-07: cualquiera puede consultar la lista de profesionales."""
    respuesta = sb.table("profesionales").select(
        "*, perfiles(nombre)"
    ).eq("estado", "aprobado").order("creado_en").execute()
    return render_template("profesionales/listar.html", profesionales=respuesta.data)


@profesionales_bp.route("/profesionales/<profesional_id>")
def detalle(profesional_id):
    """HU-07: perfil público de un profesional y sus servicios."""
    profesional = sb.table("profesionales").select(
        "*, perfiles(nombre)"
    ).eq("id", profesional_id).single().execute()

    servicios = sb.table("servicios").select("*").eq(
        "profesional_id", profesional_id
    ).eq("activo", True).execute()

    return render_template(
        "profesionales/detalle.html",
        profesional=profesional.data,
        servicios=servicios.data,
    )


@profesionales_bp.route("/profesionales/registro", methods=["GET", "POST"])
@exigir_sesion
def registro():
    """HU-04: un usuario con sesión se registra como profesional del negocio."""
    sb_usuario = cliente_sesion()

    if request.method == "GET":
        return render_template("profesionales/registro.html")

    especialidad = request.form.get("especialidad", "").strip()
    descripcion = request.form.get("descripcion", "").strip()
    telefono = request.form.get("telefono", "").strip()
    anios_experiencia = request.form.get("anios_experiencia", "0")

    if not especialidad:
        flash("La especialidad es obligatoria (ej. Barbería, Colorimetría, Uñas).", "error")
        return render_template("profesionales/registro.html")

    try:
        sb_usuario.table("profesionales").insert({
            "perfil_id": session["user_id"],
            "especialidad": especialidad,
            "descripcion": descripcion,
            "telefono": telefono,
            "anios_experiencia": int(anios_experiencia or 0),
        }).execute()
        sb_usuario.table("perfiles").update({"rol": "profesional"}).eq(
            "id", session["user_id"]
        ).execute()
    except Exception as error:
        flash(f"No se pudo completar el registro como profesional: {error}", "error")
        return render_template("profesionales/registro.html")

    flash("Registro como profesional completado. Ya puedes cargar tus servicios.", "success")
    return redirect(url_for("servicios.gestionar"))
