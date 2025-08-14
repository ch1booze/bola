from app.chats.models import Chat


def generate_system_prompt(interests, previous_chats):
    prompt = f"""Given the following interests of the user: {interests}
And also the last interactions had with the user: {[chat.model_dump() for chat in previous_chats]}
Generate a response to the query from the user.
"""

    return prompt
