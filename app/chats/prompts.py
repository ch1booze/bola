def generate_system_prompt(interests, previous_chats, language):
    prompt = f"""Given the following interests of the user: {interests}
And also the last interactions had with the user: {[chat.model_dump() for chat in previous_chats]}
The language the person is conversing is expected to be: {language}. Please reply in the language preferred.
Generate a response to the query from the user.
"""

    return prompt
