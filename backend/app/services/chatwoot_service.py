import httpx
from app.config import get_settings
import logging
import asyncio
from pathlib import Path
from typing import Optional

settings = get_settings()
logger = logging.getLogger(__name__)


class ChatwootService:
    """Service for interacting with Chatwoot API"""
    
    def __init__(self):
        self.base_url = settings.chatwoot_url
        self.api_key = settings.chatwoot_access_token
        self.account_id = settings.chatwoot_account_id
        self.client = httpx.AsyncClient(
            headers={"api_access_token": self.api_key},
            timeout=30.0
        )
    
    async def send_message(
        self,
        conversation_id: int,
        content: str,
        private: bool = False,
        message_type: str = "outgoing"
    ) -> dict:
        """
        Send message to Chatwoot conversation
        
        Args:
            conversation_id: Chatwoot conversation ID
            content: Message content
            private: Whether message is private (internal note)
            message_type: 'outgoing' for bot, 'incoming' for user
        
        Returns:
            Message dict from Chatwoot API
        """
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
            
            response = await self.client.post(
                url,
                json={
                    "content": content,
                    "message_type": message_type,
                    "private": private
                }
            )
            
            response.raise_for_status()
            logger.info(f"Message sent to conversation {conversation_id}")
            return response.json()
        
        except httpx.HTTPStatusError as e:
            logger.error(f"Chatwoot API error sending message: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending message to Chatwoot: {e}")
            raise
    
    async def get_messages(self, conversation_id: int) -> list:
        """
        Get messages from a conversation
        
        Args:
            conversation_id: Chatwoot conversation ID
        
        Returns:
            List of message dicts
        """
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            messages = response.json()
            logger.info(f"Retrieved {len(messages)} messages from conversation {conversation_id}")
            return messages
        
        except Exception as e:
            logger.error(f"Error getting messages from Chatwoot: {e}")
            return []
    
    async def get_conversation(self, conversation_id: int) -> dict:
        """
        Get conversation details
        
        Args:
            conversation_id: Chatwoot conversation ID
        
        Returns:
            Conversation dict
        """
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}"
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            return response.json()
        
        except Exception as e:
            logger.error(f"Error getting conversation from Chatwoot: {e}")
            raise
    
    async def assign_conversation(
        self,
        conversation_id: int,
        agent_id: int = None,
        team_id: int = None
    ) -> dict:
        """
        Assign conversation to agent or team
        
        Args:
            conversation_id: Chatwoot conversation ID
            agent_id: Agent ID to assign to
            team_id: Team ID to assign to
        
        Returns:
            Updated conversation dict
        """
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/assignments"
            
            payload = {}
            if agent_id:
                payload["assignee_id"] = agent_id
            if team_id:
                payload["team_id"] = team_id
            
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            logger.info(f"Conversation {conversation_id} assigned")
            return response.json()
        
        except Exception as e:
            logger.error(f"Error assigning conversation: {e}")
            raise
    
    async def send_attachment(
        self,
        conversation_id: int,
        file_path: str,
        message_type: str = "outgoing",
        caption: Optional[str] = None
    ) -> dict:
        """
        Send a file attachment to a Chatwoot conversation
        
        Args:
            conversation_id: Chatwoot conversation ID
            file_path: Path to the file to send
            message_type: 'outgoing' for bot, 'incoming' for user
            caption: Optional text caption for the file
        
        Returns:
            Message dict from Chatwoot API
        """
        try:
            url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
            
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Prepare multipart form data
            files = {
                'attachments[]': (path.name, open(file_path, 'rb'))
            }
            
            data = {
                'message_type': message_type,
                'private': False
            }
            
            if caption:
                data['content'] = caption
            
            response = await self.client.post(
                url,
                files=files,
                data=data
            )
            
            response.raise_for_status()
            logger.info(f"Attachment sent to conversation {conversation_id}: {path.name}")
            return response.json()
        
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            raise
        except httpx.HTTPStatusError as e:
            logger.error(f"Chatwoot API error sending attachment: {e}")
            raise
        except Exception as e:
            logger.error(f"Error sending attachment to Chatwoot: {e}")
            raise
    
    async def send_template_sequence(
        self,
        conversation_id: int,
        messages: list,
        variables: dict = None
    ) -> list:
        """
        Send a sequence of messages (text, images, files) in order
        
        Args:
            conversation_id: Chatwoot conversation ID
            messages: List of message dicts with 'type', 'content', 'file_url', 'delay_seconds'
            variables: Optional dict to replace variables in text messages
        
        Returns:
            List of sent message responses
        """
        sent_messages = []
        
        try:
            # Sort messages by order
            sorted_messages = sorted(messages, key=lambda x: x.get('order', 0))
            
            for msg in sorted_messages:
                msg_type = msg.get('type', 'text')
                content = msg.get('content', '')
                file_url = msg.get('file_url')
                delay = msg.get('delay_seconds', 0)
                
                # Apply variable replacement for text messages
                if msg_type == 'text' and variables:
                    for key, value in variables.items():
                        content = content.replace(f'{{{key}}}', str(value))
                
                # Wait if delay is specified
                if delay > 0:
                    await asyncio.sleep(delay)
                
                # Send based on type
                if msg_type == 'text':
                    response = await self.send_message(
                        conversation_id=conversation_id,
                        content=content
                    )
                    sent_messages.append(response)
                else:
                    # For files (image, document, audio, video)
                    if not file_url:
                        logger.warning(f"Skipping {msg_type} message without file_url")
                        continue
                    
                    response = await self.send_attachment(
                        conversation_id=conversation_id,
                        file_path=file_url,
                        caption=content if content else None
                    )
                    sent_messages.append(response)
            
            logger.info(f"Template sequence sent to conversation {conversation_id}: {len(sent_messages)} messages")
            return sent_messages
        
        except Exception as e:
            logger.error(f"Error sending template sequence: {e}")
            raise
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Singleton instance
chatwoot_service = ChatwootService()
