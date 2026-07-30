"""
Database System Tests
Verifying that our persistence layer works as elegantly as it was designed
"""

import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Import our database components
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from database import Base, User, ConversationHistory, StudentProgress, SystemLog
from database import get_or_create_user, log_conversation, update_student_progress, log_system_event

@pytest.fixture
def test_db():
    """Create a temporary test database"""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(bind=engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    yield db
    
    # Cleanup
    db.close()
    os.close(db_fd)
    os.unlink(db_path)

class TestUserManagement:
    """Test user creation and management"""
    
    def test_create_new_user(self, test_db):
        """Test creating a new user account"""
        user = get_or_create_user(test_db, "alice", "alice@example.com")
        
        assert user.username == "alice"
        assert user.email == "alice@example.com"
        assert user.clearance_level == "BRONZE_CODER"
        assert user.session_count == 0
        assert user.current_room == "boardwalk"
        assert user.is_active is True
    
    def test_retrieve_existing_user(self, test_db):
        """Test retrieving an existing user"""
        # Create user first
        user1 = get_or_create_user(test_db, "bob", "bob@example.com")
        original_id = user1.id
        original_created = user1.created_at
        
        # Retrieve the same user
        user2 = get_or_create_user(test_db, "bob", "bob@example.com")
        
        assert user2.id == original_id
        assert user2.created_at == original_created
        assert user2.session_count == 1  # Should increment
    
    def test_user_progress_creation(self, test_db):
        """Test that user progress is created with new users"""
        user = get_or_create_user(test_db, "charlie", "charlie@example.com")
        
        # Check that progress record was created
        progress = test_db.query(StudentProgress).filter(
            StudentProgress.user_id == user.id
        ).first()
        
        assert progress is not None
        assert progress.liza_conversations == 0
        assert progress.found_storm_drains is False

class TestConversationLogging:
    """Test agent conversation tracking"""
    
    def test_log_conversation(self, test_db):
        """Test logging a conversation between user and agent"""
        user = get_or_create_user(test_db, "diana", "diana@example.com")
        
        conversation = log_conversation(
            db=test_db,
            user_id=user.id,
            agent_id="liza",
            user_input="hello",
            agent_response="Hello there!",
            room_location="boardwalk",
            context={"first_meeting": True}
        )
        
        assert conversation.user_id == user.id
        assert conversation.agent_id == "liza"
        assert conversation.user_input == "hello"
        assert conversation.agent_response == "Hello there!"
        assert conversation.room_location == "boardwalk"
        assert '"first_meeting": true' in conversation.conversation_context.lower()
    
    def test_conversation_history_retrieval(self, test_db):
        """Test retrieving conversation history"""
        user = get_or_create_user(test_db, "eve", "eve@example.com")
        
        # Log multiple conversations
        log_conversation(test_db, user.id, "liza", "hello", "Hello!", "boardwalk")
        log_conversation(test_db, user.id, "liza", "how are you?", "I'm well!", "boardwalk")
        
        # Retrieve conversations
        conversations = test_db.query(ConversationHistory).filter(
            ConversationHistory.user_id == user.id
        ).all()
        
        assert len(conversations) == 2
        assert conversations[0].user_input == "hello"
        assert conversations[1].user_input == "how are you?"

class TestStudentProgress:
    """Test educational progress tracking"""
    
    def test_update_progress(self, test_db):
        """Test updating student progress metrics"""
        user = get_or_create_user(test_db, "frank", "frank@example.com")
        
        # Update progress
        progress = update_student_progress(
            db=test_db,
            user_id=user.id,
            liza_conversations=5,
            found_storm_drains=True,
            exploration_score=85
        )
        
        assert progress.liza_conversations == 5
        assert progress.found_storm_drains is True
        assert progress.exploration_score == 85
    
    def test_progress_json_fields(self, test_db):
        """Test JSON field storage for complex data"""
        user = get_or_create_user(test_db, "grace", "grace@example.com")
        
        import json
        rooms_visited = ["boardwalk", "arcade", "storm_drain"]
        
        progress = update_student_progress(
            db=test_db,
            user_id=user.id,
            rooms_visited=json.dumps(rooms_visited)
        )
        
        assert progress.rooms_visited == json.dumps(rooms_visited)
        
        # Test that we can parse it back
        parsed_rooms = json.loads(progress.rooms_visited)
        assert parsed_rooms == rooms_visited

class TestSystemLogging:
    """Test system event logging"""
    
    def test_log_system_event(self, test_db):
        """Test logging system events"""
        user = get_or_create_user(test_db, "henry", "henry@example.com")
        
        log_entry = log_system_event(
            db=test_db,
            level="INFO",
            component="websocket",
            message="User connected successfully",
            user_id=user.id,
            additional_data={"session_id": "abc123", "room": "boardwalk"}
        )
        
        assert log_entry.level == "INFO"
        assert log_entry.component == "websocket"
        assert log_entry.message == "User connected successfully"
        assert log_entry.user_id == user.id
        assert '"session_id": "abc123"' in log_entry.additional_data
    
    def test_log_without_user(self, test_db):
        """Test logging system events without user context"""
        log_entry = log_system_event(
            db=test_db,
            level="WARNING",
            component="room_system",
            message="Room file could not be loaded"
        )
        
        assert log_entry.level == "WARNING"
        assert log_entry.component == "room_system"
        assert log_entry.user_id is None

class TestDatabaseIntegrity:
    """Test database relationships and constraints"""
    
    def test_user_conversation_relationship(self, test_db):
        """Test the relationship between users and conversations"""
        user = get_or_create_user(test_db, "iris", "iris@example.com")
        
        # Add conversations
        log_conversation(test_db, user.id, "liza", "test1", "response1", "boardwalk")
        log_conversation(test_db, user.id, "liza", "test2", "response2", "arcade")
        
        # Test relationship
        conversations = user.conversations
        assert len(conversations) == 2
        assert conversations[0].user_input == "test1"
    
    def test_user_progress_relationship(self, test_db):
        """Test the relationship between users and progress records"""
        user = get_or_create_user(test_db, "jack", "jack@example.com")
        
        # Progress should be automatically created
        progress_records = user.progress_records
        assert len(progress_records) == 1
        
        # Update progress
        update_student_progress(test_db, user.id, exploration_score=75)
        
        # Check updated relationship
        updated_progress = user.progress_records[0]
        assert updated_progress.exploration_score == 75

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main(["-v", __file__])