"""
Horario laboral del profesional (prerrequisito de HU-03).
Módulo nuevo: no modifica auth.py, perfil.py ni profesionales.py.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from utilidades import exigir_sesion, cliente_sesion

horarios_bp = Blueprint("horarios", __name__)

DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]


@horarios_bp.route("/mis-horarios")
@exigir_sesion
def gestionar():
    sb_usuario = cliente_sesion()
    propio = sb_usuario.table("profesionales").select("id").eq(
        "perfil_id", session["user_id"]
    ).maybe_single().execute()

    if propio.data is None:
        flash("Primero debes registrarte como profesional.", "error")
        return redirect(url_for("profesionales.registro"))

    horarios = sb_usuario.table("horarios_profesional").select("*").eq(
        "profesional_id", propio.data["id"]
    ).order("dia_semana").execute()

    return render_template("horarios/gestionar.html", horarios=horarios.data, dias=DIAS)


@horarios_bp.route("/mis-horarios/nuevo", methods=["POST"])
@exigir_sesion
def nuevo():
    sb_usuario = cliente_sesion()
    propio = sb_usuario.table("profesionales").select("id").eq(
        "perfil_id", session["user_id"]
    ).maybe_single().execute()

    if propio.data is None:
        flash("Primero debes registrarte como profesional.", "error")
        return redirect(url_for("profesionales.registro"))

    dia_semana = request.form.get("dia_semana")
    hora_inicio = request.form.get("hora_inicio", "").strip()
    hora_fin = request.form.get("hora_fin", "").strip()

    if dia_semana is None or not hora_inicio or not hora_fin:
        flash("Completa día, hora de inicio y hora de fin.", "error")
        return redirect(url_for("horarios.gestionar"))

    if hora_fin <= hora_inicio:
        flash("La hora de fin debe ser posterior a la de inicio.", "error")
        return redirect(url_for("horarios.gestionar"))

    try:
        sb_usuario.table("horarios_profesional").insert({
            "profesional_id": propio.data["id"],
            "dia_semana": int(dia_semana),
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
        }).execute()
    except Exception as error:
        flash(f"No se pudo guardar la franja horaria: {error}", "error")
        return redirect(url_for("horarios.gestionar"))

    flash("Franja horaria agregada.", "success")
    return redirect(url_for("horarios.gestionar"))


@horarios_bp.route("/mis-horarios/<horario_id>/eliminar", methods=["POST"])
@exigir_sesion
def eliminar(horario_id):
    sb_usuario = cliente_sesion()
    sb_usuario.table("horarios_profesional").delete().eq("id", horario_id).execute()
    flash("Franja horaria eliminada.", "success")
    return redirect(url_for("horarios.gestionar"))