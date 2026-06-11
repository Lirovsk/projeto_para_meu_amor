from . import MusicCRUD
from flask import Blueprint

app = Blueprint("music", __name__, url_prefix="/musics")


@app.route("/get", methods=["GET"])
def get_music():
    return MusicCRUD.get_random_music()


@app.route("/renew", methods=["POST"])
def renew_music():
    return MusicCRUD.restore_music()


@app.route("/get_seen", methods=["GET"])
def get_seen_musics():
    return MusicCRUD.get_seen_music()
