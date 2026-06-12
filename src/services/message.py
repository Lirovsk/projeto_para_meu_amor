from ..app import db
from . import Message, SeenMessage


class MessageCRUD:
    
    @staticmethod
    def get_random_message() -> tuple[dict, int]:
        stmt = db.select(Message).order_by(db.func.random()).limit(1)
        result = db.session.execute(stmt).scalar_one_or_none()
        if not result:
            return {"error": "No messages found in the database."}, 404
        
        content = result.content
        id = result.id
        
        # Move the message to the seen database
        seen_message = SeenMessage(content=content)
        try:
            db.session.add(seen_message)
            db.session.delete(result)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error adding seen message: {e}")
            return {"error": "Failed to add seen message."}, 500
        
        return {"content": content}, 200


    @staticmethod
    def get_seen_message() -> tuple[list[dict], int]:
        stmt = db.select(SeenMessage).order_by(SeenMessage.id.desc())
        results = db.session.scalars(stmt).all()
        
        if not results:
            return {"error": "No seen messages found in the database."}, 404
        
        response = {"messages":[]}
        
        for line in results:
            response["messages"].append({"id":line.id, "content":line.content})
        
        
        return response, 200
    
    
    @staticmethod
    def restore_message() -> tuple[dict, int]:
        max_id = db.session.scalar(db.select(db.func.max(SeenMessage.id)))
        actual_id = 1
        
        while actual_id <= max_id:
            seen_message = db.session.get(SeenMessage, actual_id)
            if seen_message:
                message = Message(content=seen_message.content)
                try:
                    db.session.add(message)
                    db.session.delete(seen_message)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"Error restoring message with ID {actual_id}: {e}")
            actual_id += 1
        return {"message": "All messages restored successfully."}, 200
