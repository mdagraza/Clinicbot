#Traducción de mensajes de error para la validación de JSON
def msg_traducido(error):
    path = ".".join(map(str, error.path)) or "raíz"

    match error.validator:
        case "type":
            return f"El campo '{path}' debe ser del tipo {error.validator_value}"
        case "enum":
            return f"El campo '{path}' debe ser uno de {error.validator_value}"
        case "pattern":
            return f"El campo '{path}' no cumple el formato esperado"
        case "minimum":
            return f"El campo '{path}' no puede ser menor que {error.validator_value}"
        case "maximum":
            return f"El campo '{path}' no puede ser mayor que {error.validator_value}"
        case "required":
            missing_field = error.message.split("'")[1]
            return f"Falta el campo obligatorio '{missing_field}' en '{path}'"
        case "anyOf":
            # Extraemos los campos requeridos dentro de each subschema
            required_fields = []
            for subschema in error.validator_value:
                if "required" in subschema:
                    required_fields.extend(subschema["required"])
            # Quitamos duplicados
            required_fields = list(set(required_fields))
            return (f"En '{path}', se requiere al menos uno de los siguientes campos: "
                    f"{', '.join(required_fields)}")
        case _:
            return f"{path}: {error.message}"
        
#Función de validación de JSON 
def validate_json(schema, data):
    from jsonschema import Draft7Validator

    validator = Draft7Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    valid = True

    #Campos opcionales
    warning_messages = []
    for prop in schema["properties"]:
        if prop not in data and prop not in schema.get("required", []):
            warning_messages.append(f"Falta el campo opcional '{prop}'")

    #Campos obligatorios
    error_messages = []        
    if errors:
        valid = False
        for error in errors:
            if error.validator in ["required", "type", "enum", "format", "pattern", "minimum", "maximum", "anyOf"]:
                error_messages.append({
                    "ruta": list(error.path),
                    "error": msg_traducido(error)
                })
        
    # Validar que no haya campos extra
    extra_keys = set(data.keys()) - set(schema["properties"].keys())
    if extra_keys:
        valid = False
        for key in extra_keys:
            error_messages.append({
                "ruta": [],
                "error": f"El campo '{key}' no está permitido en la raíz"
            })

    return valid, error_messages, warning_messages