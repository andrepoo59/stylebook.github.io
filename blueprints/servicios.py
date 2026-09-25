
"""HU-05 Gestión de servicios (crear, editar, eliminar los propios)
HU-06 Consultar servicios (catálogo público)"""

"""
HU-05 Gestión de servicios (crear, editar, eliminar los propios)
HU-06 Consultar servicios (catálogo público)
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from supabase_client import sb
from utilidades import exigir_sesion, cliente_sesion

servicios_bp = Blueprint("servicios", __name__)


@servicios_bp.route("/servicios")
def catalogo():
    """HU-06: catálogo público de servicios, con filtro opcional por categoría."""
    categoria = request.args.get("categoria")
    consulta = sb.table("servicios").select(
        "*, profesionales(id, especialidad, perfiles(nombre))"
    ).eq("activo", True)

    if categoria:
        consulta = consulta.eq("categoria", categoria)

    respuesta = consulta.order("creado_en", desc=True).execute()
    return render_template("servicios/listar.html", servicios=respuesta.data, categoria=categoria)


@servicios_bp.route("/mis-servicios")
@exigir_sesion
def gestionar():
    """HU-05: el profesional ve y administra sus propios servicios."""
    sb_usuario = cliente_sesion()

    propio = sb_usuario.table("profesionales").select("id").eq(
        "perfil_id", session["user_id"]
    ).maybe_single().execute()

    if propio.data is None:
        flash("Primero debes registrarte como profesional.", "error")
        return redirect(url_for("profesionales.registro"))

    servicios = sb_usuario.table("servicios").select("*").eq(
        "profesional_id", propio.data["id"]
    ).order("creado_en", desc=True).execute()

    return render_template("servicios/gestionar.html", servicios=servicios.data)


@servicios_bp.route("/mis-servicios/nuevo", methods=["GET", "POST"])
@exigir_sesion
def nuevo():
    sb_usuario = cliente_sesion()

    propio = sb_usuario.table("profesionales").select("id").eq(
        "perfil_id", session["user_id"]
    ).maybe_single().execute()

    if propio.data is None:
        flash("Primero debes registrarte como profesional.", "error")
        return redirect(url_for("profesionales.registro"))

    if request.method == "GET":
        return render_template("servicios/form.html", servicio=None)

    datos = _leer_formulario(request)
    if datos is None:
        return render_template("servicios/form.html", servicio=None)

    datos["profesional_id"] = propio.data["id"]
    sb_usuario.table("servicios").insert(datos).execute()

    flash("Servicio agregado al catálogo.", "success")
    return redirect(url_for("servicios.gestionar"))


@servicios_bp.route("/mis-servicios/<servicio_id>/editar", methods=["GET", "POST"])
@exigir_sesion
def editar(servicio_id):
    sb_usuario = cliente_sesion()

    if request.method == "GET":
        servicio = sb_usuario.table("servicios").select("*").eq(
            "id", servicio_id
        ).single().execute()
        return render_template("servicios/form.html", servicio=servicio.data)

    datos = _leer_formulario(request)
    if datos is None:
        servicio = sb_usuario.table("servicios").select("*").eq(
            "id", servicio_id
        ).single().execute()
        return render_template("servicios/form.html", servicio=servicio.data)

    sb_usuario.table("servicios").update(datos).eq("id", servicio_id).execute()
    flash("Servicio actualizado.", "success")
    return redirect(url_for("servicios.gestionar"))


@servicios_bp.route("/mis-servicios/<servicio_id>/eliminar", methods=["POST"])
@exigir_sesion
def eliminar(servicio_id):
    sb_usuario = cliente_sesion()
    sb_usuario.table("servicios").delete().eq("id", servicio_id).execute()
    flash("Servicio eliminado.", "success")
    return redirect(url_for("servicios.gestionar"))


def _leer_formulario(request):
    nombre = request.form.get("nombre", "").strip()
    categoria = request.form.get("categoria", "general").strip() or "general"
    descripcion = request.form.get("descripcion", "").strip()
    precio = request.form.get("precio", "")
    duracion_min = request.form.get("duracion_min", "")

    if not nombre or not precio or not duracion_min:
        flash("Nombre, precio y duración son obligatorios.", "error")
        return None

    try:
        precio = float(precio)
        duracion_min = int(duracion_min)
    except ValueError:
        flash("Precio y duración deben ser numéricos.", "error")
        return None

    return {
        "nombre": nombre,
        "categoria": categoria,
        "descripcion": descripcion,
        "precio": precio,
        "duracion_min": duracion_min,
    }
