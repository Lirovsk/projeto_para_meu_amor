import click
import os

from flask import Flask, current_app, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# Import models to ensure they are registered with SQLAlchemy
from .models import Message, SeenMessage, Music, SeenMusic, Photo


@click.command("init-db")
def init_db():
    with current_app.app_context():
        try:
            db.create_all(bind_key=None)  # Create tables for the default bind
            db.create_all(bind_key="photos")  # Create tables for the "photos" bind
            db.create_all(bind_key="seen")  # Create tables for the "seen" bind
            click.echo("Database initialized successfully.")
            
        except Exception as e:
            click.echo(f"Error initializing the database: {e}")


@click.command("add-message")
def add_data():
    try:
        while True:
            content = input("Enter the message content:\n")
            
            if len(content) > 255:
                print("Content exceeds 255 characters. Please try again.")
                continue
            
            new_message = Message(content=content)
            
            db.session.add(new_message)
            db.session.commit()
            print(f"Message added with ID: {new_message.id}")
    except Exception as e:
        print(f"Error adding message: {e}")
    
    except KeyboardInterrupt:
        print("\nData entry interrupted. Exiting.")
            
    return None


@click.command("add-music")
def add_music():
    try:
        while True:
            url = input("Enter the music URL:\n")
            
            if len(url) > 255:
                print("URL exceeds 255 characters. Please try again.")
                continue
            
            new_music = Music(url=url)
            
            db.session.add(new_music)
            db.session.commit()
            print(f"Music added with ID: {new_music.id}")
    except Exception as e:
        print(f"Error adding music: {e}")
    
    except KeyboardInterrupt:
        print("\nData entry interrupted. Exiting.")
            
    return None


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="super-secret-key",
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db",
        SQLALCHEMY_BINDS={
            "photos": "sqlite:///photos.db",
            "seen": "sqlite:///seen.db"
        })
    
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
        
    os.makedirs(app.instance_path, exist_ok=True)
    
    app.cli.add_command(init_db)
    app.cli.add_command(add_data)
    app.cli.add_command(add_music)
    
    db.init_app(app)
    from ..controllers import message, music, main, photo
    app.register_blueprint(message.app)
    app.register_blueprint(music.app)
    app.register_blueprint(main.app)
    app.register_blueprint(photo.app)
    
    
    return app
