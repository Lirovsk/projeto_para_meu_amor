from ..app import db
from . import Music, SeenMusic


class MusicCRUD:
    @staticmethod
    def get_random_music():
        stmt = db.select(Music).order_by(db.func.random()).limit(1)
        result = db.session.execute(stmt).scalar_one_or_none()
        if not result:
            return {"error": "No music found in the database."}, 404
        
        url = result.url
        id = result.id
        
        # Move the music to the seen database
        seen_music = SeenMusic(url=url)
        try:
            db.session.add(seen_music)
            db.session.delete(result)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding seen music: {e}")
            return {"error": "Failed to add seen music."}, 500
        
        return {"url": url}, 200


    @staticmethod
    def get_seen_music():
        stmt = db.select(SeenMusic)
        result = db.session.execute(stmt).scalars().all()
        if not result:
            return {"error": "No seen music found."}, 404
        
        response = {"musics": []}
        
        for line in result:
            response["musics"].append({"id": line.id, "url":line.url})
        
        return response, 200
    
    
    @staticmethod
    def restore_music():
        max_id = db.session.scalar(db.select(db.func.max(SeenMusic.id)))
        actual_id = 1
        
        while actual_id <= max_id:
            seen_music = db.session.get(SeenMusic, actual_id)
            if seen_music:
                music = Music(url=seen_music.url)
                try:
                    db.session.add(music)
                    db.session.delete(seen_music)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error restoring music with ID {actual_id}: {e}")
            actual_id += 1
        return {"message": "All music restored successfully."}, 200
