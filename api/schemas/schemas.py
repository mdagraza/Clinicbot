#Esquema de validación para pacientes
paciente_schema = {
    "type": "object",
    "properties": {
        "nombre": {"type": "string"},
        "apellidos": {"type": "string"},
        "ident_muestra": {"type": "string"},
        "ident_petri": {"type": "string"},
        "edad": {"type": "integer"},
        "email": {"type": "string", "format": "email"},
        "genero": {"type": "string", "enum": ["Hombre", "Mujer", "Otro"]},
        "gr_sanguineo": {"type": "string", "enum": ["0-", "0+", "A+", "A-", "B+", "B-", "AB+", "AB-"]}
    },
    "required": ["nombre", "apellidos", "edad", "email", "genero", "gr_sanguineo"],
    "additionalProperties": False,
    "anyOf": [
        {"required": ["ident_muestra"]},
        {"required": ["ident_petri"]}
    ]
}

#Esquema de validación para muestras
muestras_schema = {
    "type": "object",
    "properties": {
        "identificacion": {"type": "string"},
        "caracteristicas_camara": {"type": "string"},
        "datos_muestra": {
            "type": "object",
            "properties": {
                "tipo_muestra": {"type": "string"},
                "fecha": {"type": "string", "pattern": r"^\d{2}/\d{2}/\d{4}$"},
                "hora": {"type": "string", "pattern": r"^\d{2}:\d{2}$"},
                "metodo_dilucion": {"type": "string"},
                "tipo_diluyente": {"type": "string"},
                "volumen_muestra_sembrado": {"type": "number"},
                "dilucion": {"type": "integer"}
            },
            "required": ["tipo_muestra", "fecha", "hora", "metodo_dilucion", "tipo_diluyente", "volumen_muestra_sembrado", "dilucion"],
            "additionalProperties": False
        },
        "datos_imagen": {
            "type": "object",
            "properties": {
                "id_imagen": {"type": "string"},
                "extension": {"type": "string", "enum": ["png", "jpg", "jpeg"]},
                "rgb": {
                    "type": "object",
                    "properties": {
                        "r": {"type": "integer", "minimum": 0, "maximum": 255},
                        "g": {"type": "integer", "minimum": 0, "maximum": 255},
                        "b": {"type": "integer", "minimum": 0, "maximum": 255}
                    },
                    "required": ["r", "g", "b"],
                    "additionalProperties": False
                },
                "hsv": {
                    "type": "object",
                    "properties": {
                        "h": {"type": "integer", "minimum": 0, "maximum": 255},
                        "s": {"type": "integer", "minimum": 0, "maximum": 255},
                        "v": {"type": "integer", "minimum": 0, "maximum": 255}
                    },
                    "required": ["h", "s", "v"],
                    "additionalProperties": False
                },
                "resolucion_imagen": {"type": "number"},
                "umbral_color": {"type": "integer"}
            },
            "required": ["id_imagen", "extension", "rgb", "hsv", "resolucion_imagen", "umbral_color"],
            "additionalProperties": False
        },
        "datos_analisis": {
            "type": "object",
            "properties": {
                "radio_min": {"type": "integer"},
                "radio_max": {"type": "integer"}
            },
            "required": ["radio_min", "radio_max", "parametros_procesamiento"],
            "additionalProperties": False
        },
        "resultados": {
            "type": "object",
            "properties": {
                "superficie_contada_1_cuadrado": {"type": "number"},
                "superficie_contada_5_cuadrados": {"type": "number"},
                "profundidad_camara_recuento": {"type": "number"},
                "factor_dilucion": {"type": "string"},
                "eritrocitos_cuadrado_1": {"type": "integer"},
                "eritrocitos_cuadrado_2": {"type": "integer"},
                "eritrocitos_cuadrado_3": {"type": "integer"},
                "eritrocitos_cuadrado_4": {"type": "integer"},
                "eritrocitos_cuadrado_5": {"type": "integer"},
                "eritrocitos_por_muestra": {"type": "number"},
                "valores_referencia_mujeres": {"type": "string"},
                "valores_referencia_hombres": {"type": "string"}
            },
            "required": [
                "superficie_contada_1_cuadrado", "superficie_contada_5_cuadrados",
                "profundidad_camara_recuento", "factor_dilucion",
                "eritrocitos_cuadrado_1","eritrocitos_cuadrado_2","eritrocitos_cuadrado_3",
                "eritrocitos_cuadrado_4","eritrocitos_cuadrado_5","eritrocitos_por_muestra",
                "valores_referencia_mujeres","valores_referencia_hombres"
            ],
            "additionalProperties": False
        }
    },
    "required": ["identificacion","caracteristicas_camara","datos_muestra","datos_imagen","datos_analisis","resultados"],
    "additionalProperties": False
}

#Esquema de validación para petri
petri_schema = {
    "type": "object",
    "properties": {
        "identificacion": {"type": "string"},
        "placa": {"type": "integer"},
        "datos_muestra": {
            "type": "object",
            "properties": {
                "tipo": {"type": "string"},
                "fecha": {"type": "string", "pattern": r"^\d{2}/\d{2}/\d{4}$"},
                "hora": {"type": "string", "pattern": r"^\d{2}:\d{2}$"},
                "metodo_siembra": {"type": "string"},
                "tipo_medio": {"type": "string"},
                "volumen": {"type": "integer"},
                "dilucion": {"type": "number"},
                "tiempo_incubacion": {"type": "integer"},
                "temperatura": {"type": "integer"}
            },
            "required": ["tipo","fecha","hora","metodo_siembra","tipo_medio","volumen","dilucion","tiempo_incubacion","temperatura"],
            "additionalProperties": False
        },
        "datos_imagen": {
            "type": "object",
            "properties": {
                "id_imagen": {"type": "string"},
                "extension": {"type": "string", "enum": ["png", "jpg", "jpeg"]},
                "rgb": {
                    "type": "object",
                    "properties": {
                        "r": {"type": "integer", "minimum":0, "maximum":255},
                        "g": {"type": "integer", "minimum":0, "maximum":255},
                        "b": {"type": "integer", "minimum":0, "maximum":255}
                    },
                    "required": ["r","g","b"],
                    "additionalProperties": False
                },
                "hsv": {
                    "type": "object",
                    "properties": {
                        "h": {"type": "integer", "minimum":0, "maximum":179},
                        "s": {"type": "integer", "minimum":0, "maximum":255},
                        "v": {"type": "integer", "minimum":0, "maximum":255}
                    },
                    "required": ["h","s","v"],
                    "additionalProperties": False
                },
                "resolucion": {"type": "number"},
                "umbral_color": {"type": "integer"}
            },
            "required": ["id_imagen","extension","rgb","hsv","resolucion","umbral_color"],
            "additionalProperties": False
        },
        "datos_analisis": {
            "type": "object",
            "properties": {
                "radio_min": {"type": "number"},
                "radio_max": {"type": "number"}
            },
            "required": ["radio_min","radio_max"],
            "additionalProperties": False
        },
        "resultados": {
            "type": "object",
            "properties": {
                "colonias_placa": {"type": "integer"},
                "colonias_muestra": {"type": "integer"},
                "objetos_no_validos": {"type": "integer"}
            },
            "required": ["colonias_placa","colonias_muestra","objetos_no_validos"],
            "additionalProperties": False
        }
    },
    "required": ["identificacion","placa","datos_muestra","datos_imagen","datos_analisis","resultados"],
    "additionalProperties": False
}

#Esquema de validación para Tokens
token_schema = {
    "type": "object",
    "properties": {
        "user": {"type": "string"},
        "pass": {"type": "string"},
        "expires": {"type": "integer", "default": 720}  # opcional
    },
    "required": ["user","pass"],
    "additionalProperties": False
}