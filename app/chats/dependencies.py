import httpx
from groq import AsyncGroq
from spitch import AsyncSpitch

from app.environment import GEMINI_API_KEY, GEMINI_API_URL, GROQ_API_KEY, SPITCH_API_KEY
from app.preferences.models import Language


class SpitchClient:
    def __init__(self) -> None:
        self.client = AsyncSpitch(api_key=SPITCH_API_KEY)

    async def stt(self, audio_bytes: bytes):
        response = await self.client.speech.transcribe(
            language="en", content=audio_bytes
        )
        print("STT:", response.text)
        return response.text

    async def tts(self, text: str, language: Language):
        voices = {
            Language.EN: "john",
            Language.HA: "hasan",
            Language.IG: "obinna",
            Language.YO: "sade",
        }
        response = await self.client.speech.generate(
            language="en", text=text, voice=voices[language]
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
            max_completion_tokens=8192,
        )
        return chat_completion.choices[0].message.content


def get_groq_client():
    return GroqClient()


class GeminiClient:
    async def generate(self, system_prompt: str, user_query: str):
        print(system_prompt + user_query)
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY,
        }
        payload = {"contents": [{"parts": [{"text": system_prompt + user_query}]}]}

        async with httpx.AsyncClient() as client:
            response = await client.post(GEMINI_API_URL, headers=headers, json=payload)
            response.raise_for_status()

            try:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                print("Full response:", response.json())
                raise ValueError(f"Failed to extract response text: {e}")


def get_gemini_client():
    return GeminiClient()
