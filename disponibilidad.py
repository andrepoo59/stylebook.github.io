"""
Cálculo de disponibilidad real (HU-03) y validación de cruces al reservar (HU-04).
Módulo nuevo e independiente: no modifica utilidades.py.
"""
from datetime import datetime, timedelta, date, time


def _a_time(valor):
    """Convierte 'HH:MM:SS' / 'HH:MM' (formato que devuelve Supabase) a datetime.time."""
    if isinstance(valor, time):
        return valor
    partes = valor.split(":")
    return time(int(partes[0]), int(partes[1]))


def generar_franjas_libres(fecha: date, horario_laboral: list, citas_del_dia: list,
                            duracion_min: int, paso_min: int = 15):
    """
    Devuelve las horas de inicio ('HH:MM') realmente libres ese día:
    dentro del horario laboral del profesional y sin chocar con citas ya confirmadas.
    """
    ocupados = [(_a_time(c["hora_inicio"]), _a_time(c["hora_fin"])) for c in citas_del_dia]
    libres = []
    duracion = timedelta(minutes=duracion_min)
    paso = timedelta(minutes=paso_min)

    for bloque in horario_laboral:
        inicio_bloque = datetime.combine(fecha, _a_time(bloque["hora_inicio"]))
        fin_bloque = datetime.combine(fecha, _a_time(bloque["hora_fin"]))

        cursor = inicio_bloque
        while cursor + duracion <= fin_bloque:
            fin_propuesto = cursor + duracion
            se_cruza = any(
                cursor.time() < fin_o and fin_propuesto.time() > inicio_o
                for inicio_o, fin_o in ocupados
            )
            if not se_cruza:
                libres.append(cursor.strftime("%H:%M"))
            cursor += paso

    return libres


def hay_cruce(hora_inicio_nueva: time, hora_fin_nueva: time, citas_del_dia: list) -> bool:
    """Verificación final del servidor antes de guardar, por si el horario mostrado
    quedó desactualizado entre que se cargó la página y se envió el formulario (HU-04)."""
    for c in citas_del_dia:
        inicio_o, fin_o = _a_time(c["hora_inicio"]), _a_time(c["hora_fin"])
        if hora_inicio_nueva < fin_o and hora_fin_nueva > inicio_o:
            return True
    return False