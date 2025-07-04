# Dark Heresy Character Sheet Manager

This is a simple offline-only GUI application for creating, viewing and editing Dark Heresy (1st Edition) character sheets.

## Quick start (development)

```bash
# (Optional) create a virtual environment
python3 -m venv venv && source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --break-system-packages

# Run the application
python main.py
```

Character data is stored in a human-readable INI‐style ``.txt`` file. Use *File → Save* or *File → Open* in the GUI.

## Packaging a standalone binary

```
pip install pyinstaller --break-system-packages
pyinstaller --onefile main.py
```

The resulting executable can be found in the ``dist/`` directory.

## Roadmap / TODO

* Add the remaining character sheet sections (wounds, equipment, talents, psychic powers …)
* Track unsaved changes
* Validation and better UX (drop-downs for homeworlds etc.)
* Dark/Light theme toggle

Pull requests are welcome!
