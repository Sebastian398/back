import base64
import requests
import os

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
REPO_OWNER = 'Sebastian398'
REPO_NAME = 'Images'
BRANCH = 'main'

def upload_image_to_github(image_path, filename):
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

    response = requests.put(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        return f"https://{REPO_OWNER}.github.io/{REPO_NAME}/avatars/{filename}"
    else:
        raise Exception(f"GitHub upload failed: {response.status_code} {response.text}")
