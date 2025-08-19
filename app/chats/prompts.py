def generate_system_prompt(interests, previous_chats, language):
    q_and_a = [f"Query: {chat.query}\nAnswer: {chat.answer}" for chat in previous_chats]

    prompt = f"""Given the following interests of the user: {interests}
And also the last interactions had with the user: {q_and_a}
The language the person is conversing is expected to be: {language}. Please reply in the language preferred.
Generate a response to the query from the user.

User Query:
"""

    return prompt
