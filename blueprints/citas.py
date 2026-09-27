"""
HU-03: disponibilidad real de horarios de un profesional.
HU-04: reserva de cita eligiendo servicio, profesional y horario.
Módulo nuevo: no modifica profesionales.py ni servicios.py.
"""
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from supabase_client import sb
from utilidades import exigir_sesion, cliente_sesion
from disponibilidad import generar_franjas_libres, hay_cruce, _a_time

citas_bp = Blueprint("citas", __name__)


def _disponibilidad(profesional_id, fecha_str, duracion_min):
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    dia_semana = fecha.weekday()  # 0=Lunes ... 6=Domingo, igual que en la BD

    horario_laboral = sb.table("horarios_profesional").select(
        "hora_inicio, hora_fin"
    ).eq("profesional_id", profesional_id).eq("dia_semana", dia_semana).execute()

    citas_del_dia = sb.table("citas").select(
        "hora_inicio, hora_fin"
    ).eq("profesional_id", profesional_id).eq("fecha", fecha_str).eq(
        "estado", "confirmada"
    ).execute()

    libres = generar_franjas_libres(fecha, horario_laboral.data, citas_del_dia.data, duracion_min)
    return fecha, citas_del_dia.data, libres


@citas_bp.route("/profesionales/<profesional_id>/reservar", methods=["GET", "POST"])
@exigir_sesion
def reservar(profesional_id):
    sb_usuario = cliente_sesion()

    profesional = sb.table("profesionales").select(
        "*, perfiles(nombre)"
    ).eq("id", profesional_id).single().execute()

    servicios = sb.table("servicios").select("*").eq(
        "profesional_id", profesional_id
    ).eq("activo", True).execute()

    if request.method == "GET":
        return render_template(
            "citas/reservar.html", profesional=profesional.data,
            servicios=servicios.data, fecha=None, horarios_libres=[], servicio_id=None,
        )

    servicio_id = request.form.get("servicio_id", "")
    fecha_str = request.form.get("fecha", "")
    hora_inicio_str = request.form.get("hora_inicio", "")

    servicio = next((s for s in servicios.data if s["id"] == servicio_id), None)
    if not servicio or not fecha_str or not hora_inicio_str:
        flash("Selecciona un servicio, una fecha y un horario válidos.", "error")
        return render_template(
            "citas/reservar.html", profesional=profesional.data, servicios=servicios.data,
            fecha=fecha_str, horarios_libres=[], servicio_id=servicio_id,
        )

    fecha, citas_del_dia, libres = _disponibilidad(profesional_id, fecha_str, servicio["duracion_min"])

    # HU-03: solo se acepta un horario que realmente esté libre.
    if hora_inicio_str not in libres:
        flash("Ese horario ya no está disponible. Elige otro.", "error")
        return render_template(
            "citas/reservar.html", profesional=profesional.data, servicios=servicios.data,
            fecha=fecha_str, horarios_libres=libres, servicio_id=servicio_id,
        )

    hora_inicio = _a_time(hora_inicio_str)
    minutos_fin = hora_inicio.hour * 60 + hora_inicio.minute + servicio["duracion_min"]
    hora_fin = f"{minutos_fin // 60:02d}:{minutos_fin % 60:02d}"

    # HU-04: verificación final por si alguien reservó justo antes.
    if hay_cruce(hora_inicio, _a_time(hora_fin), citas_del_dia):
        flash("Alguien acaba de reservar ese horario. Elige otro.", "error")
        return render_template(
            "citas/reservar.html", profesional=profesional.data, servicios=servicios.data,
            fecha=fecha_str, horarios_libres=[], servicio_id=servicio_id,
        )

    try:
        sb_usuario.table("citas").insert({
            "cliente_id": session["user_id"],
            "profesional_id": profesional_id,
            "servicio_id": servicio_id,
            "fecha": fecha_str,
            "hora_inicio": hora_inicio_str,
            "hora_fin": hora_fin,
        }).execute()
    except Exception as error:
        flash(f"No se pudo reservar la cita: {error}", "error")
        return render_template(
            "citas/reservar.html", profesional=profesional.data, servicios=servicios.data,
            fecha=fecha_str, horarios_libres=[], servicio_id=servicio_id,
        )

    flash("¡Cita reservada con éxito!", "success")
    return redirect(url_for("citas.mis_citas"))


@citas_bp.route("/profesionales/<profesional_id>/horarios-disponibles")
def horarios_disponibles(profesional_id):
    """Endpoint AJAX: refresca los horarios libres al cambiar fecha o servicio, sin recargar la página."""
    fecha_str = request.args.get("fecha", "")
    servicio_id = request.args.get("servicio_id", "")

    servicio = sb.table("servicios").select("duracion_min").eq("id", servicio_id).maybe_single().execute()
    if not fecha_str or not servicio.data:
        return jsonify({"horarios": []})

    _, _, libres = _disponibilidad(profesional_id, fecha_str, servicio.data["duracion_min"])
    return jsonify({"horarios": libres})


@citas_bp.route("/mis-citas")
@exigir_sesion
def mis_citas():
    sb_usuario = cliente_sesion()
    citas = sb_usuario.table("citas").select(
        "*, profesionales(especialidad, perfiles(nombre)), servicios(nombre, precio)"
    ).eq("cliente_id", session["user_id"]).order("fecha", desc=True).execute()
    return render_template("citas/mis_citas.html", citas=citas.data)


@citas_bp.route("/citas/<cita_id>/cancelar", methods=["POST"])
@exigir_sesion
def cancelar(cita_id):
    sb_usuario = cliente_sesion()
    sb_usuario.table("citas").update({"estado": "cancelada"}).eq("id", cita_id).execute()
    flash("Cita cancelada.", "success")
    return redirect(url_for("citas.mis_citas"))