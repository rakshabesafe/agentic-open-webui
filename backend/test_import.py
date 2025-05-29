import sys
import os

# Add the backend directory to sys.path to allow direct import of open_webui
# Assuming the script is in /app/backend/test_import.py
# and we want to add /app/ to sys.path to import open_webui as a top-level package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


print("Attempting to import agents_router...")
try:
    from open_webui.routers.agents import router as agents_router
    print("Successfully imported agents_router!")
except ImportError as e:
    print(f"Failed to import agents_router: {e}")
except Exception as e:
    print(f"An unexpected error occurred during agents_router import: {e}")

print("\nAttempting to import typer...")
try:
    import typer
    print("Successfully imported typer!")
except ImportError as e:
    print(f"Failed to import typer: {e}")
except Exception as e:
    print(f"An unexpected error occurred during typer import: {e}")
