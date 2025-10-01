import base64
import requests
import os
from datetime import datetime

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = 'Sebastian398'
REPO_NAME = 'Images'
BRANCH = 'main'

def delete_old_avatar_from_github(old_avatar_url):
    """
    Eliminar imagen anterior de GitHub si existe
    """
    if not old_avatar_url or 'github.io' not in old_avatar_url:
        return  # No es una URL de GitHub, no hacer nada
    
    try:
        # Extraer el nombre del archivo de la URL
        # URL formato: https://Sebastian398.github.io/Images/avatars/filename.jpg
        filename = old_avatar_url.split('/avatars/')[-1]
        
        # URL de la API para eliminar
        api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/avatars/{filename}"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }
        
        # Obtener SHA del archivo a eliminar
        get_response = requests.get(api_url, headers=headers)
        if get_response.status_code == 200:
            file_data = get_response.json()
            sha = file_data["sha"]
            
            # Eliminar archivo
            delete_data = {
                "message": f"Delete old avatar {filename}",
                "branch": BRANCH,
                "sha": sha
            }
            
            delete_response = requests.delete(api_url, json=delete_data, headers=headers)
            if delete_response.status_code == 200:
                print(f"Avatar anterior eliminado exitosamente: {filename}")
            else:
                print(f"Error eliminando avatar anterior: {delete_response.status_code}")
        else:
            print(f"Avatar anterior no encontrado para eliminar: {filename}")
            
    except Exception as e:
        print(f"Error al eliminar avatar anterior: {e}")

def upload_image_to_github(image_path, user_id, existing_avatar_url=None):
    """
    Subir nueva imagen con nombre único basado en timestamp
    """
    # ELIMINAR IMAGEN ANTERIOR SI EXISTE
    if existing_avatar_url:
        delete_old_avatar_from_github(existing_avatar_url)
    
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    # GENERAR NOMBRE ÚNICO CON TIMESTAMP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"avatar_{user_id}_{timestamp}.jpg"
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/avatars/{filename}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    data = {
        "message": f"Upload new avatar {filename}",
        "branch": BRANCH,
        "content": encoded_string
    }

    # SUBIR NUEVO ARCHIVO (siempre será nuevo por el timestamp)
    response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        new_url = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/avatars/{filename}"
        print(f"Nueva avatar subida exitosamente: {new_url}")
        return new_url
    else:
        raise Exception(f"Error al subir avatar: {response.status_code} - {response.json()}")