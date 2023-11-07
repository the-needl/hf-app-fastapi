from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base

class KEYModel(Base):
    """
    A conversation with messages and linked documents
    """

    messages = relationship("Message", back_populates="conversation")
    conversation_documents = relationship(
        "ConversationDocument", back_populates="conversation"
    )
