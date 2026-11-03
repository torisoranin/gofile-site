import os, re, time
from datetime import datetime, timezone
from urllib.parse import quote
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)
FOLDER = os.getenv('GOFILE_FOLDER_ID', '').strip()
TOKEN = os.getenv('GOFILE_API_TOKEN', '').strip()
TITLE = os.getenv('SITE_TITLE', '動画一覧')
DESC = os.getenv('SITE_DESCRIPTION', '公開ファイル一覧')
IMAGE = os.getenv('SITE_IMAGE_URL', '').strip()
# Optional external JSON file thumbnail map, keyed by file ID or filename.
import json
try:
    with open(os.path.join(os.path.dirname(__file__), 'thumbnails.json'), encoding='utf-8') as fp:
        THUMBS = json.load(fp)
except (FileNotFoundError, json.JSONDecodeError):
    THUMBS = {}

@app.get('/')
def home():
    return render_template('index.html', title=TITLE, description=DESC, image=IMAGE)

@app.get('/api/files')
def files():
    if not FOLDER or not TOKEN:
        return jsonify(error='GOFILE_FOLDER_ID / GOFILE_API_TOKEN が未設定です'), 503
    if not re.fullmatch(r'[A-Za-z0-9-]{4,64}', FOLDER):
        return jsonify(error='フォルダIDの形式が不正です'), 400
    try:
        r = requests.get('https://api.gofile.io/contents/' + quote(FOLDER, safe=''),
            headers={'Authorization': 'Bearer ' + TOKEN},
            params={'page': 1, 'pageSize': 1000}, timeout=18)
        r.raise_for_status()
        obj = r.json()
        if obj.get('status') != 'ok':
            app.logger.warning('Gofile API status: %s', obj.get('status'))
            return jsonify(error='Gofile APIで一覧を取得できません。Premium要件・権限・フォルダIDを確認してください。'), 502
        data = obj.get('data') or {}
        children = data.get('children', data.get('childs', {}))
        if isinstance(children, dict): children = list(children.values())
        if not isinstance(children, list): children = []
        out=[]
        for f in children:
            if not isinstance(f, dict): continue
            fid = str(f.get('id') or '')
            name = str(f.get('name') or '名前なし')
            folder = f.get('type') == 'folder'
            link = str(f.get('link') or '')
            # For public pages, go through Gofile's own view rather than leak signed direct URLs.
            url = f'https://gofile.io/d/{f.get("code") or fid}' if folder else f'https://gofile.io/d/{FOLDER}'
            if link.startswith('https://gofile.io/'): url = link
            out.append({'id': fid, 'name': name, 'size': None if folder else f.get('size'),
                        'date': f.get('createTime'), 'folder': folder,
                        'url': url, 'thumb': THUMBS.get(fid) or THUMBS.get(name) or ''})
        response = jsonify(files=out, folder=f'https://gofile.io/d/{FOLDER}', total=len(out))
        response.headers['Cache-Control'] = 'public, max-age=60, s-maxage=60'
        return response
    except (requests.RequestException, ValueError):
        app.logger.exception('Gofile request failed')
        return jsonify(error='Gofileへの接続でエラーが発生しました'), 502

if __name__ == '__main__':
    app.run(port=8765, debug=False)
