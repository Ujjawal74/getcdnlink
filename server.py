from flask import Flask, render_template, make_response, jsonify, request
import os
import threading
import queue
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import save_media
from flask_cors import CORS

app = Flask(__name__, static_url_path='')
CORS(app)
que = queue.Queue()

# global queue and thread
# Adding Cors Policy Also


def deletion():
    while True:
        files = que.get()
        if files:
            time.sleep(120)
        for file in files:
            loc = f"static/media/{file.split('/')[4]}"
            try:
                os.remove(path=loc)
            except Exception as e:
                print(f'No Such File Found! {e}')
        que.task_done()


threading.Thread(target=deletion, daemon=True).start()


def get_links(links):
    tray = []
    with ThreadPoolExecutor() as executor:
        results = [executor.submit(save_media, url) for url in links]
        for f in as_completed(results):
            try:
                tray.append(f.result())
            except:
                tray.append('No Media Found!')
    return tray

# routing


@app.route('/')
def index():
    return jsonify({'status': 'ok'})


@app.route('/api/getcdn', methods=['GET', 'POST'])
def thumbnail():
    if request.method == 'GET':
        return jsonify({'thumbnail': 'working...'})
    if request.method == 'POST':
        links = request.get_json()['links']
        thumbnails = get_links(links=links)
        que.put(thumbnails)
        return make_response(jsonify(thumbnails))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
