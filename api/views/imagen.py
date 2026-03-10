from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime
from api.decorators import token_required

import os
from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import uuid

################ GESTIÓN DE IMAGENES ################
class Save_Images(APIView):
    """
    Endpoint de la API para subir y gestionar imágenes de muestras médicas.
    
    Gestiona la subida de imágenes para placas Petri y muestras de sangre.
    Soporta formatos PNG, JPG y JPEG con validación de tamaño de archivo.
    Requiere autenticación por token.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    
    @token_required
    def post(self, request):
        """
        Subir imágenes de muestras médicas.
        
        Parámetros:<br/>
            tipo: Tipo de muestra ('petri' o 'muestras')<br/>
            file: Archivo de imagen a subir (PNG, JPG, JPEG)<br/>
        """
        # Validar tipo de muestra
        TIPOS_PERMITIDOS = {'petri', 'muestras'}

        tipo = request.data.get('tipo', '').lower()

        if tipo == '':
            return Response(
                {
                    'error': f'Se espera un campo con la key tipo y valor: {", ".join(TIPOS_PERMITIDOS)}'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if tipo not in TIPOS_PERMITIDOS:
            return Response({
                'error': f'El tipo enviado no es válido. Se esperaba un tipo con valor: {", ".join(TIPOS_PERMITIDOS)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Procesar y analizar archivos
        archivos_procesados = []
        errores = []

        for field_name, file_obj in request.FILES.items():         
            # Validar que sea PNG o JPG
            TIPOS_IMAGEN_PERMITIDOS = {'png', 'jpg', 'jpeg'} #TODO: Cambiar a MIME Types, para que sea más robusto
            content_type = (file_obj.content_type or '').lower()
            if not any(tipo in content_type for tipo in TIPOS_IMAGEN_PERMITIDOS):
                return Response({'error': f'{file_obj.name}: Solo se permiten archivos {", ".join(TIPOS_IMAGEN_PERMITIDOS).upper()}'}, status=status.HTTP_400_BAD_REQUEST)

            if file_obj.size > settings.DATA_UPLOAD_MAX_MEMORY_SIZE: 
                return Response({'error': f"La imagen '{file_obj.name}' es demasiado grande. Enviado: {file_obj.size/1048576}MB | Máximo: {settings.DATA_UPLOAD_MAX_MEMORY_SIZE/1048576}MB"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Resetear posición del archivo
                file_obj.seek(0)
                
                # Leer todo el archivo
                full_data = file_obj.read()
                file_obj.seek(0)  # Volver al inicio por si acaso
                
                # Guardar archivo en la carpeta correspondiente según el tipo
                saved_path = None
                try:
                    # Crear directorio según el tipo si no existe
                    target_dir = os.path.join(settings.MEDIA_ROOT, tipo)
                    os.makedirs(target_dir, exist_ok=True)
                    
                    # Respetar el nombre original del archivo
                    if file_obj.name:
                        filename = file_obj.name
                    else:
                        # Solo si no tiene nombre, generar uno
                        filename = f"archivo_sin_nombre_{uuid.uuid4().hex[:8]}"
                    
                    saved_path = os.path.join(target_dir, filename)
                    
                    # Si ya existe, agregar número secuencial
                    counter = 1
                    while os.path.exists(saved_path):
                        name, ext = os.path.splitext(filename)
                        saved_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                        counter += 1
                    
                    # Guardar el archivo
                    with open(saved_path, 'wb') as f:
                        f.write(full_data)
                    
                except Exception as save_error:
                    print(f"ERROR: API Views: No se pudo guardar el archivo: {save_error}")
                    saved_path = None
                
                # Agregar a la lista de procesados
                archivo_info = {
                    'campo': field_name,
                    'nombre_original': file_obj.name,
                    'nombre_guardado': os.path.basename(saved_path) if saved_path else None,
                    'carpeta': tipo,
                    'size_bytes': file_obj.size,
                    'size_kb': round(file_obj.size / 1024, 2),
                    'content_type': file_obj.content_type,
                    'procesado_en': datetime.now().isoformat()
                }
                archivos_procesados.append(archivo_info)
                
            except Exception as e:
                error_msg = f"Error procesando archivo '{field_name}': {str(e)}"
                errores.append(error_msg)
                print(f"ERROR: API Views: {error_msg}")
                import traceback
                traceback.print_exc()
        
        if archivos_procesados:
            return Response({
                "status": "success",
                "mensaje": "Archivos recibidos y procesados correctamente",
                "archivos_procesados": archivos_procesados,
                "total_archivos": len(archivos_procesados),
                "campos_texto": {k: v for k, v in request.data.items() if k not in request.FILES},
                "errores": errores if errores else None,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return Response({
                "status": "error",
                "mensaje": "No se encontraron archivos válidos para procesar",
                "debug_info": {
                    "files_keys": list(request.FILES.keys()),
                    "data_keys": list(request.data.keys()),
                    "content_type": request.content_type,
                    "errores": errores
                },
                "timestamp": datetime.now().isoformat()
            }, status=400)