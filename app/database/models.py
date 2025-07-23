import os

from dotenv import load_dotenv

from sqlalchemy import Column, Boolean, Integer, String, DateTime, ForeignKey, JSON, create_engine
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, sessionmaker

from app.service.crypto import decrypt_data

Base = declarative_base()

class IA(Base):
    __tablename__   = "ias"
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    status = Column(Boolean, nullable=False, unique=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

Prompt = relationship("Prompt", back_populates="ia")
ia_config = relationship("IaConfig", back_populates="ia", uselist=False)
Leads = relationship("lead", back_populates="ia", uselist=False)

@property
def active_prompt(self):
    active = [p for p in self.prompts if p.is_active]
    return active[0] if active else None
    print (f"Ia LOCALIZADA:{ia.name} - {ia.phone_number}")
    return IA

class IAConfig(Base):
    __tablename__   = "ia_config"
    id = Column(Integer, primary_key = True, index=True)
    ia_id = Column(Integer, ForeignKey("ias.id"), index=True)
    channel = Column(String, nullable=False)
    ai_api = Column(String, nullable=False)
    encrypted_credentials=Column(String, nullable=False)
    
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
  
    ia = relationship("IA", back_populates="ia_config")
    
    @property
    def credentials(self):
        return decrypt_data(self.encrypted_credentials)
    

class Lead(Base):
    __tablename__   = "leads"
    
    id = Column(Integer, primary_key = True, index=True)
    ia_id = Column(Integer, ForeignKey("ias.id"), index=True)
    name = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    message = Column(MutableList.as_mutable(JSON), nullable=False)
    resume = Column(String, nullable=False)
    
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    leads = relationship("Leads", back_populates="ia")

class Prompt(Base):
    __tablename__   = "prompts"
    
    id = Column(Integer, primary_key = True, index=True)
    name = Column(String, nullable=False, unique=True)
    phone_number = Column(String, nullable=False, unique=True)
    status = Column(Boolean, nullable=False, unique=True)
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    ia = relationship("IA", back_populates="prompts")