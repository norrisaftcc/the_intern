"""
Integration Tests - Full System Harmony
Testing the beautiful symphony of components working together
"""

import pytest
import asyncio
import tempfile
import os
import sys
from fastapi.testclient import TestClient

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Import system components
from app import app
from database import Base, create_engine, sessionmaker, get_or_create_user
from terminal_integration import TerminalCommands

@pytest.fixture
def test_client():
    """Create test client for FastAPI app"""
    return TestClient(app)

@pytest.fixture
def terminal_system():
    """Create terminal command system for testing"""
    return TerminalCommands()

@pytest.fixture
def test_db_session():
    """Create isolated test database session"""
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

class TestApplicationStartup:
    """Test that the application starts correctly"""
    
    def test_app_health(self, test_client):
        """Test basic application health"""
        # Test the root endpoint (if it exists)
        response = test_client.get("/")
        # FastAPI returns 404 for undefined routes, which is expected
        assert response.status_code in [200, 404]
    
    def test_openapi_docs(self, test_client):
        """Test that API documentation is available"""
        response = test_client.get("/docs")
        assert response.status_code == 200
    
    def test_openapi_schema(self, test_client):
        """Test that OpenAPI schema is available"""
        response = test_client.get("/openapi.json")
        assert response.status_code == 200
        assert "AlgoCratic Futures" in response.json()["info"]["title"]

class TestRoomSystem:
    """Test room loading and navigation"""
    
    def test_room_loading(self, terminal_system):
        """Test that rooms are loaded from YAML files"""
        assert len(terminal_system.world.rooms) > 0
        
        # Should have key rooms
        room_ids = list(terminal_system.world.rooms.keys())
        assert any('boardwalk' in room_id for room_id in room_ids)
        assert any('arcade' in room_id for room_id in room_ids)
    
    def test_player_movement(self, terminal_system):
        """Test basic player movement between rooms"""
        player_id = "test_player"
        
        # Start player at default location
        response = terminal_system.process_command(player_id, "look")
        assert 'type' in response
        # The response type might be 'room_description' or 'error' depending on room setup
        
        # Test movement command
        response = terminal_system.process_command(player_id, "arcade")
        # Should either move successfully or give appropriate response
        assert 'type' in response
        assert response['type'] in ['movement', 'room_description', 'error']
    
    def test_help_command(self, terminal_system):
        """Test help system"""
        response = terminal_system.process_command("test_player", "help")
        
        assert response['type'] == 'help'
        assert 'message' in response
        assert 'Movement:' in response['message']
        assert 'Social:' in response['message']

class TestAgentInteraction:
    """Test full agent interaction pipeline"""
    
    def test_liza_conversation_flow(self, terminal_system, test_db_session):
        """Test complete conversation flow with Liza"""
        player_id = "test_player"
        user = get_or_create_user(test_db_session, player_id, "test@example.com")
        
        # Test talking to Liza
        response = terminal_system.process_command(player_id, "talk to liza")
        
        # Should get a conversation response
        assert 'type' in response
        # Response type might vary based on implementation
        assert len(str(response)) > 50  # Should be substantial
    
    def test_conversation_with_topics(self, terminal_system):
        """Test conversation responses to different topics"""
        player_id = "topic_tester"
        
        topics = [
            "talk to liza about drains",
            "talk to liza about assessment", 
            "talk to liza about help",
            "talk to liza about the orb"
        ]
        
        for topic in topics:
            response = terminal_system.process_command(player_id, topic)
            # Should get some kind of response for each topic
            assert response is not None

class TestDatabaseIntegration:
    """Test database integration with game systems"""
    
    def test_user_creation_on_connection(self, test_db_session):
        """Test that users are created when they connect"""
        user = get_or_create_user(test_db_session, "new_player", "new@example.com")
        
        assert user.username == "new_player"
        assert user.current_room == "boardwalk"
        assert user.session_count == 0
    
    def test_conversation_persistence(self, test_db_session):
        """Test that conversations are saved to database"""
        from database import log_conversation, ConversationHistory
        
        user = get_or_create_user(test_db_session, "chat_user", "chat@example.com")
        
        # Log a conversation
        log_conversation(
            test_db_session, user.id, "liza", 
            "hello", "Hello there!", "boardwalk"
        )
        
        # Verify it was saved
        conversations = test_db_session.query(ConversationHistory).filter(
            ConversationHistory.user_id == user.id
        ).all()
        
        assert len(conversations) == 1
        assert conversations[0].agent_id == "liza"
    
    def test_progress_tracking(self, test_db_session):
        """Test student progress tracking"""
        from database import update_student_progress, StudentProgress
        
        user = get_or_create_user(test_db_session, "progress_user", "progress@example.com")
        
        # Update progress
        update_student_progress(
            test_db_session, user.id,
            liza_conversations=5,
            exploration_score=75
        )
        
        # Verify progress was saved
        progress = test_db_session.query(StudentProgress).filter(
            StudentProgress.user_id == user.id
        ).first()
        
        assert progress.liza_conversations == 5
        assert progress.exploration_score == 75

class TestErrorHandling:
    """Test system resilience and error handling"""
    
    def test_invalid_commands(self, terminal_system):
        """Test handling of invalid commands"""
        player_id = "error_tester"
        
        invalid_commands = [
            "definitely_not_a_command",
            "talk to nobody",
            "go to narnia",
            ""  # Empty command
        ]
        
        for cmd in invalid_commands:
            response = terminal_system.process_command(player_id, cmd)
            # Should get some response, not crash
            assert response is not None
            assert 'type' in response
    
    def test_malformed_input(self, terminal_system):
        """Test handling of malformed input"""
        player_id = "malform_tester"
        
        malformed_inputs = [
            "talk to" + " " * 1000,  # Very long spaces
            "talk to liza" + "x" * 10000,  # Very long input
            "talk\tto\nliza",  # Special characters
        ]
        
        for cmd in malformed_inputs:
            try:
                response = terminal_system.process_command(player_id, cmd)
                assert response is not None
            except Exception as e:
                # Should not crash, but if it does, fail the test
                pytest.fail(f"System crashed on input '{cmd[:50]}...': {e}")

class TestPerformance:
    """Test basic performance characteristics"""
    
    def test_command_response_time(self, terminal_system):
        """Test that commands respond in reasonable time"""
        import time
        
        player_id = "speed_tester"
        
        start_time = time.time()
        response = terminal_system.process_command(player_id, "look")
        end_time = time.time()
        
        # Should respond within 1 second for basic commands
        response_time = end_time - start_time
        assert response_time < 1.0
    
    def test_multiple_concurrent_players(self, terminal_system):
        """Test handling multiple players simultaneously"""
        import threading
        import time
        
        responses = {}
        
        def player_session(player_id):
            """Simulate a player session"""
            commands = ["look", "help", "talk to liza"]
            player_responses = []
            
            for cmd in commands:
                response = terminal_system.process_command(player_id, cmd)
                player_responses.append(response)
                time.sleep(0.1)  # Small delay between commands
            
            responses[player_id] = player_responses
        
        # Create multiple player threads
        threads = []
        for i in range(5):
            player_id = f"concurrent_player_{i}"
            thread = threading.Thread(target=player_session, args=(player_id,))
            threads.append(thread)
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join(timeout=10)  # 10 second timeout
        
        # Check that all players got responses
        assert len(responses) == 5
        for player_id, player_responses in responses.items():
            assert len(player_responses) == 3  # Should have 3 responses
            for response in player_responses:
                assert response is not None

if __name__ == "__main__":
    # Run integration tests
    pytest.main(["-v", __file__])