"""
Comprehensive testing for calculator_repl module.

This test suite covers the functionality of the calculator REPL,
including command handling, arithmetic operations, exception handling,
and initialization processes.
"""

import pytest
from unittest.mock import patch, MagicMock, call
from decimal import Decimal
import logging

from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError


class TestCalculatorREPLBasicCommands:
    """Test basic REPL commands."""

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_exit_command(self, mock_calculator_class, mock_print, mock_input):
        """Test that 'exit' command exits the REPL."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.save_history.assert_called_once()
        assert any('Goodbye!' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['help', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.display_help')
    @patch('app.calculator_repl.Calculator')
    def test_help_command(self, mock_calculator_class, mock_display_help, mock_print, mock_input):
        """Test that 'help' command displays help menu."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_display_help.assert_called_once()

    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_history_command_empty(self, mock_calculator_class, mock_print, mock_input):
        """Test 'history' command with empty history."""
        mock_calc = MagicMock()
        mock_calc.show_history.return_value = []
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.show_history.assert_called_once()
        assert any('No calculations in history' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['history', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_history_command_with_entries(self, mock_calculator_class, mock_print, mock_input):
        """Test 'history' command with history entries."""
        mock_calc = MagicMock()
        mock_calc.show_history.return_value = [
            'Addition(5, 3) = 8',
            'Subtraction(10, 4) = 6'
        ]
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.show_history.assert_called_once()
        # Check that history entries are printed
        print_calls_str = str(mock_print.call_args_list)
        assert 'Calculation History' in print_calls_str

    @patch('builtins.input', side_effect=['clear', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_clear_command(self, mock_calculator_class, mock_print, mock_input):
        """Test 'clear' command clears history."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.clear_history.assert_called_once()
        assert any('History cleared' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['undo', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_undo_command_success(self, mock_calculator_class, mock_print, mock_input):
        """Test 'undo' command when undo is successful."""
        mock_calc = MagicMock()
        mock_calc.undo.return_value = True
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.undo.assert_called_once()
        assert any('Operation undone' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['undo', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_undo_command_nothing_to_undo(self, mock_calculator_class, mock_print, mock_input):
        """Test 'undo' command when nothing to undo."""
        mock_calc = MagicMock()
        mock_calc.undo.return_value = False
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.undo.assert_called_once()
        assert any('Nothing to undo' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['redo', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_redo_command_success(self, mock_calculator_class, mock_print, mock_input):
        """Test 'redo' command when redo is successful."""
        mock_calc = MagicMock()
        mock_calc.redo.return_value = True
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.redo.assert_called_once()
        assert any('Operation redone' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['redo', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_redo_command_nothing_to_redo(self, mock_calculator_class, mock_print, mock_input):
        """Test 'redo' command when nothing to redo."""
        mock_calc = MagicMock()
        mock_calc.redo.return_value = False
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.redo.assert_called_once()
        assert any('Nothing to redo' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['save', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_save_command_success(self, mock_calculator_class, mock_print, mock_input):
        """Test 'save' command saves history successfully."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        # save_history is called twice: once from 'save' command, once from 'exit'
        assert mock_calc.save_history.call_count == 2
        assert any('History saved successfully' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['save', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_save_command_error(self, mock_calculator_class, mock_print, mock_input):
        """Test 'save' command when save fails."""
        mock_calc = MagicMock()
        mock_calc.save_history.side_effect = [Exception("Save failed"), None]
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        assert any('Error saving history' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['load', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_load_command_success(self, mock_calculator_class, mock_print, mock_input):
        """Test 'load' command loads history successfully."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.load_history.assert_called()
        assert any('History loaded successfully' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['load', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_load_command_error(self, mock_calculator_class, mock_print, mock_input):
        """Test 'load' command when load fails."""
        mock_calc = MagicMock()
        mock_calc.load_history.side_effect = Exception("Load failed")
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        assert any('Error loading history' in str(call) for call in mock_print.call_args_list)


class TestCalculatorREPLOperations:
    """Test arithmetic operations through the REPL."""

    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_valid_operation_add(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test performing a valid addition operation."""
        mock_calc = MagicMock()
        mock_calc.perform_operation.return_value = Decimal('8')
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        mock_factory.create_operation.assert_called_with('add')
        mock_calc.set_operation.assert_called_with(mock_operation)
        mock_calc.perform_operation.assert_called_with('5', '3')
        assert any('Result: 8' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['multiply', '6', '7', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_valid_operation_multiply(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test performing a valid multiplication operation."""
        mock_calc = MagicMock()
        mock_calc.perform_operation.return_value = Decimal('42')
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        mock_factory.create_operation.assert_called_with('multiply')
        assert any('Result: 42' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_operation_cancelled_first_number(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test cancelling operation at first number input."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        mock_calc.perform_operation.assert_not_called()
        assert any('Operation cancelled' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['add', '5', 'cancel', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_operation_cancelled_second_number(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test cancelling operation at second number input."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        mock_calc.perform_operation.assert_not_called()
        assert any('Operation cancelled' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['invalid_op', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_invalid_operation_command(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test handling of invalid operation command."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        mock_factory.create_operation.side_effect = ValueError("Unknown operation")
        
        calculator_repl()
        
        assert any("Unknown command: 'invalid_op'" in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['divide', '10', '0', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_operation_validation_error(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test handling of ValidationError during operation."""
        mock_calc = MagicMock()
        mock_calc.perform_operation.side_effect = ValidationError("Division by zero")
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        assert any('Error: Division by zero' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_operation_error(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test handling of OperationError during operation."""
        mock_calc = MagicMock()
        mock_calc.perform_operation.side_effect = OperationError("Operation failed")
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        assert any('Error: Operation failed' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_unexpected_error_during_operation(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test handling of unexpected errors during operation."""
        mock_calc = MagicMock()
        mock_calc.perform_operation.side_effect = RuntimeError("Unexpected error")
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        calculator_repl()
        
        assert any('Unexpected error' in str(call) for call in mock_print.call_args_list)


class TestCalculatorREPLExceptionHandling:
    """Test exception handling in the REPL."""

    @patch('builtins.input', side_effect=KeyboardInterrupt())
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_keyboard_interrupt_during_input(self, mock_calculator_class, mock_print, mock_input):
        """Test handling of KeyboardInterrupt (Ctrl+C)."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        # Need to add 'exit' after KeyboardInterrupt to end the loop
        mock_input.side_effect = [KeyboardInterrupt(), 'exit']
        
        calculator_repl()
        
        assert any('Operation cancelled' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=EOFError())
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_eof_error_during_input(self, mock_calculator_class, mock_print, mock_input):
        """Test handling of EOFError (Ctrl+D)."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        assert any('Input terminated' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['add', '5', '3', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.OperationFactory')
    @patch('app.calculator_repl.Calculator')
    def test_generic_exception_during_loop(self, mock_calculator_class, mock_factory, mock_print, mock_input):
        """Test handling of generic exceptions during the loop."""
        mock_calc = MagicMock()
        mock_calc.perform_operation.side_effect = [Exception("Random error"), None]
        mock_calculator_class.return_value = mock_calc
        
        mock_operation = MagicMock()
        mock_factory.create_operation.return_value = mock_operation
        
        # Should continue after error
        calculator_repl()
        
        assert any('Unexpected error' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_fatal_error_during_initialization(self, mock_calculator_class, mock_print):
        """Test handling of fatal error during calculator initialization."""
        mock_calculator_class.side_effect = Exception("Fatal initialization error")
        
        with pytest.raises(Exception, match="Fatal initialization error"):
            calculator_repl()
        
        assert any('Fatal error' in str(call) for call in mock_print.call_args_list)


class TestCalculatorREPLExitHandling:
    """Test exit command variations and save on exit."""

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_exit_saves_history_successfully(self, mock_calculator_class, mock_print, mock_input):
        """Test that exiting saves history successfully."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        mock_calc.save_history.assert_called_once()
        assert any('History saved successfully' in str(call) for call in mock_print.call_args_list)
        assert any('Goodbye!' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_exit_warning_on_save_failure(self, mock_calculator_class, mock_print, mock_input):
        """Test that exit shows warning when save fails."""
        mock_calc = MagicMock()
        mock_calc.save_history.side_effect = Exception("Cannot save")
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        assert any('Could not save history' in str(call) for call in mock_print.call_args_list)
        assert any('Goodbye!' in str(call) for call in mock_print.call_args_list)


class TestCalculatorREPLInitialization:
    """Test calculator initialization and observer registration."""

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.AutoSaveObserver')
    @patch('app.calculator_repl.LoggingObserver')
    @patch('app.calculator_repl.Calculator')
    def test_observers_registered(self, mock_calculator_class, mock_logging_obs, 
                                   mock_autosave_obs, mock_print, mock_input):
        """Test that observers are registered on initialization."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        # Verify observers were added
        assert mock_calc.add_observer.call_count == 2

    @patch('builtins.input', side_effect=['exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_startup_message_displayed(self, mock_calculator_class, mock_print, mock_input):
        """Test that startup message is displayed."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        assert any("Calculator started" in str(call) for call in mock_print.call_args_list)


class TestCalculatorREPLEmptyInput:
    """Test handling of empty input."""

    @patch('builtins.input', side_effect=['', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_empty_input_ignored(self, mock_calculator_class, mock_print, mock_input):
        """Test that empty input is ignored and REPL continues."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        # Should just continue to next input
        assert any('Goodbye!' in str(call) for call in mock_print.call_args_list)


class TestCalculatorREPLWhitespace:
    """Test handling of whitespace in input."""

    @patch('builtins.input', side_effect=['  exit  '])
    @patch('builtins.print')
    @patch('app.calculator_repl.Calculator')
    def test_whitespace_stripped(self, mock_calculator_class, mock_print, mock_input):
        """Test that whitespace is stripped from input."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        # Should recognize 'exit' even with surrounding whitespace
        assert any('Goodbye!' in str(call) for call in mock_print.call_args_list)

    @patch('builtins.input', side_effect=['  HELP  ', 'exit'])
    @patch('builtins.print')
    @patch('app.calculator_repl.display_help')
    @patch('app.calculator_repl.Calculator')
    def test_case_insensitive_commands(self, mock_calculator_class, mock_display_help, 
                                        mock_print, mock_input):
        """Test that commands are case-insensitive."""
        mock_calc = MagicMock()
        mock_calculator_class.return_value = mock_calc
        
        calculator_repl()
        
        # Should recognize 'HELP' as 'help'
        mock_display_help.assert_called_once()
