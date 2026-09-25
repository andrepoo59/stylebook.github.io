
"""HU-01 Registro de usuario (con selección de tipo de cuenta: cliente o profesional)
HU-02 Inicio de sesión"""
"""
HU-01 Registro de usuario (con selección de tipo de cuenta: cliente o profesional)
HU-02 Inicio de sesión
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from supabase_client import sb, sb_como_usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("auth/registro.html")

    nombre = request.form.get("nombre", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")
    telefono = request.form.get("telefono", "").strip()
    # Tipo de cuenta elegido en el registro (HU-01): cliente o profesional.
    # El rol "admin" no es auto-seleccionable por seguridad; se asigna manualmente.
    tipo_cuenta = request.form.get("tipo_cuenta", "cliente")
    if tipo_cuenta not in ("cliente", "profesional"):
        tipo_cuenta = "cliente"

    if not nombre or not email or not password:
        flash("Nombre, correo y contraseña son obligatorios.", "error")
        return render_template("auth/registro.html")

    if len(password) < 6:
        flash("La contraseña debe tener al menos 6 caracteres.", "error")
        return render_template("auth/registro.html")

    try:
        resultado = sb.auth.sign_up({
            "email": email,
            "password": password,
            "options": {"data": {"nombre": nombre}},
        })
    except Exception as error:
        flash(f"No se pudo completar el registro: {error}", "error")
        return render_template("auth/registro.html")

    if resultado.user is None:
        flash("No se pudo crear la cuenta. Intenta de nuevo.", "error")
        return render_template("auth/registro.html")

    # Si el proyecto de Supabase tiene confirmación de correo activada,
    # todavía no hay sesión activa: pedimos al usuario iniciar sesión.
    if resultado.session is None:
        flash("Cuenta creada. Revisa tu correo para confirmar antes de iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    # Con la sesión recién creada, completamos el perfil que dejó el trigger
    # (teléfono y, si eligió "profesional", el rol) respetando las RLS.
    cliente_autenticado = sb_como_usuario(resultado.session.access_token, resultado.session.refresh_token)
    datos_perfil = {}
    if telefono:
        datos_perfil["telefono"] = telefono
    if tipo_cuenta == "profesional":
        datos_perfil["rol"] = "profesional"
    if datos_perfil:
        try:
            cliente_autenticado.table("perfiles").update(datos_perfil).eq(
                "id", resultado.user.id
            ).execute()
        except Exception:
            pass  # el registro ya fue exitoso; se puede completar luego en el perfil

    _guardar_sesion(resultado)
    flash("Cuenta creada correctamente. ¡Bienvenido a StyleBook!", "success")

    if tipo_cuenta == "profesional":
        flash("Ahora completa tus datos para aparecer en el listado de profesionales.", "success")
        return redirect(url_for("profesionales.registro"))
    return redirect(url_for("perfil.ver"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    try:
        resultado = sb.auth.sign_in_with_password({"email": email, "password": password})
    except Exception:
        flash("Correo o contraseña incorrectos.", "error")
        return render_template("auth/login.html")

    _guardar_sesion(resultado)
    flash("Sesión iniciada correctamente.", "success")

    destino = request.args.get("volver")
    if destino:
        return redirect(destino)

    # Redirige según el cargo de la cuenta (cliente, profesional o administrador).
    if session.get("rol") == "admin":
        return redirect(url_for("admin.panel"))
    if session.get("rol") == "profesional":
        return redirect(url_for("servicios.gestionar"))
    return redirect(url_for("perfil.ver"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada.", "success")
    return redirect(url_for("index"))


def _guardar_sesion(resultado):
    """Guarda los tokens de Supabase y el cargo (rol) del usuario en la sesión de Flask (HU-02)."""
    session["access_token"] = resultado.session.access_token
    session["refresh_token"] = resultado.session.refresh_token
    session["user_id"] = resultado.user.id
    session["nombre"] = resultado.user.user_metadata.get("nombre", "Usuario")

    cliente = sb_como_usuario(session["access_token"], session["refresh_token"])
    try:
        perfil = cliente.table("perfiles").select("rol").eq("id", session["user_id"]).single().execute()
        session["rol"] = perfil.data["rol"]
    except Exception:
        session["rol"] = "cliente"
