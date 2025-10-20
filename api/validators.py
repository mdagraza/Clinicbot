"""
Validaciones para los campos de Muestras de Sangre
Basado en los parámetros definidos en Parametros-muestraSangre.csv
"""

import re
from datetime import datetime


class MuestraSangreValidator:
    """
    Clase para validar los campos de muestras de sangre.
    Fácil de editar y mantener las reglas de validación.
    """

    # Configuración de validaciones (fácil de modificar)
    VALIDATION_RULES = {
        'codigo_identificacion': {
            'pattern': r'^[A-Z0-9]{4}\.[0-9]{2}[0-9]{2}[0-9]{3}[0-9]{2}$',
            'description': 'Formato PPPP.ddmmtttTT (ej: ABCD.151012025)',
            'required': True,
            'example': 'Code-128 PPPP.ddmmtttTT'
        },
        'fecha': {
            'pattern': r'^[0-3][0-9]/[0-1][0-9]$',
            'description': 'Formato dd/mm',
            'required': True,
            'example': '25/12'
        },
        'hora': {
            'pattern': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
            'description': 'Formato hh:mm (24 horas)',
            'required': False,
            'example': '14:30'
        },
        'extension_imagen': {
            'allowed_values': ['png', 'jpeg', 'jpg'],
            'description': 'Formato de imagen permitido',
            'required': False
        },
        'color_rgb_r': {
            'min_value': 0,
            'max_value': 255,
            'description': 'Componente R del color RGB (0-255)',
            'required': False
        },
        'color_rgb_g': {
            'min_value': 0,
            'max_value': 255,
            'description': 'Componente G del color RGB (0-255)',
            'required': False
        },
        'color_rgb_b': {
            'min_value': 0,
            'max_value': 255,
            'description': 'Componente B del color RGB (0-255)',
            'required': False
        },
        'color_hsv_h': {
            'min_value': 0,
            'max_value': 360,
            'description': 'Componente H del color HSV (0-360)',
            'required': False
        },
        'color_hsv_s': {
            'min_value': 0,
            'max_value': 100,
            'description': 'Componente S del color HSV (0-100%)',
            'required': False
        },
        'color_hsv_v': {
            'min_value': 0,
            'max_value': 100,
            'description': 'Componente V del color HSV (0-100%)',
            'required': False
        },
        'resolucion_imagen': {
            'min_value': 0.1,
            'max_value': 100,
            'description': 'Resolución en megapíxeles',
            'required': False
        },
        'radio_minimo': {
            'min_value': 1,
            'max_value': 1000,
            'description': 'Radio mínimo en píxeles',
            'required': False
        },
        'radio_maximo': {
            'min_value': 1,
            'max_value': 1000,
            'description': 'Radio máximo en píxeles',
            'required': False
        },
        'superficie_1_cuadrado': {
            'fixed_value': 0.04,
            'description': 'Superficie contada (1 cuadrado) en mm²',
            'required': False
        },
        'superficie_5_cuadrados': {
            'fixed_value': 0.2,
            'description': 'Superficie contada (5 cuadrados) en mm²',
            'required': False
        },
        'profundidad_camara': {
            'fixed_value': 0.1,
            'description': 'Profundidad cámara recuento en mm',
            'required': False
        },
        'factor_dilucion': {
            'fixed_value': 200,
            'description': 'Factor de dilución (1/200)',
            'required': False
        },
        'valores_referencia_mujeres_min': {
            'fixed_value': 4.2,
            'description': 'Valor referencia mujeres mínimo (millones/mm³)',
            'required': False
        },
        'valores_referencia_mujeres_max': {
            'fixed_value': 5.4,
            'description': 'Valor referencia mujeres máximo (millones/mm³)',
            'required': False
        },
        'valores_referencia_hombres_min': {
            'fixed_value': 4.7,
            'description': 'Valor referencia hombres mínimo (millones/mm³)',
            'required': False
        },
        'valores_referencia_hombres_max': {
            'fixed_value': 6.1,
            'description': 'Valor referencia hombres máximo (millones/mm³)',
            'required': False
        },
        'eritrocitos_cuadrado': {
            'min_value': 0,
            'max_value': 1000,
            'description': 'Número de eritrocitos por cuadrado',
            'required': False
        }
    }

    @classmethod
    def validate_codigo_identificacion(cls, codigo):
        """
        Valida el código de identificación formato PPPP.ddmmtttTT
        """
        rule = cls.VALIDATION_RULES['codigo_identificacion']

        if not codigo:
            if rule['required']:
                return False, "El código de identificación es requerido"
            return True, ""

        if not re.match(rule['pattern'], codigo):
            return False, f"Formato inválido. {rule['description']}. Ejemplo: {rule['example']}"

        # Validación adicional: verificar fecha válida
        try:
            dia = int(codigo[5:7])
            mes = int(codigo[7:9])

            if dia < 1 or dia > 31:
                return False, "Día inválido en el código (01-31)"

            if mes < 1 or mes > 12:
                return False, "Mes inválido en el código (01-12)"

        except (ValueError, IndexError):
            return False, "Formato de fecha en código inválido"

        return True, ""

    @classmethod
    def validate_fecha(cls, fecha):
        """
        Valida la fecha en formato dd/mm
        """
        rule = cls.VALIDATION_RULES['fecha']

        if not fecha:
            if rule['required']:
                return False, "La fecha es requerida"
            return True, ""

        if not re.match(rule['pattern'], fecha):
            return False, f"Formato inválido. {rule['description']}"

        try:
            dia = int(fecha[:2])
            mes = int(fecha[3:5])

            if dia < 1 or dia > 31:
                return False, "Día inválido (01-31)"

            if mes < 1 or mes > 12:
                return False, "Mes inválido (01-12)"

        except (ValueError, IndexError):
            return False, "Formato de fecha inválido"

        return True, ""

    @classmethod
    def validate_hora(cls, hora):
        """
        Valida la hora en formato hh:mm
        """
        rule = cls.VALIDATION_RULES['hora']

        if not hora:
            return True, ""  # No requerido

        if not re.match(rule['pattern'], hora):
            return False, f"Formato inválido. {rule['description']}"

        return True, ""

    @classmethod
    def validate_extension_imagen(cls, extension):
        """
        Valida la extensión de la imagen
        """
        rule = cls.VALIDATION_RULES['extension_imagen']

        if not extension:
            return True, ""  # No requerido

        extension = extension.lower().replace('.', '')
        if extension not in rule['allowed_values']:
            return False, f"Extensión no permitida. Valores válidos: {', '.join(rule['allowed_values'])}"

        return True, ""

    @classmethod
    def validate_rgb_component(cls, value, component):
        """
        Valida componentes RGB
        """
        rule = cls.VALIDATION_RULES[f'color_rgb_{component}']

        if value is None:
            return True, ""  # No requerido

        try:
            value = float(value)
            if value < rule['min_value'] or value > rule['max_value']:
                return False, f"Valor {component} debe estar entre {rule['min_value']} y {rule['max_value']}"
        except (ValueError, TypeError):
            return False, f"Valor {component} debe ser numérico"

        return True, ""

    @classmethod
    def validate_hsv_component(cls, value, component):
        """
        Valida componentes HSV
        """
        rule = cls.VALIDATION_RULES[f'color_hsv_{component}']

        if value is None:
            return True, ""  # No requerido

        try:
            value = float(value)
            if value < rule['min_value'] or value > rule['max_value']:
                return False, f"Valor {component} debe estar entre {rule['min_value']} y {rule['max_value']}"
        except (ValueError, TypeError):
            return False, f"Valor {component} debe ser numérico"

        return True, ""

    @classmethod
    def validate_numeric_range(cls, value, field_name):
        """
        Valida rangos numéricos genéricos
        """
        if field_name not in cls.VALIDATION_RULES:
            return True, ""

        rule = cls.VALIDATION_RULES[field_name]

        if value is None:
            return True, ""  # No requerido

        try:
            value = float(value)
            if 'min_value' in rule and value < rule['min_value']:
                return False, f"{rule['description']} - valor mínimo: {rule['min_value']}"
            if 'max_value' in rule and value > rule['max_value']:
                return False, f"{rule['description']} - valor máximo: {rule['max_value']}"
        except (ValueError, TypeError):
            return False, f"{rule['description']} - debe ser numérico"

        return True, ""

    @classmethod
    def validate_fixed_value(cls, value, field_name):
        """
        Valida valores fijos predefinidos
        """
        if field_name not in cls.VALIDATION_RULES:
            return True, ""

        rule = cls.VALIDATION_RULES[field_name]

        if value is None:
            return True, ""  # No requerido

        try:
            value = float(value)
            if abs(value - rule['fixed_value']) > 0.001:  # Tolerancia para decimales
                return False, f"Valor debe ser {rule['fixed_value']} ({rule['description']})"
        except (ValueError, TypeError):
            return False, f"Valor debe ser numérico"

        return True, ""

    @classmethod
    def validate_eritrocitos_cuadrado(cls, value, cuadrado_num):
        """
        Valida el conteo de eritrocitos por cuadrado
        """
        rule = cls.VALIDATION_RULES['eritrocitos_cuadrado']

        if value is None:
            return True, ""  # No requerido

        try:
            value = int(value)
            if value < rule['min_value'] or value > rule['max_value']:
                return False, f"Eritrocitos cuadrado {cuadrado_num}: debe estar entre {rule['min_value']} y {rule['max_value']}"
        except (ValueError, TypeError):
            return False, f"Eritrocitos cuadrado {cuadrado_num}: debe ser un número entero"

        return True, ""

    @classmethod
    def validate_muestra_completa(cls, data):
        """
        Valida todos los campos de una muestra de sangre
        """
        errors = {}

        # Validaciones de campos principales
        if 'codigo_identificacion' in data:
            valid, msg = cls.validate_codigo_identificacion(data['codigo_identificacion'])
            if not valid:
                errors['codigo_identificacion'] = msg

        if 'fecha' in data:
            valid, msg = cls.validate_fecha(data['fecha'])
            if not valid:
                errors['fecha'] = msg

        if 'hora' in data:
            valid, msg = cls.validate_hora(data['hora'])
            if not valid:
                errors['hora'] = msg

        # Validaciones de imagen
        if 'extension_imagen' in data:
            valid, msg = cls.validate_extension_imagen(data['extension_imagen'])
            if not valid:
                errors['extension_imagen'] = msg

        # Validaciones RGB
        for component in ['r', 'g', 'b']:
            field_name = f'color_rgb_{component}'
            if field_name in data:
                valid, msg = cls.validate_rgb_component(data[field_name], component)
                if not valid:
                    errors[field_name] = msg

        # Validaciones HSV
        for component in ['h', 's', 'v']:
            field_name = f'color_hsv_{component}'
            if field_name in data:
                valid, msg = cls.validate_hsv_component(data[field_name], component)
                if not valid:
                    errors[field_name] = msg

        # Validaciones de rangos numéricos
        numeric_fields = ['resolucion_imagen', 'radio_minimo', 'radio_maximo']
        for field in numeric_fields:
            if field in data:
                valid, msg = cls.validate_numeric_range(data[field], field)
                if not valid:
                    errors[field] = msg

        # Validaciones de valores fijos
        fixed_value_fields = [
            'superficie_1_cuadrado', 'superficie_5_cuadrados',
            'profundidad_camara', 'factor_dilucion'
        ]
        for field in fixed_value_fields:
            if field in data:
                valid, msg = cls.validate_fixed_value(data[field], field)
                if not valid:
                    errors[field] = msg

        # Validaciones de valores de referencia
        reference_fields = [
            'valores_referencia_mujeres_min', 'valores_referencia_mujeres_max',
            'valores_referencia_hombres_min', 'valores_referencia_hombres_max'
        ]
        for field in reference_fields:
            if field in data:
                valid, msg = cls.validate_fixed_value(data[field], field)
                if not valid:
                    errors[field] = msg

        # Validaciones de eritrocitos por cuadrado
        for i in range(1, 6):  # Cuadrados 1-5
            field_name = f'eritrocitos_cuadrado_{i}'
            if field_name in data:
                valid, msg = cls.validate_eritrocitos_cuadrado(data[field_name], i)
                if not valid:
                    errors[field_name] = msg

        return errors