from . import MessageCRUD

from flask import Blueprint, request

app = Blueprint("message", __name__, url_prefix="/messages")


@app.route("/get", methods=["GET"])
def get_message():
    return MessageCRUD.get_random_message()


@app.route("/renew", methods=["POST"])
def renew_message():
    return MessageCRUD.restore_message()


@app.route("/get_seen", methods=["GET"])
def get_seen_messages():
    return MessageCRUD.get_seen_message()
