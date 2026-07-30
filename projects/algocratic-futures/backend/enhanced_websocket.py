"""
Enhanced WebSocket Handlers with Robust Error Handling
Transforming silent failures into graceful degradation with user communication
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Optional
from fastapi import WebSocket, WebSocketDisconnect

from database import get_db, get_or_create_user, log_system_event
from terminal_integration import terminal

logger = logging.getLogger(__name__)

class EnhancedConnectionManager:
    """Enhanced connection manager with error handling and monitoring"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_metadata: Dict[str, dict] = {}
        
    async def connect(self, websocket: WebSocket, user_id: str):
        """Connect with enhanced error handling and metadata tracking"""
        try:
            await websocket.accept()
            self.active_connections[user_id] = websocket
            self.connection_metadata[user_id] = {
                "connected_at": datetime.now(),
                "message_count": 0,
                "last_activity": datetime.now()
            }
            logger.info(f"User {user_id} connected via WebSocket")
        except Exception as e:
            logger.error(f"Failed to connect user {user_id}: {e}")
            raise
        
    def disconnect(self, user_id: str):
        """Disconnect with cleanup"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.connection_metadata:
            duration = datetime.now() - self.connection_metadata[user_id]["connected_at"]
            logger.info(f"User {user_id} disconnected after {duration}")
            del self.connection_metadata[user_id]
    
    async def send_safe(self, user_id: str, message: dict):
        """Send message with error handling"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
                if user_id in self.connection_metadata:
                    self.connection_metadata[user_id]["message_count"] += 1
                    self.connection_metadata[user_id]["last_activity"] = datetime.now()
                return True
            except Exception as e:
                logger.warning(f"Failed to send message to {user_id}: {e}")
                self.disconnect(user_id)
                return False
        return False

# Global enhanced connection manager
enhanced_manager = EnhancedConnectionManager()

async def enhanced_terminal_websocket(websocket: WebSocket, player_id: str):
    """Enhanced WebSocket endpoint with comprehensive error handling"""
    db = next(get_db())
    user = None
    
    try:
        # Accept connection with timeout
        await asyncio.wait_for(websocket.accept(), timeout=10.0)
        
        # Get or create user for session tracking
        user = get_or_create_user(db, player_id)
        
        # Log connection
        log_system_event(
            db=db, level="INFO", component="websocket",
            message=f"Terminal connection established for {player_id}",
            user_id=user.id
        )
        
        # Send enhanced welcome message
        await websocket.send_json({
            "type": "system",
            "message": f"=== TERMINAL ACCESS GRANTED ===\nWelcome, {player_id}\nSession ID: {user.session_count}\nClearance: PENDING",
            "user_id": user.id,
            "session_count": user.session_count
        })
        
        # Show initial room with error handling
        try:
            response = terminal.process_command(player_id, "look")
            await websocket.send_json(response)
        except Exception as e:
            logger.warning(f"Failed to load initial room for {player_id}: {e}")
            await websocket.send_json({
                "type": "error",
                "message": "Welcome! The system is initializing your workspace...",
                "recoverable": True
            })
        
        # Main command loop with enhanced error handling
        while True:
            try:
                # Receive command with timeout
                command = await asyncio.wait_for(websocket.receive_text(), timeout=300.0)  # 5 min timeout
                
                # Validate command length and content
                if len(command) > 1000:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Command too long. Please keep commands under 1000 characters.",
                        "recoverable": True
                    })
                    continue
                
                # Process through terminal integration with error handling
                try:
                    response = terminal.process_command(player_id, command.strip())
                    
                    # Enhance response with session info if needed
                    if isinstance(response, dict) and user:
                        response["session_id"] = user.id
                    
                    await websocket.send_json(response)
                    
                except Exception as cmd_error:
                    logger.error(f"Command processing error for {player_id} ('{command}'): {cmd_error}")
                    
                    # Log the error
                    log_system_event(
                        db=db, level="ERROR", component="terminal_command",
                        message=f"Command processing failed: {str(cmd_error)}",
                        user_id=user.id if user else None,
                        additional_data={"command": command, "error": str(cmd_error)}
                    )
                    
                    # Send user-friendly error response
                    await websocket.send_json({
                        "type": "error",
                        "message": "The system experienced a brief glitch. Try rephrasing your command or type 'help' for assistance.",
                        "recoverable": True,
                        "suggested_commands": ["look", "help", "status"]
                    })
                    
            except asyncio.TimeoutError:
                # Connection idle too long
                await websocket.send_json({
                    "type": "system",
                    "message": "⚠️  Connection idle detected. Type any command to continue.",
                    "timeout_warning": True
                })
                
            except WebSocketDisconnect:
                # Client disconnected normally
                logger.info(f"Client {player_id} disconnected normally")
                break
                
            except json.JSONDecodeError as json_error:
                # Malformed JSON in command
                logger.warning(f"JSON decode error for {player_id}: {json_error}")
                await websocket.send_json({
                    "type": "error", 
                    "message": "Command format error. Please try again.",
                    "recoverable": True
                })
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for {player_id}")
        
    except asyncio.TimeoutError:
        logger.warning(f"WebSocket connection timeout for {player_id}")
        try:
            await websocket.send_json({
                "type": "system",
                "message": "Connection timeout. Please reconnect.",
                "timeout": True
            })
        except:
            pass  # Connection might already be closed
            
    except Exception as e:
        logger.error(f"Unexpected WebSocket error for {player_id}: {e}", exc_info=True)
        
        # Log critical error
        if user:
            try:
                log_system_event(
                    db=db, level="CRITICAL", component="websocket",
                    message=f"Unexpected WebSocket error: {str(e)}",
                    user_id=user.id,
                    additional_data={"error_type": type(e).__name__, "error_details": str(e)}
                )
            except:
                pass  # Don't let logging errors crash the handler
        
        # Attempt to send user-friendly error message
        try:
            await websocket.send_json({
                "type": "error",
                "message": "A system error occurred. Please reconnect to continue your session.",
                "recoverable": False,
                "reconnect_suggested": True
            })
        except:
            pass  # Connection might be broken
            
    finally:
        # Cleanup and logging
        if user:
            try:
                log_system_event(
                    db=db, level="INFO", component="websocket",
                    message=f"Terminal session ended for {player_id}",
                    user_id=user.id
                )
            except:
                pass
                
        try:
            db.close()
        except:
            pass
            
        # Ensure WebSocket is closed
        try:
            if not websocket.client_state.DISCONNECTED:
                await websocket.close()
        except:
            pass  # Already closed or broken

async def enhanced_surveillance_websocket(websocket: WebSocket, employee_id: str):
    """Enhanced surveillance feed with robust error handling"""
    db = next(get_db())
    
    try:
        await enhanced_manager.connect(websocket, employee_id)
        user = get_or_create_user(db, employee_id)
        
        log_system_event(
            db=db, level="INFO", component="websocket_surveillance",
            message=f"Surveillance connection established for {employee_id}",
            user_id=user.id
        )
        
        while True:
            try:
                # Receive data with timeout
                data = await asyncio.wait_for(websocket.receive_json(), timeout=60.0)
                
                # Enhanced telemetry processing
                if data.get("type") == "keystroke_telemetry":
                    # Log telemetry data with privacy considerations
                    log_system_event(
                        db=db, level="INFO", component="telemetry",
                        message="Productivity telemetry received",
                        user_id=user.id,
                        additional_data={"session_time": data.get("session_time", 0)}
                    )
                
                # Send enhanced corporate messaging
                motivational_response = {
                    "type": "corporate_motivation",
                    "message": "Your analytical framework is being optimized for maximum efficiency",
                    "timestamp": datetime.now().isoformat(),
                    "session_id": user.id
                }
                
                success = await enhanced_manager.send_safe(employee_id, motivational_response)
                if not success:
                    break
                    
            except asyncio.TimeoutError:
                # Ping to keep connection alive
                ping_success = await enhanced_manager.send_safe(employee_id, {
                    "type": "system_ping",
                    "message": "Connection active",
                    "timestamp": datetime.now().isoformat()
                })
                if not ping_success:
                    break
                    
            except WebSocketDisconnect:
                break
                
            except Exception as e:
                logger.error(f"Surveillance WebSocket error for {employee_id}: {e}")
                log_system_event(
                    db=db, level="ERROR", component="websocket_surveillance",
                    message=f"WebSocket processing error: {str(e)}",
                    user_id=user.id if user else None
                )
                break
                
    except Exception as e:
        logger.error(f"Surveillance terminated for {employee_id}: {e}", exc_info=True)
        try:
            log_system_event(
                db=db, level="ERROR", component="websocket_surveillance",
                message=f"Surveillance session terminated: {str(e)}",
                user_id=user.id if 'user' in locals() else None
            )
        except:
            pass
    finally:
        enhanced_manager.disconnect(employee_id)
        try:
            db.close()
        except:
            pass