from ..app import db
from . import Photo

from flask import request, flash, redirect, url_for, render_template, send_file
import io

class PhotoCRUD:
    @staticmethod
    def upload_foto():
        if request.method == "POST":
            print("dentro da função com post")
            if "photo_file" not in request.files:
                flash("Nenhum arquivo enviado.")
                return redirect(request.url)

            file = request.files["photo_file"]
            subtitle = request.form.get("subtitle")

            if file:
                # Instanciando o modelo exatamente como você definiu
                new_photo = Photo(data=file.read(), subtitle=subtitle if subtitle else None)
                db.session.add(new_photo)
                db.session.commit()
                print("salvando arquivo")
                flash("Foto salva com sucesso no banco de dados!")
                return redirect(url_for("photo.upload_foto"))

        # Busca todas as fotos usando a sintaxe do SQLAlchemy
        photos_list = db.session.execute(db.select(Photo)).scalars().all()
        return render_template("upload.html", photos=photos_list)

    @staticmethod
    def get_random_photo():
        # Busca uma foto aleatória usando a sintaxe do SQLAlchemy
        stmt = db.select(Photo).order_by(db.func.random()).limit(1)
        random_photo = db.session.execute(stmt).scalar_one_or_none()
        if random_photo:
            return send_file(io.BytesIO(random_photo.data), mimetype="image/jpeg")
        else:
            flash("Nenhuma foto encontrada.")
            return render_template("upload.html")
