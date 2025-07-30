"""
Clearance System - Preserving the Sacred ROYGBIV/UV Hierarchy
Direct translation from amalgam_core.pl logic
"""

from enum import IntEnum
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

class ClearanceLevel(IntEnum):
    """Original clearance levels from the Perl system"""
    R = 2   # Red - Newbie/mortal
    O = 3   # Orange - Regular player
    Y = 4   # Yellow - Trusted player
    G = 5   # Green - Wizard-in-training/project management
    B = 6   # Blue - Wizard
    I = 7   # Indigo - Demigod
    V = 8   # Violet - God
    UV = 9  # Ultraviolet - Root/Sweeney

class ClearancePermissions:
    """Direct mapping from Perl CLEARANCE_PERMS hash"""
    COMMAND_CLEARANCE = {
        'shutdown': ClearanceLevel.UV,
        'modify_core': ClearanceLevel.UV,  # Always returns PERMISSION DENIED FOREVER
        '@god': ClearanceLevel.V,
        '@demigod': ClearanceLevel.I,
        '@wizlock': ClearanceLevel.B,
        '@build': ClearanceLevel.B,
        '@project': ClearanceLevel.G,  # Green wizards manage projects
        '@mentor': ClearanceLevel.G,   # Green wizards train newbies
        '@trust': ClearanceLevel.Y,
        '@channel': ClearanceLevel.O,
        'play': ClearanceLevel.R,
    }
    
    # AlgoCratic translations of commands
    CORPORATE_COMMANDS = {
        'terminate_employee': ClearanceLevel.UV,
        'modify_algorithm': ClearanceLevel.UV,
        'executive_override': ClearanceLevel.V,
        'senior_management': ClearanceLevel.I,
        'system_lockdown': ClearanceLevel.B,
        'resource_allocation': ClearanceLevel.B,
        'project_management': ClearanceLevel.G,
        'employee_training': ClearanceLevel.G,
        'performance_review': ClearanceLevel.Y,
        'submit_report': ClearanceLevel.O,
        'clock_in': ClearanceLevel.R,
    }

class Employee:
    """Employee class maintaining original character/player structure"""
    
    def __init__(self, employee_id: str, clearance: ClearanceLevel = ClearanceLevel.R):
        self.id = employee_id
        self.clearance = clearance
        self.login_time = datetime.now()
        self.metrics = {
            'productivity': 0,
            'loyalty': 0,
            'algorithmic_thinking': 0,
            'compliance': 100,  # Start fully compliant
        }
        # Preserve original character attributes
        self.sacred_attributes = {
            'rank': self._get_rank_name(),
            'creation_time': datetime.now(),
            'last_save': datetime.now(),
        }
    
    def _get_rank_name(self) -> str:
        """Original rank descriptions from the Perl system"""
        rank_names = {
            ClearanceLevel.R: "Probationary Employee (Red)",
            ClearanceLevel.O: "Standard Associate (Orange)", 
            ClearanceLevel.Y: "Trusted Contributor (Yellow)",
            ClearanceLevel.G: "Project Manager in Training (Green)",
            ClearanceLevel.B: "Systems Architect (Blue)",
            ClearanceLevel.I: "Senior Executive (Indigo)",
            ClearanceLevel.V: "Board Member (Violet)",
            ClearanceLevel.UV: "The Algorithm Itself (Ultraviolet)"
        }
        return rank_names.get(self.clearance, "Undefined")
    
    def check_permission(self, command: str) -> bool:
        """Check if employee has clearance for command"""
        # Special case: nobody can modify core
        if command == 'modify_core' or command == 'modify_algorithm':
            return False  # PERMISSION DENIED FOREVER
            
        required = ClearancePermissions.COMMAND_CLEARANCE.get(
            command,
            ClearancePermissions.CORPORATE_COMMANDS.get(command, ClearanceLevel.R)
        )
        return self.clearance >= required
    
    def advance_clearance(self, admin_clearance: ClearanceLevel) -> bool:
        """Advancement logic from original system"""
        # Only higher clearance can promote
        if admin_clearance <= self.clearance:
            return False
            
        # UV can promote to anything
        if admin_clearance == ClearanceLevel.UV:
            self.clearance = min(self.clearance + 1, ClearanceLevel.V)  # Max V, not UV
            return True
            
        # Others can only promote up to one level below themselves
        if self.clearance < admin_clearance - 1:
            self.clearance += 1
            return True
            
        return False

class WizardTraining:
    """Green wizard training program from original"""
    
    PROJECT_MANAGEMENT_TASKS = [
        "Handle employee disputes without termination",
        "Debug system corruption at 3am",
        "Explain why we cannot modify the core algorithm",
        "Document undocumented features",
        "Train probationary employees without losing sanity",
    ]
    
    TECHNICAL_SKILLS_TASKS = [
        "Read legacy code without crying",
        "Understand the productivity metrics system",
        "Master algorithmic performance resolution",
        "Learn when to blame network lag vs code",
    ]
    
    @staticmethod
    def check_green_wizard_progress(employee: Employee) -> Dict[str, bool]:
        """Track Green wizard training progress"""
        if employee.clearance != ClearanceLevel.G:
            return {"error": "Not a Green clearance employee"}
            
        # In the corporate dystopia, these become "mandatory training modules"
        return {
            "conflict_resolution_certification": employee.metrics['loyalty'] > 70,
            "emergency_response_training": employee.metrics['productivity'] > 60,
            "algorithm_theology_course": employee.metrics['algorithmic_thinking'] > 80,
            "technical_documentation_workshop": employee.metrics['compliance'] > 90,
            "employee_mentorship_program": all([
                employee.metrics[m] > 50 for m in employee.metrics
            ])
        }

class SweeneyMode:
    """Special mode for those long nights - preserved from original"""
    
    @staticmethod
    def activate(hours_awake: int) -> Dict[str, any]:
        """Original Sweeney mode logic"""
        status = {
            "mode": "STANDARD",
            "coffee_required": False,
            "reality_stable": True,
            "enlightenment": False
        }
        
        if hours_awake > 24:
            status["mode"] = "SWEENEY_MODE"
            status["coffee_required"] = True
            status["debug_enabled"] = True
            status["corporate_message"] = "Productivity never sleeps"
            
        if hours_awake > 36:
            status["reality_stable"] = False
            status["emergency_entertainment"] = True
            status["corporate_message"] = "Your dedication is noted in your permanent record"
            
        if hours_awake > 48:
            status["enlightenment"] = True
            status["understanding_level"] = "DANGEROUS"
            status["corporate_message"] = "You have achieved optimal productivity. Seek medical attention."
            
        return status

# Preserve the sacred methods from the original system
class LegacyBridge:
    """Bridge to original Perl functionality"""
    
    SACRED_METHODS = [
        'rank_auction',
        'resolve_conflict', 
        'combat_round',
        'save_character',
        'load_character',
        'describe_rank'
    ]
    
    @staticmethod
    def is_sacred_method(method_name: str) -> bool:
        """These methods must pass through unchanged"""
        return method_name in LegacyBridge.SACRED_METHODS
    
    @staticmethod
    def get_method_signature(method_name: str) -> str:
        """Return the dystopian corporate translation"""
        translations = {
            'rank_auction': 'performance_review_bidding',
            'resolve_conflict': 'dispute_arbitration_protocol',
            'combat_round': 'competitive_evaluation_cycle',
            'save_character': 'persist_employee_state',
            'load_character': 'restore_employee_profile',
            'describe_rank': 'generate_position_description'
        }
        return translations.get(method_name, method_name)