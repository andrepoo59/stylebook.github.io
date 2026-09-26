"""HU-06 Cancelar o reprogramar cita"""
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from utilidades import exigir_sesion, cliente_sesion

citas_bp = Blueprint("citas", __name__)


@citas_bp.route("/mis-citas")
@exigir_sesion
def listar():
    """Historial de citas del cliente autenticado."""
    sb_usuario = cliente_sesion()
    citas = sb_usuario.table("citas").select(
        "*, profesionales(especialidad, perfiles(nombre)), servicios(nombre, duracion_min)"
    ).eq("cliente_id", session["user_id"]).order("fecha").order("hora_inicio").execute()
    return render_template("citas/listar.html", citas=citas.data)


@citas_bp.route("/mis-citas/<cita_id>/cancelar", methods=["POST"])
@exigir_sesion
def cancelar(cita_id):
    """El cliente cancela; el horario queda libre para otros clientes."""
    sb_usuario = cliente_sesion()
    sb_usuario.table("citas").update({"estado": "cancelada"}).eq(
        "id", cita_id
    ).eq("cliente_id", session["user_id"]).execute()
    flash("Cita cancelada. El horario quedó disponible nuevamente.", "success")
    return redirect(url_for("citas.listar"))


@citas_bp.route("/mis-citas/<cita_id>/reprogramar", methods=["GET", "POST"])
@exigir_sesion
def reprogramar(cita_id):
    """El cliente elige nueva fecha/hora; se valida contra otras citas del profesional (RD-02)."""
    sb_usuario = cliente_sesion()

    cita = sb_usuario.table("citas").select("*").eq(
        "id", cita_id
    ).eq("cliente_id", session["user_id"]).single().execute()

    if cita.data is None:
        flash("No se encontró la cita.", "error")
        return redirect(url_for("citas.listar"))

    if request.method == "GET":
        return render_template("citas/reprogramar.html", cita=cita.data)

    fecha = request.form.get("fecha", "").strip()
    hora_inicio = request.form.get("hora_inicio", "").strip()

    if not fecha or not hora_inicio:
        flash("Fecha y hora son obligatorias.", "error")
        return render_template("citas/reprogramar.html", cita=cita.data)

    try:
        inicio_dt = datetime.strptime(f"{fecha} {hora_inicio}", "%Y-%m-%d %H:%M")
    except ValueError:
        flash("Fecha u hora inválida.", "error")
        return render_template("citas/reprogramar.html", cita=cita.data)

    servicio = sb_usuario.table("servicios").select("duracion_min").eq(
        "id", cita.data["servicio_id"]
    ).single().execute()
    duracion = servicio.data["duracion_min"] if servicio.data else 30
    hora_fin = (inicio_dt + timedelta(minutes=duracion)).strftime("%H:%M")

    # RD-02: el profesional no puede tener dos citas que se superpongan
    otras = sb_usuario.table("citas").select("hora_inicio, hora_fin").eq(
        "profesional_id", cita.data["profesional_id"]
    ).eq("fecha", fecha).neq("id", cita_id).in_(
        "estado", ["pendiente", "confirmada"]
    ).execute()

    for otra in otras.data:
        if hora_inicio < otra["hora_fin"] and otra["hora_inicio"] < hora_fin:
            flash("Ese horario ya está ocupado para este profesional. Elige otro.", "error")
            return render_template("citas/reprogramar.html", cita=cita.data)

    sb_usuario.table("citas").update({
        "fecha": fecha,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
    }).eq("id", cita_id).execute()

    flash("Cita reprogramada correctamente.", "success")
    return redirect(url_for("citas.listar"))