from openai import AsyncOpenAI
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIInterface:
    def __init__(self, model="gpt-4"):
        self.model = model
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def get_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7
    ) -> str:
        """Get completion from OpenAI API"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            raise