"""
Agent Conversation System Tests
Ensuring our digital actors perform their roles with consistency and charm
"""

import pytest
import tempfile
import os
import sys

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from agent_conversation import AgentConversation
from database import Base, get_or_create_user, create_engine, sessionmaker

@pytest.fixture
def conversation_system():
    """Create an agent conversation system for testing"""
    return AgentConversation()

@pytest.fixture
def test_db():
    """Create a temporary test database"""
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

class TestAgentLoading:
    """Test that agents are properly loaded from YAML files"""
    
    def test_liza_loaded(self, conversation_system):
        """Test that Liza is loaded correctly"""
        assert 'liza' in conversation_system.agents
        
        liza = conversation_system.agents['liza']
        assert 'personality' in liza
        assert 'examples' in liza
        assert 'nonverbal' in liza
    
    def test_liza_personality_data(self, conversation_system):
        """Test that Liza's personality data is loaded"""
        liza = conversation_system.agents['liza']
        personality = liza['personality']
        
        assert personality['agent_id'] == 'liza'
        assert personality['full_name'] == 'Dr. Elizabeth Anderson'
        assert personality['preferred_name'] == 'LIZA'
        assert 'traits' in personality
    
    def test_liza_conversation_examples(self, conversation_system):
        """Test that Liza's conversation examples are loaded"""
        liza = conversation_system.agents['liza']
        examples = liza['examples']
        
        assert 'greetings' in examples
        assert 'hints_and_guidance' in examples
        assert 'technical_discussions' in examples
        assert 'personality_quirks' in examples

class TestBasicConversation:
    """Test basic conversation patterns without database"""
    
    def test_greeting_first_meeting(self, conversation_system):
        """Test first meeting greeting"""
        response = conversation_system.talk_to_agent('liza', 'hello')
        
        assert 'Dr. Anderson here' in response
        assert 'call me LIZA' in response
        assert '[*Monocle adjusts' in response
    
    def test_greeting_variations(self, conversation_system):
        """Test different greeting variations"""
        greetings = ['hello', 'hi', 'hey', 'greetings']
        
        for greeting in greetings:
            response = conversation_system.talk_to_agent('liza', greeting)
            assert len(response) > 50  # Should get a substantial response
            assert '[*' in response  # Should include nonverbal behavior
    
    def test_topic_based_responses(self, conversation_system):
        """Test responses to specific topics"""
        # Test drain/tunnel topic
        response = conversation_system.talk_to_agent('liza', 'tell me about drains')
        assert 'animation sequences' in response
        assert 'water flows' in response
        
        # Test assessment topic
        response = conversation_system.talk_to_agent('liza', 'what about assessment?')
        assert 'quality control' in response
        assert 'animation' in response
        
        # Test help topic
        response = conversation_system.talk_to_agent('liza', 'I need help debugging')
        assert 'frame-by-frame analysis' in response
        assert 'glitch' in response
    
    def test_orb_team_reference(self, conversation_system):
        """Test Team Orb references"""
        response = conversation_system.talk_to_agent('liza', 'tell me about the orb')
        
        assert 'Orb teaches us' in response
        assert 'duality' in response
        assert 'orbital' in response
    
    def test_unknown_agent(self, conversation_system):
        """Test talking to non-existent agent"""
        response = conversation_system.talk_to_agent('unknown_agent', 'hello')
        assert response == "That person doesn't seem to be here."
    
    def test_default_response(self, conversation_system):
        """Test default response for unrecognized input"""
        response = conversation_system.talk_to_agent('liza', 'random nonsense input')
        
        assert '[*' in response  # Should include nonverbal
        assert 'frames in an animation' in response
        assert 'What specific aspect intrigues you?' in response

class TestConversationWithDatabase:
    """Test conversation system with database integration"""
    
    def test_first_vs_returning_conversation(self, conversation_system, test_db):
        """Test different responses for first-time vs returning users"""
        user = get_or_create_user(test_db, "test_user", "test@example.com")
        
        # First conversation (should be first meeting)
        response1 = conversation_system.talk_to_agent(
            'liza', 'hello', 
            db=test_db, user_id=user.id, room_location='boardwalk'
        )
        assert 'New to our' in response1
        
        # Second conversation (should be returning player)
        response2 = conversation_system.talk_to_agent(
            'liza', 'hello',
            db=test_db, user_id=user.id, room_location='boardwalk'
        )
        assert 'you\'ve returned' in response2
    
    def test_conversation_logging(self, conversation_system, test_db):
        """Test that conversations are properly logged"""
        user = get_or_create_user(test_db, "logger_user", "logger@example.com")
        
        # Have a conversation
        response = conversation_system.talk_to_agent(
            'liza', 'hello there',
            db=test_db, user_id=user.id, room_location='boardwalk'
        )
        
        # Check that conversation was logged
        from database import ConversationHistory
        conversations = test_db.query(ConversationHistory).filter(
            ConversationHistory.user_id == user.id
        ).all()
        
        assert len(conversations) == 1
        assert conversations[0].agent_id == 'liza'
        assert conversations[0].user_input == 'hello there'
        assert conversations[0].room_location == 'boardwalk'
    
    def test_progress_tracking(self, conversation_system, test_db):
        """Test that Liza conversations update student progress"""
        user = get_or_create_user(test_db, "progress_user", "progress@example.com")
        
        # Have multiple conversations
        for i in range(3):
            conversation_system.talk_to_agent(
                'liza', f'conversation {i}',
                db=test_db, user_id=user.id, room_location='boardwalk'
            )
        
        # Check progress
        from database import StudentProgress
        progress = test_db.query(StudentProgress).filter(
            StudentProgress.user_id == user.id
        ).first()
        
        assert progress.liza_conversations == 3

class TestNonverbalBehaviors:
    """Test agent nonverbal behavior system"""
    
    def test_idle_emote(self, conversation_system):
        """Test getting idle emotes"""
        emote = conversation_system.get_agent_emote('liza', 'idle')
        
        assert isinstance(emote, str)
        assert len(emote) > 0
        # Should be one of the common idle animations
    
    def test_emotional_emotes(self, conversation_system):
        """Test emotional state emotes"""
        # Test various emotional states if they exist
        emotions = ['idle', 'focused', 'confused', 'excited']
        
        for emotion in emotions:
            emote = conversation_system.get_agent_emote('liza', emotion)
            assert isinstance(emote, str)
    
    def test_unknown_agent_emote(self, conversation_system):
        """Test emote for unknown agent"""
        emote = conversation_system.get_agent_emote('unknown_agent', 'idle')
        assert emote == ""

class TestConversationRobustness:
    """Test edge cases and error handling"""
    
    def test_empty_input(self, conversation_system):
        """Test handling of empty input"""
        response = conversation_system.talk_to_agent('liza', '')
        assert len(response) > 0  # Should still provide a response
    
    def test_very_long_input(self, conversation_system):
        """Test handling of very long input"""
        long_input = "hello " * 1000  # Very long greeting
        response = conversation_system.talk_to_agent('liza', long_input)
        
        # Should still recognize as greeting
        assert 'Dr. Anderson' in response or 'returned' in response
    
    def test_case_insensitive_matching(self, conversation_system):
        """Test that keyword matching is case insensitive"""
        responses = []
        
        # Test different cases
        variations = ['HELLO', 'Hello', 'hello', 'HeLLo']
        
        for variation in variations:
            response = conversation_system.talk_to_agent('liza', variation)
            responses.append(response)
        
        # All should trigger greeting responses
        for response in responses:
            assert 'Dr. Anderson' in response or 'returned' in response
    
    def test_database_error_handling(self, conversation_system):
        """Test graceful handling of database errors"""
        # Test with invalid database session
        response = conversation_system.talk_to_agent(
            'liza', 'hello',
            db=None, user_id=1, room_location='boardwalk'
        )
        
        # Should still work without database
        assert len(response) > 0
        assert 'Dr. Anderson' in response

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main(["-v", __file__])