import os

# Must be set before PyQt5 creates a QApplication so Qt tests can run
# headless (no X server) in CI / this sandbox.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
