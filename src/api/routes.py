"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Blueprint, jsonify, request
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import secrets
import time

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# -----------------------------
# Mock data (según tu requerimiento)
# -----------------------------

APERTURAS_DATA = [
    {
        "id": 350,
        "fecha_apertura": "2025-10-27T00:00:00.000Z",
        "id_recurso": "BA225",
        "id_empresa_recurso": "26",
        "clave": "BA225",
        "apertura_valida": "1",
        "cod_param_base": "BA-COLCURA",
        "id_empresa_apertura": "26",
        "cod_param_horario": "HOR7",
        "cod_param_operador": "OP-ARAUCO",
        "id_movil": "AL004",
        "id_empresa_movil": "02",
        "id_jefe_brigada": "243       ",
        "id_empr_jefe_brigada": "02",
        "id_conductor_piloto": "003       ",
        "id_empr_conductor_piloto": "26",
        "cant_personas_brigada": "0",
        "cant_personas_motosierristas": "0",
        "cant_personas_conductores": "1",
        "disponibilidad__motosierristas": "OASI",
        "disponibilidad__motobomba": "OASI",
        "disponibilidad__meteorologos": "OASI",
        "stock_combust_aereo_base_lts": "0",
        "cod_param_actividad": "ACT46",
        "id_empresa_predio": "02",
        "id_area_predio": "12",
        "id_predio": "20450",
        "nombre_predio": "LOTA                            ",
        "nombre_area": "Costas del Carbon               ",
        "fono_contacto": "945454545",
        "observacion": " ",
        "create_id_user": "00045",
        "mod_id_user": "00045",
        "coordenada_x": "-36.792",
        "coordenada_y": "-73.063",
        "huso": "3",
        "hemisferio": "E",
        "tipo_brigada": "U",
        "apertura_combustible": "0",
        "tipo_brigada_nombre": "BRIGADA TIPO II",
        "zona": "FORESTAL ARAUCO S. A.",
        "nombre_usuario": "Jorge Cariqueo",
        "nombre_area_real": "Costas del Carbon",
        "files": None,
        "personas": None
    },
    {
        "id": 349,
        "fecha_apertura": "2025-10-27T00:00:00.000Z",
        "id_recurso": "R0002",
        "id_empresa_recurso": "03",
        "clave": "BHA12",
        "apertura_valida": "1",
        "cod_param_base": "BA-PICHOY",
        "id_empresa_apertura": "03",
        "cod_param_horario": "HOR4",
        "cod_param_operador": "OP-PEGASUS",
        "id_movil": "H0124",
        "id_empresa_movil": "26",
        "id_jefe_brigada": "543       ",
        "id_empr_jefe_brigada": "02",
        "id_conductor_piloto": "430       ",
        "id_empr_conductor_piloto": "02",
        "cant_personas_brigada": "0",
        "cant_personas_motosierristas": "0",
        "cant_personas_conductores": "1",
        "disponibilidad__motosierristas": "OASI",
        "disponibilidad__motobomba": "OANA",
        "disponibilidad__meteorologos": "OASI",
        "stock_combust_aereo_base_lts": "8500",
        "cod_param_actividad": "ACT46",
        "id_empresa_predio": "03",
        "id_area_predio": "03",
        "id_predio": "99991",
        "nombre_predio": "PISTA LAS MARIAS                ",
        "nombre_area": "TEMUCO                          ",
        "fono_contacto": "958745321",
        "observacion": " ",
        "create_id_user": "00045",
        "mod_id_user": "00045",
        "coordenada_x": "-36.792",
        "coordenada_y": "-73.063",
        "huso": "3",
        "hemisferio": "E",
        "tipo_brigada": "1",
        "apertura_combustible": "1",
        "tipo_brigada_nombre": "HELITRANS",
        "zona": "ZONA VALDIVIA",
        "nombre_usuario": "Jorge Cariqueo",
        "nombre_area_real": "TEMUCO",
        "files": None,
        "personas": None
    }
]

RECURSOS_FOCO_DATA = [
    {
        "id_despacho": "001 ",
        "id_empresa": "02",
        "id_foco_incendio": "0223010222",
        "id_temporada": "23",
        "desc_tipo_foco": "FOCO",
        "nombre_recurso": "BA235                   ",
        "tipo_numero_personas": "BRIGADA TIPO II, 6 persona(s)",
        "estado_recurso": "🔥 Combatiendo en LOS ALAMOS Y SAN AMBROSIO"
    },
    {
        "id_despacho": "0011",
        "id_empresa": "02",
        "id_foco_incendio": "0223010222",
        "id_temporada": "23",
        "desc_tipo_foco": "FOCO",
        "nombre_recurso": "SKID SAN RAFAEL         ",
        "tipo_numero_personas": "SKIDDER, 2 persona(s)",
        "estado_recurso": "🛬 Aproximando a LOS ALAMOS Y SAN AMBROSIO"
    }
]

TEMPORADA_DATA = {
    "id_temporada": "49",
    "temporada_ini": "01-07-2025",
    "temporada_fin": "30-06-2026",
    "glosa": "2026"
}

POSICIONES_DATA = {
    "hasZ": False,
    "features": [
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{CF0C85F1-6877-4757-B1AF-7E5FCDD273EF}",
                "hgassetmodel": "BHA1",
                "objectid": 66,
                "posicionx": -72.68742,
                "posiciony": -37.797633
            },
            "geometry": {"x": -8091526.5781, "y": -4550877.457199998}
        },
        {
            "attributes": {
                "hgalias": "AEREA",
                "globalid": "{42E56C23-A59C-4037-A510-D42E61470144}",
                "hgassetmodel": "AA6",
                "objectid": 69,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8016749.383300001, "y": -4177433.8894999996}
        },
        {
            "attributes": {
                "hgalias": "BRGADA TIPO I",
                "globalid": "{3959499B-3EEF-4A2F-8882-A0A06C25FC4E}",
                "hgassetmodel": "BA224",
                "objectid": 72,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8061670.0261, "y": -4410233.719900001}
        },
        {
            "attributes": {
                "hgalias": "AEREO",
                "globalid": "{FA52D757-3C3B-4EA0-9907-291C6F041284}",
                "hgassetmodel": "AA10",
                "objectid": 75,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8122221.8179, "y": -4463663.201699998}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{2EC97FF5-8DCE-4F42-B23B-C2D034E322B7}",
                "hgassetmodel": "BA231",
                "objectid": 78,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8022313.5768, "y": -4462803.035500001}
        },
        {
            "attributes": {
                "hgalias": "AEREA",
                "globalid": "{97D14983-EE52-4D92-9526-E50A7F9746AF}",
                "hgassetmodel": "AA5",
                "objectid": 37,
                "posicionx": -72.021141,
                "posiciony": -34.990107
            },
            "geometry": {"x": -8017366.1775, "y": -4162552.645300001}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{83FC0ED5-2E3F-492C-8F8E-53C89C239AC6}",
                "hgassetmodel": "BHA17",
                "objectid": 35,
                "posicionx": -73.352104,
                "posiciony": -37.423385
            },
            "geometry": {"x": -7936577.255799999, "y": -4216724.0744}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO II",
                "globalid": "{A97B51AB-65F6-4B01-B6DF-BABFB6496306}",
                "hgassetmodel": "BA151",
                "objectid": 36,
                "posicionx": -73.352104,
                "posiciony": -37.423385
            },
            "geometry": {"x": -7936577.1065, "y": -4216724.0744}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO II",
                "globalid": "{F797BF1C-D5B7-4D14-A3AD-BE0ACC0EFE37}",
                "hgassetmodel": "BA181",
                "objectid": 67,
                "posicionx": -71.294066,
                "posiciony": -35.383078
            },
            "geometry": {"x": -7936419.1219999995, "y": -4216062.554299999}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{020D942F-6651-4F73-8878-F2E140C887FA}",
                "hgassetmodel": "BA664",
                "objectid": 70,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8086210.964500001, "y": -4373083.1653}
        },
        {
            "attributes": {
                "hgalias": "AEREA",
                "globalid": "{24058126-93CD-48FB-85AF-F0EEEE5065C4}",
                "hgassetmodel": "AA7",
                "objectid": 73,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8091592.7052, "y": -4550354.949099999}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{9C055E0D-8776-4BDD-A1DF-5DAF829CD25F}",
                "hgassetmodel": "BHA15",
                "objectid": 76,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8065676.8599, "y": -4656267.055399999}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{006E87AC-3984-4B9B-A777-FC068826BA88}",
                "hgassetmodel": "BA310",
                "objectid": 79,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8165329.066199999, "y": -4497945.764800001}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{CD6CC230-EA00-453B-8C74-6BD2D90B2185}",
                "hgassetmodel": "BHA18",
                "objectid": 52,
                "posicionx": -72.02069,
                "posiciony": -36.697196
            },
            "geometry": {"x": -8017306.047700001, "y": -4396984.16}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO II",
                "globalid": "{2FF5B76D-0D5F-4F0C-B972-BF18EDB168DA}",
                "hgassetmodel": "BA225",
                "objectid": 50,
                "posicionx": -72.96316,
                "posiciony": -37.17597
            },
            "geometry": {"x": -8143375.049000001, "y": -4453834.2333}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{84FFBA57-8BB7-4109-B00C-66A2305DFF77}",
                "hgassetmodel": "BHA9",
                "objectid": 57,
                "posicionx": -73.228463,
                "posiciony": -37.213995
            },
            "geometry": None
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{D41F5230-E4DF-407C-BEE1-F8B7326BA217}",
                "hgassetmodel": "BA664",
                "objectid": 59,
                "posicionx": -72.639669,
                "posiciony": -36.524856
            },
            "geometry": None
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{3C65196F-A783-42C5-BDBB-0D848D10D961}",
                "hgassetmodel": "BA224",
                "objectid": 61,
                "posicionx": -72.419214,
                "posiciony": -36.792575
            },
            "geometry": None
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{B8BBA773-2F20-4EC3-A8D7-451EE50B3060}",
                "hgassetmodel": "BA154",
                "objectid": 32,
                "posicionx": -72.551604,
                "posiciony": -36.298285
            },
            "geometry": {"x": -8076402.1425, "y": -4341758.9065999985}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{A79332CA-4377-45A7-BCA2-6EC38C7DCCFD}",
                "hgassetmodel": "BHA6",
                "objectid": 34,
                "posicionx": -72.232479,
                "posiciony": -35.485358
            },
            "geometry": {"x": -7936577.255799999, "y": -4216724.223700002}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{09DB8A1F-A612-49AB-9C8D-A5BC363898BD}",
                "hgassetmodel": "BHA9",
                "objectid": 68,
                "posicionx": -73.228463,
                "posiciony": -37.213995
            },
            "geometry": {"x": -8151755.2126, "y": -4468977.054200001}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{44180266-D61F-4ED0-A122-4C2DFDC92424}",
                "hgassetmodel": "BA186",
                "objectid": 71,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8165329.066199999, "y": -4497945.764800001}
        },
        {
            "attributes": {
                "hgalias": "BRIGADA TIPO I",
                "globalid": "{F97C45D5-CC8E-4C21-8A2C-BFA978B1B641}",
                "hgassetmodel": "BA180",
                "objectid": 74,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8084787.9673999995, "y": -4496380.2173999995}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{E3F79456-914C-49B3-B348-3D75C42C884D}",
                "hgassetmodel": "BHA11",
                "objectid": 77,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8023337.827400001, "y": -4393930.731899999}
        },
        {
            "attributes": {
                "hgalias": "HELITRANS",
                "globalid": "{255AFDF8-8BB1-4BD9-846A-7740A8B2555A}",
                "hgassetmodel": "BHA12",
                "objectid": 80,
                "posicionx": None,
                "posiciony": None
            },
            "geometry": {"x": -8105850.283, "y": -4470445.1415}
        }
    ],
    "exceededTransferLimit": False,
    "hasM": False,
    "globalIdFieldName": "globalid",
    "objectIdFieldName": "objectid",
    "fields": [
        {"defaultValue": None, "name": "objectid", "length": 4, "alias": "OBJECTID", "type": "esriFieldTypeOID"},
        {"defaultValue": None, "name": "globalid", "length": 38, "alias": "globalid", "type": "esriFieldTypeGlobalID"},
        {"defaultValue": None, "name": "hgassetmodel", "length": 255, "alias": "hgassetmodel", "type": "esriFieldTypeString"},
        {"defaultValue": None, "name": "hgalias", "length": 255, "alias": "hgalias", "type": "esriFieldTypeString"},
        {"defaultValue": None, "name": "posicionx", "alias": "posicionx", "type": "esriFieldTypeDouble"},
        {"defaultValue": None, "name": "posiciony", "alias": "posiciony", "type": "esriFieldTypeDouble"}
    ],
    "spatialReference": {"latestWkid": 3857, "wkid": 102100},
    "geometryType": "esriGeometryPoint"
}


# -----------------------------
# Endpoints
# -----------------------------

@api.route('/hello', methods=['GET', 'POST'])
def handle_hello():
    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }
    return jsonify(response_body), 200


@api.route('/aperturas', methods=['GET'])
def get_aperturas():
    """Apertura de recursos (GET sin parámetros)."""
    return jsonify(APERTURAS_DATA), 200


@api.route('/recursos-en-foco', methods=['GET'])
def get_recursos_en_foco():
    """Recursos en foco (GET sin parámetros)."""
    return jsonify(RECURSOS_FOCO_DATA), 200


@api.route('/temporada', methods=['GET'])
def get_temporada():
    """Temporada (GET sin parámetros)."""
    return jsonify(TEMPORADA_DATA), 200


@api.route('/posiciones', methods=['GET'])
def get_posiciones():
    """Posición de recursos (GET sin parámetros)."""
    return jsonify(POSICIONES_DATA), 200


@api.route('/token', methods=['POST'])
def post_token():
    """
    Genera un token estilo ArcGIS/servicios: 
    - token: string seguro URL-safe
    - expires: epoch en ms (por defecto +1h)
    - ssl: True
    Puedes opcionalmente validar credenciales en el body si lo necesitas.
    """
    # Opcional: validar body (username/password, client, etc.)
    # payload = request.get_json(silent=True) or {}
    # if not payload.get("username") or not payload.get("password"):
    #     return jsonify({"msg": "username/password requeridos"}), 400

    token = secrets.token_urlsafe(128)
    expires_ms = int((time.time() + 3600) * 1000)  # +1 hora
    return jsonify({"token": token, "expires": expires_ms, "ssl": True}), 200


# (Opcional) endpoint de salud
@api.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200
