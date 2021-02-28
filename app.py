from flask import Flask, request, render_template
import spotipy
from sqlalchemy import create_engine
import json
from celery.task import task
from celery import current_app
from celery.bin import worker
from spotipy.oauth2 import SpotifyClientCredentials
from celery import Celery
spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

# Flask constructor
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(app)

"""
Fetch top songs by artist name using a celery task
"""


@celery.task(name='app.fetch_artist_details', bind=True)
def fetch_artist_details(self, artist):
    results = spotify.search(q='artist:' + artist, type='artist')
    items = results['artists']['items']

    if len(items) > 0:
        artist = items[0]
        return_data = {}
        result = spotify.artist_top_tracks(artist['id'])
        i = 0
        for track in result['tracks'][:10]:
            return_data.update({i: {"track_name": track['name'], "audio": track['preview_url'], "cover_art":
                track['album']['images'][0]['url']}})
            i = i + 1
        print(return_data)
        return return_data


# A decorator used to tell the application
# which URL is associated function
@app.route('/api/v1/get-top-songs/', methods=["GET", "POST"])
def gfg():
    if request.method == "POST":
        artist = request.form.get("artist")
        process_task = fetch_artist_details.apply_async(args=[artist])
        result = process_task.get()
        task_id = process_task.task_id
        task_state = process_task.state
        print(artist)
        # Return response
        response = app.response_class(
            response=json.dumps(result),
            status=200,
            mimetype='application/json'
        )
        print(result)
        return response

    return render_template("my-form.html")


@app.route('/', methods=['GET'])
def serve_default_page():
    artist = request.form.get("artist")
    print(artist)
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
