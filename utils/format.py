def format_user(user_object) -> dict:
    object = {
        "user_id": user_object.user_id,
        "user_name": user_object.user_name,
        "user_email": user_object.user_email
    }

    return object