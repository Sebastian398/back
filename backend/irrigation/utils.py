import base64
import requests
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = 'Sebastian398'
REPO_NAME = 'Images'
BRANCH = 'main'

def upload_image_to_github(image_path, filename, existing_avatar_url=None):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/avatars/{filename}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    data = {
        "message": f"Upload avatar {filename}",
        "branch": BRANCH,
        "content": encoded_string
    }

    # VERIFICAR SI EL ARCHIVO YA EXISTE Y OBTENER SU SHA
    try:
        # Hacer GET request para obtener información del archivo actual
        get_response = requests.get(url, headers=headers)
        if get_response.status_code == 200:
            # El archivo existe, obtener su SHA
            current_data = get_response.json()
            data["sha"] = current_data["sha"]  # Agregar SHA requerido para actualización
            print(f"Archivo existe, usando SHA: {data['sha']}")
        elif get_response.status_code == 404:
            # El archivo no existe, no necesita SHA
            print("Archivo nuevo, no necesita SHA")
        else:
            print(f"Error verificando archivo existente: {get_response.status_code}")
    except Exception as e:
        print(f"Error al verificar archivo existente: {e}")
        # Continúa sin SHA (para archivos nuevos)

    # SUBIR/ACTUALIZAR EL ARCHIVO
    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        return f"https://{REPO_OWNER}.github.io/{REPO_NAME}/avatars/{filename}"
    else:
        raise Exception(f"Error al subir avatar: {response.status_code} - {response.json()}")