########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver
from app.logger import LoggingObserver
from app.operations import OperationFactory
from app.help_menu import display_help  # Import the dynamic help menu


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    Uses a dynamic help menu that automatically updates with new operations.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display dynamically generated help menu using Decorator pattern
                    # The help menu automatically includes all operations registered
                    # in the OperationFactory without manual updates
                    display_help()
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print("History cleared")
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print("Operation undone")
                    else:
                        print("Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print("Operation redone")
                    else:
                        print("Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                # Check if the command is a valid operation from the OperationFactory
                # This dynamically supports all registered operations
                try:
                    operation = OperationFactory.create_operation(command)
                    
                    # Perform the specified arithmetic operation
                    print("\nEnter numbers (or 'cancel' to abort):")
                    a = input("First number: ")
                    if a.lower() == 'cancel':
                        print("Operation cancelled")
                        continue
                    b = input("Second number: ")
                    if b.lower() == 'cancel':
                        print("Operation cancelled")
                        continue

                    # Set the operation and perform calculation
                    calc.set_operation(operation)
                    result = calc.perform_operation(a, b)

                    # Normalize the result if it's a Decimal
                    if isinstance(result, Decimal):
                        result = result.normalize()

                    print(f"\nResult: {result}")
                    
                except ValueError:
                    # Command is not a valid operation
                    print(f"Unknown command: '{command}'. Type 'help' for available commands.")
                except (ValidationError, OperationError) as e:
                    # Handle known exceptions related to validation or operation errors
                    print(f"Error: {e}")
                except Exception as e:
                    # Handle any unexpected exceptions
                    print(f"Unexpected error: {e}")
                continue

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print("\nOperation cancelled")
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print("\nInput terminated. Exiting...")
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(f"Error: {e}")
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise