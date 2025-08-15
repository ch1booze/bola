from groq import AsyncGroq
from spitch import AsyncSpitch

from app.environment import GROQ_API_KEY, SPITCH_API_KEY


class SpitchClient:
    def __init__(self) -> None:
        self.client = AsyncSpitch(api_key=SPITCH_API_KEY)

    async def stt(self, audio_bytes: bytes):
        response = await self.client.speech.transcribe(
            language="en", content=audio_bytes
        )
        return response.text

    async def tts(self, text: str):
        response = await self.client.speech.generate(
            language="en", text=text, voice="tesfaye"
        )
        audio_bytes = await response.read()
        return audio_bytes


def get_spitch_client():
    return SpitchClient()


class GroqClient:
    def __init__(self) -> None:
        self.client = AsyncGroq(api_key=GROQ_API_KEY)

    async def generate(self, system_prompt: str, user_query: str):
        chat_completion = await self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content


def get_groq_client():
    return GroqClient()
