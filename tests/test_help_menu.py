"""
Tests for the dynamic help menu system using Decorator pattern.
"""

import pytest
from decimal import Decimal
from app.help_menu import (
    BaseHelpMenu,
    HelpMenuBuilder,
    OperationsHelpDecorator,
    ExamplesHelpDecorator,
    NotesHelpDecorator,
    create_default_help_menu
)
from app.operations import Operation, OperationFactory


class TestBaseHelpMenu:
    """Test the base help menu component."""
    
    def test_base_help_menu_contains_basic_info(self):
        """Test that base menu contains essential information."""
        menu = BaseHelpMenu()
        help_text = menu.get_help_text()
        
        assert "ADVANCED CALCULATOR" in help_text
        assert "BASIC USAGE" in help_text
        assert "GENERAL COMMANDS" in help_text
        assert "help" in help_text
        assert "exit" in help_text


class TestOperationsHelpDecorator:
    """Test the operations decorator."""
    
    def test_operations_decorator_adds_operations(self):
        """Test that decorator adds operations section."""
        base = BaseHelpMenu()
        decorated = OperationsHelpDecorator(base)
        help_text = decorated.get_help_text()
        
        assert "AVAILABLE OPERATIONS" in help_text
        assert "add" in help_text.lower()
        assert "subtract" in help_text.lower()
    
    def test_operations_decorator_includes_all_factory_operations(self):
        """Test that all registered operations appear in help."""
        base = BaseHelpMenu()
        decorated = OperationsHelpDecorator(base)
        help_text = decorated.get_help_text()
        
        # Check that standard operations are present
        for op_name in ['add', 'subtract', 'multiply', 'divide', 'power', 'root']:
            assert op_name in help_text.lower()
    
    def test_operations_decorator_uses_custom_descriptions(self):
        """Test that custom descriptions can be provided."""
        base = BaseHelpMenu()
        custom_descriptions = {
            'add': 'Custom addition description',
            'subtract': 'Custom subtraction description'
        }
        decorated = OperationsHelpDecorator(base, custom_descriptions)
        help_text = decorated.get_help_text()
        
        assert "Custom addition description" in help_text
        assert "Custom subtraction description" in help_text
    
    def test_dynamic_update_with_new_operation(self):
        """Test that help menu automatically updates when new operation is registered."""
        # Define a new custom operation
        class Square(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a * a
        
        # Register the new operation
        OperationFactory.register_operation('square', Square)
        
        # Create help menu - should automatically include new operation
        base = BaseHelpMenu()
        decorated = OperationsHelpDecorator(base)
        help_text = decorated.get_help_text()
        
        assert 'square' in help_text.lower()
        
        # Clean up - unregister the operation
        if 'square' in OperationFactory._operations:
            del OperationFactory._operations['square']


class TestExamplesHelpDecorator:
    """Test the examples decorator."""
    
    def test_examples_decorator_adds_examples(self):
        """Test that decorator adds examples section."""
        base = BaseHelpMenu()
        decorated = ExamplesHelpDecorator(base)
        help_text = decorated.get_help_text()
        
        assert "USAGE EXAMPLES" in help_text
        assert "add 5 3" in help_text
    
    def test_examples_decorator_uses_custom_examples(self):
        """Test that custom examples can be provided."""
        base = BaseHelpMenu()
        custom_examples = ["custom example 1", "custom example 2"]
        decorated = ExamplesHelpDecorator(base, custom_examples)
        help_text = decorated.get_help_text()
        
        assert "custom example 1" in help_text
        assert "custom example 2" in help_text


class TestNotesHelpDecorator:
    """Test the notes decorator."""
    
    def test_notes_decorator_adds_notes(self):
        """Test that decorator adds notes section."""
        base = BaseHelpMenu()
        decorated = NotesHelpDecorator(base)
        help_text = decorated.get_help_text()
        
        assert "NOTES & TIPS" in help_text
        assert "Decimal numbers are supported" in help_text
    
    def test_notes_decorator_uses_custom_notes(self):
        """Test that custom notes can be provided."""
        base = BaseHelpMenu()
        custom_notes = ["Custom note 1", "Custom note 2"]
        decorated = NotesHelpDecorator(base, custom_notes)
        help_text = decorated.get_help_text()
        
        assert "Custom note 1" in help_text
        assert "Custom note 2" in help_text


class TestHelpMenuBuilder:
    """Test the builder class."""
    
    def test_builder_with_operations(self):
        """Test builder with operations."""
        help_menu = HelpMenuBuilder().with_operations().build()
        help_text = help_menu.get_help_text()
        
        assert "AVAILABLE OPERATIONS" in help_text
        assert "add" in help_text.lower()
    
    def test_builder_with_examples(self):
        """Test builder with examples."""
        help_menu = HelpMenuBuilder().with_examples().build()
        help_text = help_menu.get_help_text()
        
        assert "USAGE EXAMPLES" in help_text
    
    def test_builder_with_notes(self):
        """Test builder with notes."""
        help_menu = HelpMenuBuilder().with_notes().build()
        help_text = help_menu.get_help_text()
        
        assert "NOTES & TIPS" in help_text
    
    def test_builder_with_all_decorators(self):
        """Test builder with all decorators applied."""
        help_menu = (HelpMenuBuilder()
                    .with_operations()
                    .with_examples()
                    .with_notes()
                    .build())
        help_text = help_menu.get_help_text()
        
        assert "AVAILABLE OPERATIONS" in help_text
        assert "USAGE EXAMPLES" in help_text
        assert "NOTES & TIPS" in help_text
    
    def test_builder_chaining(self):
        """Test that builder methods can be chained."""
        builder = HelpMenuBuilder()
        result = builder.with_operations().with_examples().with_notes()
        
        assert isinstance(result, HelpMenuBuilder)


class TestDefaultHelpMenu:
    """Test the default help menu factory function."""
    
    def test_create_default_help_menu(self):
        """Test that default help menu includes all sections."""
        help_menu = create_default_help_menu()
        help_text = help_menu.get_help_text()
        
        # Check for all expected sections
        assert "ADVANCED CALCULATOR" in help_text
        assert "BASIC USAGE" in help_text
        assert "GENERAL COMMANDS" in help_text
        assert "AVAILABLE OPERATIONS" in help_text
        assert "USAGE EXAMPLES" in help_text
        assert "NOTES & TIPS" in help_text


class TestDecoratorPattern:
    """Test that the Decorator pattern is properly implemented."""
    
    def test_multiple_decorators_can_be_stacked(self):
        """Test that multiple decorators can wrap the same component."""
        base = BaseHelpMenu()
        
        # Stack decorators
        with_ops = OperationsHelpDecorator(base)
        with_examples = ExamplesHelpDecorator(with_ops)
        with_notes = NotesHelpDecorator(with_examples)
        
        help_text = with_notes.get_help_text()
        
        # All sections should be present
        assert "AVAILABLE OPERATIONS" in help_text
        assert "USAGE EXAMPLES" in help_text
        assert "NOTES & TIPS" in help_text
    
    def test_decorator_order_affects_output(self):
        """Test that decorator order matters."""
        base = BaseHelpMenu()
        
        # Different order
        order1 = NotesHelpDecorator(ExamplesHelpDecorator(OperationsHelpDecorator(base)))
        order2 = OperationsHelpDecorator(ExamplesHelpDecorator(NotesHelpDecorator(base)))
        
        text1 = order1.get_help_text()
        text2 = order2.get_help_text()
        
        # Both should have all content but in different order
        assert text1 != text2
        assert "AVAILABLE OPERATIONS" in text1
        assert "AVAILABLE OPERATIONS" in text2


class TestDynamicBehavior:
    """Test that help menu updates dynamically."""
    
    def test_help_menu_reflects_runtime_operation_additions(self):
        """Test that adding operations at runtime updates the help menu."""
        # Create initial help menu
        initial_menu = create_default_help_menu()
        initial_text = initial_menu.get_help_text()
        
        # Define and register a new operation
        class Cube(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a ** 3
        
        OperationFactory.register_operation('cube', Cube)
        
        # Create new help menu - should include new operation
        updated_menu = create_default_help_menu()
        updated_text = updated_menu.get_help_text()
        
        assert 'cube' in updated_text.lower()
        
        # Clean up
        if 'cube' in OperationFactory._operations:
            del OperationFactory._operations['cube']
    
    def test_no_manual_updates_needed(self):
        """Test that no manual updates are needed when operations change."""
        # This test demonstrates that the help menu queries the factory
        # dynamically rather than storing a static list
        
        # Get current operation count
        help_menu = create_default_help_menu()
        text1 = help_menu.get_help_text()
        operation_count_1 = text1.count('Perform') + text1.count('Calculate')
        
        # Register new operation
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a
        
        OperationFactory.register_operation('testop', TestOp)
        
        # Create new help menu
        new_menu = create_default_help_menu()
        text2 = new_menu.get_help_text()
        
        # New operation should appear
        assert 'testop' in text2.lower()
        
        # Clean up
        if 'testop' in OperationFactory._operations:
            del OperationFactory._operations['testop']
