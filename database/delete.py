from database import Session, model


def delete_discord_message(message_id: int):
    with Session() as session:
        model_message = session.query(model.Message).filter(
            model.Message.uid == message_id
        )
        model_message.delete()
        session.commit()
