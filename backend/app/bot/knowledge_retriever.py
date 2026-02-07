from sqlalchemy.orm import Session
from sqlalchemy import or_, func, String
from app.models.knowledge import Knowledge
from app.models.faq import FAQ
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class KnowledgeRetriever:
    """Search and retrieve relevant knowledge for answering questions"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def search_knowledge(self, query: str, limit: int = 5) -> List[Knowledge]:
        """
        Search for relevant knowledge items
        Uses simple keyword-based search
        
        Args:
            query: User's question
            limit: Maximum number of results
        
        Returns:
            List of relevant Knowledge items
        """
        search_terms = query.lower().split()
        
        knowledge_items = []
        seen_ids = set()
        
        for term in search_terms:
            if len(term) < 3:  # Skip very short words
                continue
            
            term_filter = f"%{term}%"
            
            results = self.db.query(Knowledge).filter(
                Knowledge.is_active == True
            ).filter(
                or_(
                    Knowledge.title.ilike(term_filter),
                    Knowledge.content.ilike(term_filter),
                    Knowledge.keywords.cast(String).ilike(term_filter)
                )
            ).order_by(
                Knowledge.priority.desc(),
                Knowledge.times_used.desc()
            ).limit(limit).all()
            
            for item in results:
                if item.id not in seen_ids:
                    knowledge_items.append(item)
                    seen_ids.add(item.id)
        
        # Sort by priority and usage
        knowledge_items.sort(key=lambda x: (x.priority, x.times_used), reverse=True)
        
        return knowledge_items[:limit]
    
    async def search_faqs(self, query: str, limit: int = 3) -> List[FAQ]:
        """
        Search for relevant FAQs
        
        Args:
            query: User's question
            limit: Maximum number of results
        
        Returns:
            List of relevant FAQ items
        """
        search_filter = f"%{query}%"
        
        faqs = self.db.query(FAQ).filter(
            FAQ.is_active == True
        ).filter(
            or_(
                FAQ.question.ilike(search_filter),
                FAQ.answer.ilike(search_filter),
                FAQ.question_variations.cast(String).ilike(search_filter),
                FAQ.tags.cast(String).ilike(search_filter)
            )
        ).order_by(
            FAQ.priority.desc(),
            FAQ.times_used.desc(),
            FAQ.helpful_count.desc()
        ).limit(limit).all()
        
        return faqs
    
    async def get_by_category(self, category: str, limit: int = 10) -> List[Knowledge]:
        """
        Get knowledge items by category
        
        Args:
            category: Category name
            limit: Maximum number of results
        
        Returns:
            List of Knowledge items in category
        """
        return self.db.query(Knowledge).filter(
            Knowledge.is_active == True,
            Knowledge.category == category
        ).order_by(
            Knowledge.priority.desc()
        ).limit(limit).all()
    
    async def update_usage_stats(self, knowledge_ids: List[int], faq_ids: List[int]):
        """
        Update usage statistics for knowledge and FAQs
        
        Args:
            knowledge_ids: List of Knowledge IDs that were used
            faq_ids: List of FAQ IDs that were used
        """
        now = datetime.now()
        
        try:
            # Update knowledge usage
            for kid in knowledge_ids:
                knowledge = self.db.query(Knowledge).filter(Knowledge.id == kid).first()
                if knowledge:
                    knowledge.times_used = (knowledge.times_used or 0) + 1
                    knowledge.last_used_at = now
            
            # Update FAQ usage
            for fid in faq_ids:
                faq = self.db.query(FAQ).filter(FAQ.id == fid).first()
                if faq:
                    faq.times_used = (faq.times_used or 0) + 1
            
            self.db.commit()
            logger.info(f"Updated usage stats: {len(knowledge_ids)} knowledge, {len(faq_ids)} FAQs")
        
        except Exception as e:
            logger.error(f"Error updating usage stats: {e}")
            self.db.rollback()
