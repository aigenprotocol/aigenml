import os

import requests


def save_image_to_NFTSTORAGE(request, file_type):
    file = request.files[file_type]
    url = 'https://api.nft.storage/upload'
    NFTSTORAGE_API_KEY = os.environ.get('NFT_STORAGE_KEY')
    headers = {
        'Authorization': f'Bearer {NFTSTORAGE_API_KEY}',
    }
    files = {
        'file': (file.filename, file.stream, file.content_type)
    }
    response = requests.post(url, headers=headers, files=files)

    if response.status_code == 200:
        json_data = response.json()
        cid = json_data['value']['cid']
        link = f"https://ipfs.io/ipfs/{cid}/{file.filename}"
        return link
    else:
        return 'Upload failed'


def delete_file_from_NFT_STORAGE(cid):
    NFTSTORAGE_API_KEY = os.environ.get('NFT_STORAGE_KEY')

    if not cid:
        return 'CID is missing.', 400

    headers = {
        'Authorization': f'Bearer {NFTSTORAGE_API_KEY}',
    }

    delete_url = f'https://api.nft.storage/{cid}'
    response = requests.delete(delete_url, headers=headers)

    if response.status_code == 200:
        return 'File deleted successfully.'
    else:
        return f'Error deleting file: {response.text}', response.status_code
