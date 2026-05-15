import firebase_admin
from firebase_admin import credentials, firestore, storage
import os


os.environ.pop("SSLKEYLOGFILE", None)

cred = credentials.Certificate("global-biblion-firebase-adminsdk-fbsvc-962ef1c01f.json")

firebase_admin.initialize_app(cred, {
    "storageBucket": "global-biblion.firebasestorage.app"
})

db = firestore.client()
bucket = storage.bucket()

books = [
    {
        "id": "book_06",
        "title": "Anna Karenina",
        "authors": ["Lev Tolstói"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela Clásica"],
        "cover": "Anna_karenina.png",
        "pdf": "Anna_karenina.pdf",
        "description": "Un amor prohibido que desafía las normas sociales y se entrelaza con retratos de la vida familiar y pública de la Rusia del siglo XIX, explorando el deseo, la culpa y las consecuencias de elegir contra lo establecido.",
        "translations": {}
    },
    {
        "id": "book_07",
        "title": "Cuentos góticos completos",
        "authors": ["Arthur Conan Doyle"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Terror"],
        "cover": "Cuentos_góticos.png",
        "pdf": "Cuentos góticos completos .pdf",
        "description": "Los narradores de estos cuentos exponen su testimonio de misteriosas desapariciones, siniestras influencias hipnóticas, llamadas irresistibles al suicidio y a la muerte, animales grotescos, unicornios furiosos y momias que vuelven a la vida.",
        "translations": {}
    },
    {
        "id": "book_08",
        "title": "De la Tierra a la Luna",
        "authors": ["Julio Verne"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Ciencia ficción"],
        "cover": "De_la_tierra_a_la_luna.png",
        "pdf": "De la Tierra a la Luna autor Julio Verne.pdf",
        "description": "Enviar a la Luna un proyectil que, auxiliado por el monstruoso cañón Columbiad, hará la función de una auténtica nave espacial para hacer realidad en el siglo XIX un viejo sueño: atravesar el espacio y descubrir un mundo lunar hasta entonces en penumbras.",
        "translations": {}
    },
    {
        "id": "book_09",
        "title": "El huésped de Drácula",
        "authors": ["Bram Stoker"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Terror", "Misterio"],
        "cover": "El_huespued_de_dracula.png",
        "pdf": "El huésped de Drácula.pdf",
        "description": "Jonathan Harker, un abogado inglés, viaja al castillo de Drácula en los Cárpatos para ayudar al conde con la compra de una propiedad en Londres. La visita revela la naturaleza vampírica del conde y marca el inicio de una batalla contra él.",
        "translations": {}
    },
    {
        "id": "book_10",
        "title": "El maravilloso mago de Oz",
        "authors": ["Lyman Frank Baum"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela Clásica", "Fantasía"],
        "cover": "El_maravilloso_mago_de_oz.png",
        "pdf": "El maravilloso mago de Oz.pdf",
        "description": "Dorothy vive en medio de las grises praderas de Kansas con su tío, su tía y su pequeño perrito Totó. Todo cambia cuando un ciclón la lleva a un mundo fantástico lleno de aventuras.",
        "translations": {}
    },
    {
        "id": "book_11",
        "title": "El príncipe feliz",
        "authors": ["Oscar Wilde"],
        "language": "Spanish",
        "availableLanguages": ["Spanish", "English"],
        "categories": ["Ficción"],
        "cover": "El_principe_feliz.png",
        "pdf": "El_principe_feliz.pdf",
        "description": "En lo alto de una ciudad, sobre una elevada columna, se erige la estatua del Príncipe Feliz. Su figura está cubierta de hojas de oro, tiene dos zafiros por ojos y un gran rubí adorna el pomo de su espada.",
        "translations": {
            "English": {
                "pdf": "The Happy Prince.pdf",
                "pdfPath": "books/pdf/The Happy Prince.pdf",
                "translationUrl": "",
                "status": "published"
            }
        }
    },
    {
        "id": "book_12",
        "title": "Guerra y paz I",
        "authors": ["Lev Tolstói"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela Clásica"],
        "cover": "Guerra_y_paz_I.png",
        "pdf": "Guerra_y_paz1.pdf",
        "description": "Primera parte de la novela de Lev Tolstói, ambientada durante la invasión napoleónica a Rusia y centrada en varias familias aristocráticas.",
        "translations": {}
    },
    {
        "id": "book_13",
        "title": "Guerra y paz II",
        "authors": ["Lev Tolstói"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela Clásica"],
        "cover": "Guerra_y_paz_II.png",
        "pdf": "Guerra_y_paz2.pdf",
        "description": "Segunda parte de la obra de Lev Tolstói, donde continúan los conflictos personales, familiares e históricos de la sociedad rusa.",
        "translations": {}
    },
    {
        "id": "book_14",
        "title": "Las aventuras del capitán Hatteras",
        "authors": ["Julio Verne"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Aventura"],
        "cover": "Las_aventuras_del_capitna_hatteras.png",
        "pdf": "Las aventuras del capitán Hatteras.pdf",
        "description": "Novela de aventuras de Julio Verne centrada en una expedición hacia el Polo Norte, llena de peligros, exploración y misterio.",
        "translations": {}
    },
    {
        "id": "book_15",
        "title": "La esfinge de los hielos",
        "authors": ["Julio Verne"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Ciencia ficción", "Aventura"],
        "cover": "La_esfinge_de_los_hielos.png",
        "pdf": "La esfinge de los hielos.pdf",
        "description": "La esfinge de los hielos es una novela de Julio Verne que narra la búsqueda del desaparecido Pym en el Polo Sur, combinando aventura y misterio en un entorno helado.",
        "translations": {}
    },
    {
        "id": "book_16",
        "title": "La estrella del sur",
        "authors": ["Julio Verne"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Aventura"],
        "cover": "La_estrella_del_sur.png",
        "pdf": "La estrella del Sur autor Julio Verne.pdf",
        "description": "Novela de aventuras ambientada en Sudáfrica, donde un ingeniero descubre un enorme diamante artificial y se ve envuelto en intrigas, rivalidades y ambición.",
        "translations": {}
    },
    {
        "id": "book_17",
        "title": "La narración de Arthur Gordon Pym",
        "authors": ["Edgar Allan Poe"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Aventura", "Terror"],
        "cover": "La_narrativa_de_Arthur_Gordon_Pym.png",
        "pdf": "La_narración_de_Arthur_Gordon_Pym.pdf",
        "description": "Novela de aventuras y terror marítimo que sigue el viaje de un joven polizón hacia los mares del sur, donde vive naufragios, motines y sucesos inquietantes.",
        "translations": {}
    },
    {
        "id": "book_18",
        "title": "Las aventuras de Pinocho",
        "authors": ["Carlo Collodi"],
        "language": "Spanish",
        "availableLanguages": ["Spanish", "Italian"],
        "categories": ["Fantasía", "Infantil"],
        "cover": "Las_aventuras_de_Pinocho.png",
        "pdf": "Las_aventuras_de_Pinocho.pdf",
        "description": "Historia de un muñeco de madera que sueña con convertirse en un niño real mientras vive numerosas aventuras y aprende lecciones sobre la honestidad y la responsabilidad.",
        "translations": {
            "Italian": {
                "pdf": "Le avventure di Pinocchio_Italian.pdf",
                "pdfPath": "books/pdf/Le avventure di Pinocchio_Italian.pdf",
                "translationUrl": "",
                "status": "published"
            }
        }
    },
    {
        "id": "book_19",
        "title": "Las aventuras de Sherlock Holmes",
        "authors": ["Arthur Conan Doyle"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela policíaca", "Misterio"],
        "cover": "Las_aventuras_de_sherlok_holmes.png",
        "pdf": "Las_aventuras_de_Sherlock_Holmes.pdf",
        "description": "Colección de relatos protagonizados por Sherlock Holmes y su compañero Watson, quienes resuelven misteriosos casos mediante la observación y la lógica.",
        "translations": {}
    },
    {
        "id": "book_20",
        "title": "Los crímenes de la calle Morgue",
        "authors": ["Edgar Allan Poe"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Terror", "Misterio"],
        "cover": "Los_crimenes_de_la_calle_morgue.png",
        "pdf": "Los crímenes de la calle Morgue.pdf",
        "description": "El detective Auguste Dupin investiga un extraño y brutal asesinato en París utilizando la lógica y el análisis deductivo.",
        "translations": {}
    },
    {
        "id": "book_21",
        "title": "Cuentos de los hermanos Grimm",
        "authors": ["Jacob Grimm", "Wilhelm Grimm"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Infantil", "Fantasía"],
        "cover": "Los_cuentos_de_los_hermanos_grim.png",
        "pdf": "Cuentos completos de los hermanos Grimm.pdf",
        "description": "Colección de cuentos clásicos como Cenicienta, Blancanieves y Hansel y Gretel, llenos de fantasía y enseñanzas morales.",
        "translations": {}
    },
    {
        "id": "book_22",
        "title": "Los tres mosqueteros",
        "authors": ["Alexandre Dumas"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Aventura", "Novela Histórica"],
        "cover": "Los_tres_mosqueteros.png",
        "pdf": "Los_tres_mosqueteros.pdf",
        "description": "Novela de aventuras que sigue a D’Artagnan y a los mosqueteros Athos, Porthos y Aramis en duelos, intrigas políticas y misiones en la Francia del siglo XVII.",
        "translations": {}
    },
    {
        "id": "book_23",
        "title": "Moby-Dick",
        "authors": ["Herman Melville"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Aventura", "Filosofía", "Drama"],
        "cover": "moby_dick.png",
        "pdf": "Moby_Dick.pdf",
        "description": "Narra la obsesiva persecución del capitán Ahab contra una enorme ballena blanca llamada Moby Dick en un peligroso viaje por los océanos.",
        "translations": {}
    },
    {
        "id": "book_24",
        "title": "Nuestra Señora de París",
        "authors": ["Victor Hugo"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela", "Romántica"],
        "cover": "Nuestra_sra_de_paris.png",
        "pdf": "Nuestra_sra_de_paris.pdf",
        "description": "Ambientada en el París medieval, cuenta la historia de Quasimodo, Esmeralda y el archidiácono Claude Frollo entre amor, tragedia e injusticia.",
        "translations": {}
    },
    {
        "id": "book_25",
        "title": "París en el siglo XX",
        "authors": ["Julio Verne"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela", "Ciencia ficción"],
        "cover": "paris_en_el_siglo_XX.png",
        "pdf": "París en el siglo XX.pdf",
        "description": "Una sociedad futurista dominada por la tecnología y el dinero, donde un joven amante de las artes lucha por encontrar su lugar.",
        "translations": {}
    },
    {
        "id": "book_26",
        "title": "Struwwelpeter",
        "authors": ["Heinrich Hoffmann"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Infantil", "Cuento moral"],
        "cover": "Struwelpeter.png",
        "pdf": "Struwwelpeter-Pedro-Melenas.pdf",
        "description": "Libro compuesto por cuentos breves e ilustrados que muestran, de forma exagerada y moralizante, las consecuencias del mal comportamiento infantil.",
        "translations": {}
    },
    {
        "id": "book_27",
        "title": "Ivanhoe",
        "authors": ["Walter Scott"],
        "language": "Spanish",
        "availableLanguages": ["Spanish"],
        "categories": ["Novela", "Histórica"],
        "cover": "Ivanhoe.png",
        "pdf": "Ivanhoe.pdf",
        "description": "Novela ambientada en la Inglaterra medieval, donde el caballero Ivanhoe vive torneos, conflictos y aventuras entre normandos y sajones.",
        "translations": {}
    }
]

for book in books:
    ruta_portada_local = "covers/" + book["cover"]
    ruta_pdf_local = "pdfs/" + book["pdf"]

    if not os.path.exists(ruta_portada_local):
        print("No existe la portada:", ruta_portada_local)
        continue

    if not os.path.exists(ruta_pdf_local):
        print("No existe el PDF:", ruta_pdf_local)
        continue

    ruta_portada_storage = "books/covers/" + book["cover"]
    ruta_pdf_storage = "books/pdf/" + book["pdf"]

    print("Subiendo libro:", book["title"])

    portada_blob = bucket.blob(ruta_portada_storage)
    portada_blob.upload_from_filename(ruta_portada_local)
    portada_blob.content_type = "image/png"
    portada_blob.patch()

    pdf_blob = bucket.blob(ruta_pdf_storage)
    pdf_blob.upload_from_filename(ruta_pdf_local)
    pdf_blob.content_type = "application/pdf"
    pdf_blob.patch()

    translations = {}

    for idioma, datos_traduccion in book["translations"].items():
        ruta_pdf_traduccion_local = "pdfs/" + datos_traduccion["pdf"]
        ruta_pdf_traduccion_storage = datos_traduccion["pdfPath"]

        if os.path.exists(ruta_pdf_traduccion_local):
            traduccion_blob = bucket.blob(ruta_pdf_traduccion_storage)
            traduccion_blob.upload_from_filename(ruta_pdf_traduccion_local)
            traduccion_blob.content_type = "application/pdf"
            traduccion_blob.patch()

            translations[idioma] = {
                "pdfPath": ruta_pdf_traduccion_storage,
                "translationUrl": datos_traduccion["translationUrl"],
                "status": datos_traduccion["status"]
            }

            print("Traducción subida:", idioma, "-", book["title"])
        else:
            print("No existe el PDF traducido:", ruta_pdf_traduccion_local)

    db.collection("books").document(book["id"]).set({
        "title": book["title"],
        "authors": book["authors"],
        "language": book["language"],
        "availableLanguages": book["availableLanguages"],
        "categories": book["categories"],
        "description": book["description"],

        "coverPath": ruta_portada_storage,
        "pdfPath": ruta_pdf_storage,
        "audioPath": None,

        "averageRating": 0,
        "reviewsCount": 0,

        "translations": translations,

        "createdAt": firestore.SERVER_TIMESTAMP,
        "updatedAt": firestore.SERVER_TIMESTAMP
    })

    print("Libro subido correctamente:", book["title"])

print("Carga completada.")