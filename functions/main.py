from firebase_functions import firestore_fn, storage_fn
from google.cloud.firestore_v1 import ArrayUnion, SERVER_TIMESTAMP
from firebase_admin import initialize_app, firestore, storage as admin_storage
import statistics
import pdfplumber
import re
import json
import hmac
import hashlib
import tempfile
import os
from datetime import datetime

initialize_app()


@firestore_fn.on_document_written(document="books/{bookId}/reviews/{reviewId}")
def actualizar_rankings(event):
    db = firestore.client()

    book_id = event.params["bookId"]

    libro_ref = db.collection("books").document(book_id)
    reviews = libro_ref.collection("reviews").stream()

    ratings = []

    for review in reviews:
        datos = review.to_dict()

        if "rating" in datos:
            ratings.append(datos["rating"])

    if len(ratings) > 0:
        media = statistics.mean(ratings)
    else:
        media = 0

    libro_ref.update({
        "averageRating": round(media, 2),
        "reviewsCount": len(ratings)
    })

    documentos_libros = db.collection("books").stream()
    lista_libros = []

    for libro in documentos_libros:
        datos = libro.to_dict()

        lista_libros.append({
            "id": libro.id,
            "title": datos.get("title", ""),
            "authors": datos.get("authors", []),
            "coverPath": datos.get("coverPath", ""),
            "pdfPath": datos.get("pdfPath", ""),
            "averageRating": datos.get("averageRating", 0),
            "reviewsCount": datos.get("reviewsCount", 0)
        })

    for i in range(len(lista_libros)):
        for j in range(i + 1, len(lista_libros)):
            if lista_libros[j]["averageRating"] > lista_libros[i]["averageRating"]:
                lista_temporal = lista_libros[i]
                lista_libros[i] = lista_libros[j]
                lista_libros[j] = lista_temporal

    top1 = []

    if len(lista_libros) > 0:
        top1.append(lista_libros[0])

    top5 = []

    for i in range(len(lista_libros)):
        if i < 5:
            top5.append(lista_libros[i])

    db.collection("rankings_books").document("top1").set({
        "type": "top1",
        "books": top1
    })

    db.collection("rankings_books").document("top5").set({
        "type": "top5",
        "books": top5
    })

    print("Rankings actualizados correctamente")
# ---------------- VALIDACIÓN CERTIFICADOS ----------------

# Clave simulada para firmar certificados internos o datos procesados por la app
CLAVE_SIMULADA = b"clave-simulada-para-certificar"

# Instituciones reconocidas por el sistema y sus idiomas asociados
INSTITUCIONES_CERTIFICADAS = {
    "Cambridge": ["Ingles"],
    "TOEFL": ["Ingles"],
    "IELTS": ["Ingles"],
    "ESOL": ["Ingles"],


    "DELE": ["Espanol"],
    "SIELE": ["Espanol"],

    "DELF": ["Frances"],
    "DALF": ["Frances"],

    "Goethe": ["Aleman"],
    "TestDaF": ["Aleman"],

    "CAPLE": ["Portugues"],

    "CILS": ["Italiano"],
    "CELI": ["Italiano"],

    "CNSE": ["LenguaDeSignos"]
}

NIVELES_IDIOMA = {"A1", "A2", "B1", "B2", "C1", "C2"}

# Expresiones regulares para buscar campos dentro del PDF
PATRONES = {
    "emisor": r"(?:Institucion|Institución|Emisor)\s*:\s*(.+?)(?=\s*(?:Idioma|Nivel|Nombre|Titular|Fecha|Codigo|Código|CSV|ID|$))",
    "idioma": r"Idioma\s*:\s*(.+?)(?=\s*(?:Nivel|Nombre|Titular|Fecha|Codigo|Código|CSV|ID|$))",
    "nivel": r"Nivel\s*:\s*(A1|A2|B1|B2|C1|C2)",
    "nombre": r"(?:Nombre|Titular)\s*:\s*(.+?)(?=\s*(?:Fecha|Codigo|Código|CSV|ID|$))",
    "fecha": r"(?:Fecha|Fecha de emision|Fecha de emisión)\s*:\s*(\d{2}/\d{2}/\d{4})",
    "codigo": r"(?:Codigo|Código|CSV|ID)\s*:\s*([A-Z0-9\-]+)"
}
def normalizar_texto(valor):
    return valor.strip().replace("\n", " ")


def firmar_datos(datos):
    # Genera una firma HMAC-SHA256 de los datos.
    # Sirve para proteger la integridad de registros internos del sistema.

    contenido = json.dumps(datos, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hmac.new(CLAVE_SIMULADA, contenido, hashlib.sha256).hexdigest()


def extraer_texto_pdf(ruta_pdf):
    # Extrae texto de todas las páginas del PDF.

    texto = ""

    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            contenido = pagina.extract_text()

            if contenido:
                texto = texto + contenido + "\n"

    return texto.strip()


def buscar_patron(texto, patron):
    coincidencia = re.search(patron, texto, re.IGNORECASE)

    if coincidencia:
        return normalizar_texto(coincidencia.group(1))

    return None


def extraer_datos(texto):
    # Extrae del PDF los campos principales del certificado.

    datos = {
        "emisor": buscar_patron(texto, PATRONES["emisor"]),
        "idioma": buscar_patron(texto, PATRONES["idioma"]),
        "nivel": buscar_patron(texto, PATRONES["nivel"]),
        "nombre_titular": buscar_patron(texto, PATRONES["nombre"]),
        "fecha_emision": buscar_patron(texto, PATRONES["fecha"]),
        "codigo_verificacion": buscar_patron(texto, PATRONES["codigo"])
    }

    # Validación mínima de campos obligatorios
    if not datos["emisor"] or not datos["idioma"] or not datos["nivel"]:
        raise ValueError("No se pudieron extraer los datos obligatorios del PDF")

    return datos


def validar_fecha(fecha_str):
    if not fecha_str:
        return False, "No se encontró fecha de emisión"

    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")

        if fecha > datetime.now():
            return False, "La fecha de emisión es futura"

        return True, "Fecha válida"

    except ValueError:
        return False, "Formato de fecha inválido"


def validar_certificado(cert):
    evidencias = {
        "institucion_valida": False,
        "idioma_valido": False,
        "nivel_valido": False,
        "fecha_valida": False,
        "codigo_presente": False,
        "firma_interna_valida": False
    }

    # 1. Institución reconocida
    if cert["emisor"] not in INSTITUCIONES_CERTIFICADAS:
        return False, "Institución no reconocida por el sistema", evidencias

    evidencias["institucion_valida"] = True

    # 2. Idioma coherente con institución
    if cert["idioma"] not in INSTITUCIONES_CERTIFICADAS[cert["emisor"]]:
        return False, "El idioma no coincide con la institución emisora", evidencias

    evidencias["idioma_valido"] = True

    # 3. Nivel válido
    if cert["nivel"] not in NIVELES_IDIOMA:
        return False, "El nivel del idioma es inválido", evidencias

    evidencias["nivel_valido"] = True

    # 4. Fecha válida
    fecha_ok, _ = validar_fecha(cert.get("fecha_emision"))
    evidencias["fecha_valida"] = fecha_ok

    # 5. Código de verificación presente
    if cert.get("codigo_verificacion"):
        evidencias["codigo_presente"] = True

    # 6. Firma interna del sistema
    firma_recibida = cert.get("firma")

    if firma_recibida:
        datos_sin_firma = dict(cert)
        datos_sin_firma.pop("firma", None)

        firma_calculada = firmar_datos(datos_sin_firma)

        if hmac.compare_digest(firma_recibida, firma_calculada):
            evidencias["firma_interna_valida"] = True

    # Regla final de prevalidación
    if (
        evidencias["institucion_valida"]
        and evidencias["idioma_valido"]
        and evidencias["nivel_valido"]
        and evidencias["fecha_valida"]
        and evidencias["codigo_presente"]
    ):
        return True, "Certificado prevalidado correctamente", evidencias

    return False, "El certificado queda pendiente de revisión manual", evidencias


def pdf_a_certificado(ruta_pdf):
    # Convierte un PDF en una estructura de certificado y le añade una firma interna.

    texto = extraer_texto_pdf(ruta_pdf)
    datos = extraer_datos(texto)

    # Firma interna para proteger integridad en la BBDD o en procesos posteriores
    datos["firma"] = firmar_datos(datos)

    return datos


@storage_fn.on_object_finalized(region="us-east1")
def validar_certificado_subido(event):
    # Esta función se ejecuta automáticamente cuando se sube un archivo a Storage.

    db = firestore.client()

    ruta_archivo = event.data.name
    nombre_bucket = event.data.bucket

    if ruta_archivo is None:
        return

    # Solo queremos validar certificados, no portadas ni PDFs de libros
    if not ruta_archivo.startswith("users/"):
        return

    if "/certificates/" not in ruta_archivo:
        return

    if not ruta_archivo.endswith(".pdf"):
        return

    partes_ruta = ruta_archivo.split("/")
    uid = partes_ruta[1]

    try:
        # Descargamos temporalmente el PDF desde Firebase Storage
        bucket = admin_storage.bucket(nombre_bucket)
        archivo_storage = bucket.blob(ruta_archivo)

        archivo_temporal = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        archivo_temporal.close()

        archivo_storage.download_to_filename(archivo_temporal.name)

        # Usamos las mismas funciones del script original
        certificado = pdf_a_certificado(archivo_temporal.name)
        valido, mensaje, evidencias = validar_certificado(certificado)

        if valido:
            estado = "prevalidated"
        else:
            estado = "pending_review"

        modelo_validacion = {
            "emisor": certificado.get("emisor"),
            "idioma": certificado.get("idioma"),
            "nivel": certificado.get("nivel"),
            "nombre_titular": certificado.get("nombre_titular"),
            "fecha_emision": certificado.get("fecha_emision"),
            "codigo_verificacion": certificado.get("codigo_verificacion"),
            "firma": certificado.get("firma"),

            "institucion_valida": evidencias["institucion_valida"],
            "idioma_valido": evidencias["idioma_valido"],
            "nivel_valido": evidencias["nivel_valido"],
            "fecha_valida": evidencias["fecha_valida"],
            "codigo_presente": evidencias["codigo_presente"],
            "firma_interna_valida": evidencias["firma_interna_valida"],

            "mensaje": mensaje,
            "validationMethod": "automatic_prevalidation",
            "validationStatus": estado,
            "validatedAt": datetime.now().isoformat()
        }

        # Actualizamos el usuario en Firestore
        db.collection("users").document(uid).update({
            "roleVerificationStatus": estado,
            "certificateValidation": modelo_validacion
        })

        os.remove(archivo_temporal.name)

        print("Certificado procesado:", uid, mensaje)

    except Exception as error:
        db.collection("users").document(uid).update({
            "roleVerificationStatus": "pending_review",
            "certificateValidation": {
                "validationStatus": "pending_review",
                "error": str(error),
                "validatedAt": datetime.now().isoformat()
            }
        })

        print("Error validando certificado:", error)

# ---------------- PUBLICAR TRADUCCIÓN ----------------

@firestore_fn.on_document_updated(document="contribution_requests/{requestId}")
def publicar_traduccion(event):
    db = firestore.client()

    datos_antes = event.data.before.to_dict()
    datos_despues = event.data.after.to_dict()

    if datos_antes is None or datos_despues is None:
        return

    estado_antes = datos_antes.get("status")
    estado_despues = datos_despues.get("status")

    if estado_antes == estado_despues:
        return

    if estado_despues != "published":
        return

    book_id = datos_despues.get("bookId")
    target_language = datos_despues.get("targetLanguage")
    translation_path = datos_despues.get("translationPath")
    translation_url = datos_despues.get("translationUrl")

    if not book_id or not target_language or not translation_path:
        print("Faltan datos para publicar traducción")
        return

    libro_ref = db.collection("books").document(book_id)

    campo_pdf_path = "translations." + target_language + ".pdfPath"
    campo_translation_url = "translations." + target_language + ".translationUrl"
    campo_status = "translations." + target_language + ".status"

    libro_ref.update({
        "availableLanguages": ArrayUnion([target_language]),
        campo_pdf_path: translation_path,
        campo_translation_url: translation_url,
        campo_status: "published",
        "updatedAt": SERVER_TIMESTAMP
    })

    print("Traducción publicada correctamente:", book_id, target_language)

