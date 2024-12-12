from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .openai_utils import OpenAIInterface

class BaseAgent(ABC):
    def __init__(
        self, 
        name: str, 
        role: str, 
        system_prompt: str
    ):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.openai = OpenAIInterface()
        self.conversation_history = []

    def _build_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Build messages for OpenAI API"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            *self.conversation_history,
            {"role": "user", "content": user_input}
        ]
        return messages

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input data and return response"""
        try:
            formatted_input = self._format_input(input_data)
            messages = self._build_messages(formatted_input)
            
            response = await self.openai.get_completion(messages)
            if response:
                self.conversation_history.extend([
                    {"role": "user", "content": formatted_input},
                    {"role": "assistant", "content": response}
                ])
                return self._parse_response(response)
            return {"status": "error", "error": "No response received"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    @abstractmethod
    def _format_input(self, input_data: Dict[str, Any]) -> str:
        """Format input data for the agent"""
        pass

    @abstractmethod
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse the agent's response"""
        pass