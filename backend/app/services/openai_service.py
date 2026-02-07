from openai import AsyncOpenAI
from app.config import get_settings
import logging

settings = get_settings()
logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for interacting with OpenAI API"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens
    
    async def chat_completion(
        self,
        messages: list,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False
    ) -> dict:
        """
        Call ChatGPT API for text completion
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
        
        Returns:
            dict with 'content' and 'usage' keys
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=stream
            )
            
            if stream:
                return response
            
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "finish_reason": response.choices[0].finish_reason
            }
        
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for text (for future semantic search)
        
        Args:
            texts: List of texts to embed
        
        Returns:
            List of embedding vectors
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            
            return [item.embedding for item in response.data]
        
        except Exception as e:
            logger.error(f"OpenAI Embeddings error: {e}")
            raise


# Singleton instance
openai_service = OpenAIService()
