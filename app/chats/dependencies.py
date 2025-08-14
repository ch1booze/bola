from spitch import AsyncSpitch
from groq import AsyncGroq
from app.environment import SPITCH_API_KEY, GROQ_API_KEY


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

    async def _(): ...


def get_groq_client():
    return GroqClient
