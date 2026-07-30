"""
Database Models and Connection Management
AlgoCratic Futures Platform

This module provides the foundation for persistent data storage,
transforming ephemeral corporate surveillance theater into 
enduring educational record-keeping.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class User(Base):
    """
    User accounts in the AlgoCratic system
    Balances corporate tracking with educational privacy
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    clearance_level = Column(String(50), default="BRONZE_CODER")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Educational tracking
    current_room = Column(String(100), default="boardwalk")
    session_count = Column(Integer, default=0)
    
    # Relationships
    conversations = relationship("ConversationHistory", back_populates="user")
    progress_records = relationship("StudentProgress", back_populates="user")

class ConversationHistory(Base):
    """
    Agent conversation tracking
    Preserves the narrative continuity that makes our agents feel alive
    """
    __tablename__ = "conversation_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(String(50), nullable=False)  # e.g., 'liza'
    user_input = Column(Text, nullable=False)
    agent_response = Column(Text, nullable=False)
    conversation_context = Column(Text, nullable=True)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)
    room_location = Column(String(100), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")

class StudentProgress(Base):
    """
    Educational progress tracking
    The real metrics that matter for learning, not surveillance
    """
    __tablename__ = "student_progress"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Navigation and exploration
    rooms_visited = Column(Text, nullable=True)  # JSON list of room IDs
    commands_used = Column(Text, nullable=True)  # JSON list of command types
    exploration_score = Column(Integer, default=0)
    
    # Agent interactions
    liza_conversations = Column(Integer, default=0)
    conversation_quality_score = Column(Integer, default=0)
    
    # Learning milestones
    found_storm_drains = Column(Boolean, default=False)
    completed_tutorials = Column(Text, nullable=True)  # JSON list
    assessment_scores = Column(Text, nullable=True)  # JSON object
    
    # Temporal tracking
    session_start = Column(DateTime, default=datetime.utcnow)
    session_end = Column(DateTime, nullable=True)
    total_time_minutes = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")

class SystemLog(Base):
    """
    System events and operational monitoring
    Where we track the health of our educational rebellion
    """
    __tablename__ = "system_logs"
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    component = Column(String(50), nullable=False)  # websocket, agent, room_system, etc.
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    additional_data = Column(Text, nullable=True)  # JSON for detailed context

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///algocratic_futures.db")
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Database session dependency for FastAPI
    Ensures proper connection management and cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Initialize database schema
    Call this during application startup
    """
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created/verified")

def get_or_create_user(db, username: str, email: str = None) -> User:
    """
    Retrieve existing user or create new one
    Handles the corporate employee onboarding process
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(
            username=username,
            email=email,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        # Create initial progress record
        progress = StudentProgress(user_id=user.id)
        db.add(progress)
        db.commit()
        
    else:
        # Update last active time
        user.last_active = datetime.utcnow()
        user.session_count += 1
        db.commit()
    
    return user

def log_conversation(db, user_id: int, agent_id: str, user_input: str, 
                    agent_response: str, room_location: str = None, 
                    context: dict = None):
    """
    Record agent conversation for continuity and analysis
    The digital breadcrumbs that help our agents remember relationships
    """
    import json
    
    conversation = ConversationHistory(
        user_id=user_id,
        agent_id=agent_id,
        user_input=user_input,
        agent_response=agent_response,
        room_location=room_location,
        conversation_context=json.dumps(context) if context else None,
        timestamp=datetime.utcnow()
    )
    db.add(conversation)
    db.commit()
    return conversation

def update_student_progress(db, user_id: int, **progress_updates):
    """
    Update student learning progress
    The educational metrics that actually matter
    """
    progress = db.query(StudentProgress).filter(
        StudentProgress.user_id == user_id
    ).first()
    
    if not progress:
        progress = StudentProgress(user_id=user_id)
        db.add(progress)
    
    for key, value in progress_updates.items():
        if hasattr(progress, key):
            setattr(progress, key, value)
    
    db.commit()
    return progress

def log_system_event(db, level: str, component: str, message: str, 
                    user_id: int = None, additional_data: dict = None):
    """
    Record system events for monitoring and debugging
    Our window into the soul of the platform
    """
    import json
    
    log_entry = SystemLog(
        level=level.upper(),
        component=component,
        message=message,
        user_id=user_id,
        additional_data=json.dumps(additional_data) if additional_data else None
    )
    db.add(log_entry)
    db.commit()
    return log_entry