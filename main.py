"""Entry point for the GUI/Console app."""

from automation.app import App as GUIApp
# from automation.engine import Engine as ConsoleApp

app = GUIApp()
app.run()
