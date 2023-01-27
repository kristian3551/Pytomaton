"""Entry point for the GUI app."""

from src.app.app import App as GUIApp

if __name__ == "__main__":
    app = GUIApp()
    app.run()
