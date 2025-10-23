###################################################
# Help Menu System using Decorator Design Pattern #
###################################################

"""
This module implements a dynamic help menu system that automatically
updates based on available operations using the Decorator pattern.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from app.operations import OperationFactory, Operation


class HelpComponent(ABC):
    """
    Abstract base class for help menu components.
    Defines the interface for generating help text.
    """
    
    @abstractmethod
    def get_help_text(self) -> str:
        """
        Generate help text for this component.
        
        Returns:
            str: Formatted help text
        """
        pass


class BaseHelpMenu(HelpComponent):
    """
    Base help menu with core information.
    This is the component that decorators will wrap.
    """
    
    def get_help_text(self) -> str:
        """
        Generate base help menu text.
        
        Returns:
            str: Base help menu
        """
        return """
╔════════════════════════════════════════════════════════════════╗
║              ADVANCED CALCULATOR - HELP MENU                   ║
╔════════════════════════════════════════════════════════════════╗

BASIC USAGE:
  Enter command: <operation>
  First number: <operand1>
  Second number: <operand2>
  
GENERAL COMMANDS:
  help          - Display this help menu
  history       - Show calculation history
  clear         - Clear calculation history
  undo          - Undo last operation
  redo          - Redo previously undone operation
  save          - Save calculation history
  load          - Load calculation history
  exit/quit     - Exit the calculator
"""


class HelpMenuDecorator(HelpComponent):
    """
    Base decorator class for help menu components.
    Wraps a HelpComponent and delegates to it.
    """
    
    def __init__(self, component: HelpComponent):
        """
        Initialize decorator with a component to wrap.
        
        Args:
            component: The HelpComponent to decorate
        """
        self._component = component
    
    def get_help_text(self) -> str:
        """
        Delegate to the wrapped component.
        
        Returns:
            str: Help text from wrapped component
        """
        return self._component.get_help_text()


class OperationsHelpDecorator(HelpMenuDecorator):
    """
    Decorator that adds available operations to the help menu.
    Dynamically generates operation list from OperationFactory.
    """
    
    def __init__(self, component: HelpComponent, operation_descriptions: Dict[str, str] = None):
        """
        Initialize with component and optional operation descriptions.
        
        Args:
            component: The HelpComponent to decorate
            operation_descriptions: Optional dict mapping operation names to descriptions
        """
        super().__init__(component)
        self._operation_descriptions = operation_descriptions or self._get_default_descriptions()
    
    def _get_default_descriptions(self) -> Dict[str, str]:
        """
        Get default descriptions for standard operations.
        
        Returns:
            Dict mapping operation names to descriptions
        """
        return {
            'add': 'Add two numbers (a + b)',
            'subtract': 'Subtract two numbers (a - b)',
            'multiply': 'Multiply two numbers (a × b)',
            'divide': 'Divide two numbers (a ÷ b)',
            'power': 'Raise a to the power of b (a^b)',
            'root': 'Calculate the b-th root of a (a^(1/b))',
            'modulus': 'Calculate remainder of a divided by b (a mod b)',
            'int_divide': 'Integer division (floor division) (a // b)',
            'percent': 'Calculate what percentage a is of b ((a/b) × 100)',
            'abs_diff': 'Calculate absolute difference between a and b (|a - b|)',
        }
    
    def get_help_text(self) -> str:
        """
        Generate help text with available operations added.
        
        Returns:
            str: Help text including operations section
        """
        base_text = self._component.get_help_text()
        operations_text = self._generate_operations_section()
        return base_text + operations_text
    
    def _generate_operations_section(self) -> str:
        """
        Dynamically generate the operations section from OperationFactory.
        
        Returns:
            str: Formatted operations section
        """
        # Get all available operations from the factory
        available_operations = OperationFactory._operations
        
        operations_text = "\nAVAILABLE OPERATIONS:\n"
        operations_text += "=" * 64 + "\n"
        
        # Sort operations alphabetically for consistent display
        for op_name in sorted(available_operations.keys()):
            # Get description from provided dict or use operation name
            description = self._operation_descriptions.get(
                op_name, 
                f"Perform {op_name} operation"
            )
            
            # Format the operation entry with padding
            operations_text += f"  {op_name:<15} - {description}\n"
        
        operations_text += "\n"
        return operations_text


class ExamplesHelpDecorator(HelpMenuDecorator):
    """
    Decorator that adds usage examples to the help menu.
    """
    
    def __init__(self, component: HelpComponent, examples: List[str] = None):
        """
        Initialize with component and optional custom examples.
        
        Args:
            component: The HelpComponent to decorate
            examples: Optional list of example commands
        """
        super().__init__(component)
        self._examples = examples or self._get_default_examples()
    
    def _get_default_examples(self) -> List[str]:
        """
        Get default usage examples.
        
        Returns:
            List of example command strings
        """
        return [
            "add 5 3           → Result: 8",
            "subtract 10 4     → Result: 6",
            "multiply 7 6      → Result: 42",
            "divide 15 3       → Result: 5",
            "power 2 8         → Result: 256",
            "root 27 3         → Result: 3 (cube root)",
            "modulus 17 5      → Result: 2",
            "int_divide 17 5   → Result: 3",
            "percent 50 200    → Result: 25 (50 is 25% of 200)",
            "abs_diff -5 3     → Result: 8",
        ]
    
    def get_help_text(self) -> str:
        """
        Generate help text with examples added.
        
        Returns:
            str: Help text including examples section
        """
        base_text = self._component.get_help_text()
        examples_text = self._generate_examples_section()
        return base_text + examples_text
    
    def _generate_examples_section(self) -> str:
        """
        Generate the examples section.
        
        Returns:
            str: Formatted examples section
        """
        examples_text = "USAGE EXAMPLES:\n"
        examples_text += "=" * 64 + "\n"
        
        for example in self._examples:
            examples_text += f"  {example}\n"
        
        examples_text += "\n"
        return examples_text


class NotesHelpDecorator(HelpMenuDecorator):
    """
    Decorator that adds notes and tips to the help menu.
    """
    
    def __init__(self, component: HelpComponent, notes: List[str] = None):
        """
        Initialize with component and optional custom notes.
        
        Args:
            component: The HelpComponent to decorate
            notes: Optional list of note strings
        """
        super().__init__(component)
        self._notes = notes or self._get_default_notes()
    
    def _get_default_notes(self) -> List[str]:
        """
        Get default notes and tips.
        
        Returns:
            List of note strings
        """
        return [
            "• Decimal numbers are supported (e.g., 3.14, 2.5)",
            "• Negative numbers must be entered carefully",
            "• Division by zero will result in an error",
            "• History is automatically saved between sessions",
            "• Use 'undo' to revert mistakes",
            "• Type 'exit' to close the calculator",
        ]
    
    def get_help_text(self) -> str:
        """
        Generate help text with notes added.
        
        Returns:
            str: Help text including notes section
        """
        base_text = self._component.get_help_text()
        notes_text = self._generate_notes_section()
        footer = self._generate_footer()
        return base_text + notes_text + footer
    
    def _generate_notes_section(self) -> str:
        """
        Generate the notes section.
        
        Returns:
            str: Formatted notes section
        """
        notes_text = "NOTES & TIPS:\n"
        notes_text += "=" * 64 + "\n"
        
        for note in self._notes:
            notes_text += f"  {note}\n"
        
        notes_text += "\n"
        return notes_text
    
    def _generate_footer(self) -> str:
        """
        Generate footer for help menu.
        
        Returns:
            str: Formatted footer
        """
        return "╚════════════════════════════════════════════════════════════════╝\n"


class HelpMenuBuilder:
    """
    Builder class for constructing help menus with decorators.
    Provides a fluent interface for building customized help menus.
    """
    
    def __init__(self):
        """Initialize builder with base help menu."""
        self._component = BaseHelpMenu()
    
    def with_operations(self, operation_descriptions: Dict[str, str] = None) -> 'HelpMenuBuilder':
        """
        Add operations section to help menu.
        
        Args:
            operation_descriptions: Optional custom operation descriptions
            
        Returns:
            Self for method chaining
        """
        self._component = OperationsHelpDecorator(self._component, operation_descriptions)
        return self
    
    def with_examples(self, examples: List[str] = None) -> 'HelpMenuBuilder':
        """
        Add examples section to help menu.
        
        Args:
            examples: Optional custom examples
            
        Returns:
            Self for method chaining
        """
        self._component = ExamplesHelpDecorator(self._component, examples)
        return self
    
    def with_notes(self, notes: List[str] = None) -> 'HelpMenuBuilder':
        """
        Add notes section to help menu.
        
        Args:
            notes: Optional custom notes
            
        Returns:
            Self for method chaining
        """
        self._component = NotesHelpDecorator(self._component, notes)
        return self
    
    def build(self) -> HelpComponent:
        """
        Build and return the final help menu component.
        
        Returns:
            Complete HelpComponent with all decorators applied
        """
        return self._component


def create_default_help_menu() -> HelpComponent:
    """
    Factory function to create a fully-featured default help menu.
    
    Returns:
        HelpComponent with all standard decorators applied
    """
    return (HelpMenuBuilder()
            .with_operations()
            .with_examples()
            .with_notes()
            .build())


def display_help():
    """
    Display the complete help menu.
    This is the main function to call from your calculator application.
    """
    help_menu = create_default_help_menu()
    print(help_menu.get_help_text())


