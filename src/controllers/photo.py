from flask import Blueprint, request, flash, redirect, url_for, render_template, send_file
from ..app.models import Photo
from ..app import db
import io

from ..services import PhotoCRUD

app = Blueprint("photo", __name__, url_prefix="/photos")


@app.route("/", methods=["GET", "POST"])
def upload_foto():
    return PhotoCRUD.upload_foto()


@app.route("/get_random", methods=["GET"])
def get_random_photo():
    return PhotoCRUD.get_random_photo()
