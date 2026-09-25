
"""HU-03 Gestión del perfil"""
"""
HU-03 Gestión del perfil
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from utilidades import exigir_sesion, cliente_sesion

perfil_bp = Blueprint("perfil", __name__)


@perfil_bp.route("/perfil")
@exigir_sesion
def ver():
    sb_usuario = cliente_sesion()
    respuesta = sb_usuario.table("perfiles").select("*").eq(
        "id", session["user_id"]
    ).single().execute()
    return render_template("perfil/ver.html", perfil=respuesta.data)


@perfil_bp.route("/perfil/editar", methods=["GET", "POST"])
@exigir_sesion
def editar():
    sb_usuario = cliente_sesion()

    if request.method == "GET":
        respuesta = sb_usuario.table("perfiles").select("*").eq(
            "id", session["user_id"]
        ).single().execute()
        return render_template("perfil/editar.html", perfil=respuesta.data)

    nombre = request.form.get("nombre", "").strip()
    telefono = request.form.get("telefono", "").strip()

    if not nombre:
        flash("El nombre no puede quedar vacío.", "error")
        return redirect(url_for("perfil.editar"))

    sb_usuario.table("perfiles").update({
        "nombre": nombre,
        "telefono": telefono,
    }).eq("id", session["user_id"]).execute()

    session["nombre"] = nombre
    flash("Perfil actualizado correctamente.", "success")
    return redirect(url_for("perfil.ver"))
