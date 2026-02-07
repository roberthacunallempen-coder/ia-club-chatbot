from sqlalchemy.orm import Session
from app.models.message_template import MessageTemplate
from app.services.chatwoot_service import chatwoot_service
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class TemplateManager:
    """
    Manager for sending predefined message templates
    Handles template retrieval and sending
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    async def send_template_by_name(
        self,
        template_name: str,
        conversation_id: int,
        variables: Optional[dict] = None
    ) -> dict:
        """
        Send a template by its name
        
        Args:
            template_name: Name of the template to send
            conversation_id: Chatwoot conversation ID
            variables: Optional variables to replace in text messages
        
        Returns:
            dict with success status and details
        """
        try:
            # Get template
            template = self.db.query(MessageTemplate).filter(
                MessageTemplate.name == template_name,
                MessageTemplate.is_active == True
            ).first()
            
            if not template:
                logger.warning(f"Template '{template_name}' not found or inactive")
                return {
                    "success": False,
                    "error": f"Template '{template_name}' not found or inactive"
                }
            
            # Send sequence
            sent_messages = await chatwoot_service.send_template_sequence(
                conversation_id=conversation_id,
                messages=template.messages,
                variables=variables or {}
            )
            
            logger.info(f"Template '{template_name}' sent to conversation {conversation_id}")
            return {
                "success": True,
                "template_name": template_name,
                "messages_sent": len(sent_messages),
                "conversation_id": conversation_id
            }
        
        except Exception as e:
            logger.error(f"Error sending template '{template_name}': {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def send_template_by_id(
        self,
        template_id: int,
        conversation_id: int,
        variables: Optional[dict] = None
    ) -> dict:
        """
        Send a template by its ID
        
        Args:
            template_id: ID of the template to send
            conversation_id: Chatwoot conversation ID
            variables: Optional variables to replace in text messages
        
        Returns:
            dict with success status and details
        """
        try:
            # Get template
            template = self.db.query(MessageTemplate).filter(
                MessageTemplate.id == template_id,
                MessageTemplate.is_active == True
            ).first()
            
            if not template:
                logger.warning(f"Template ID {template_id} not found or inactive")
                return {
                    "success": False,
                    "error": f"Template ID {template_id} not found or inactive"
                }
            
            # Send sequence
            sent_messages = await chatwoot_service.send_template_sequence(
                conversation_id=conversation_id,
                messages=template.messages,
                variables=variables or {}
            )
            
            logger.info(f"Template '{template.name}' (ID: {template_id}) sent to conversation {conversation_id}")
            return {
                "success": True,
                "template_name": template.name,
                "messages_sent": len(sent_messages),
                "conversation_id": conversation_id
            }
        
        except Exception as e:
            logger.error(f"Error sending template ID {template_id}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_template_by_keyword(self, message: str) -> Optional[MessageTemplate]:
        """
        Find a template that matches keywords in the message
        
        Args:
            message: User's message
        
        Returns:
            MessageTemplate if found, None otherwise
        """
        try:
            message_lower = message.lower()
            
            # Get all active templates with keywords
            templates = self.db.query(MessageTemplate).filter(
                MessageTemplate.is_active == True,
                MessageTemplate.trigger_keywords.isnot(None)
            ).all()
            
            # Check each template's keywords
            for template in templates:
                if template.trigger_keywords:
                    for keyword in template.trigger_keywords:
                        if keyword.lower() in message_lower:
                            logger.info(f"Template '{template.name}' matched by keyword '{keyword}'")
                            return template
            
            return None
        
        except Exception as e:
            logger.error(f"Error finding template by keyword: {e}")
            return None
    
    async def auto_send_template(
        self,
        message: str,
        conversation_id: int,
        variables: Optional[dict] = None
    ) -> Optional[dict]:
        """
        Automatically find and send a template based on message keywords
        
        Args:
            message: User's message
            conversation_id: Chatwoot conversation ID
            variables: Optional variables to replace in text messages
        
        Returns:
            dict with result if template found and sent, None otherwise
        """
        try:
            # Find matching template
            template = self.find_template_by_keyword(message)
            
            if not template:
                return None
            
            # Send template
            result = await self.send_template_by_name(
                template_name=template.name,
                conversation_id=conversation_id,
                variables=variables
            )
            
            return result
        
        except Exception as e:
            logger.error(f"Error auto-sending template: {e}")
            return None
    
    def get_available_templates(self, category: Optional[str] = None) -> List[MessageTemplate]:
        """
        Get list of available active templates
        
        Args:
            category: Optional category filter
        
        Returns:
            List of MessageTemplate objects
        """
        query = self.db.query(MessageTemplate).filter(
            MessageTemplate.is_active == True
        )
        
        if category:
            query = query.filter(MessageTemplate.category == category)
        
        return query.all()
