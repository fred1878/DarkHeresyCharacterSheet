# Dark Heresy Character Sheet Manager - Complete Features Summary

This application is a comprehensive offline GUI tool for creating, viewing, and editing character sheets for the Dark Heresy tabletop RPG (1st Edition).

## Core Application Framework

**Technology Stack:**
- Built using Python 3 with PySide6 (Qt6 GUI framework)
- Modular architecture with separate files for models, storage, and main application
- Data persistence using human-readable INI-style `.txt` files
- Dark/grimdark themed UI with custom styling

**Main Application Features:**
- Tabbed interface for organized character data entry
- File menu with New, Open, Save, Save As, and Exit options
- Automatic prompting to save changes when switching files
- Standalone executable creation support via PyInstaller

## Character Sheet Components

### 1. Basic Information Tab
**Personal Details:**
- Name, Gender, Age, Height, Weight, Build
- Physical appearance: Hair color, Eye color, Aura description
- Background information: Homeworld, Background, Role, Divination

### 2. Attributes Tab
**Core Characteristics:**
- All nine Dark Heresy primary attributes:
  - WS (Weapon Skill)
  - BS (Ballistic Skill) 
  - S (Strength)
  - T (Toughness)
  - Ag (Agility)
  - Int (Intelligence)
  - Per (Perception)
  - WP (Willpower)
  - Fel (Fellowship)
- Numeric input with 0-100 range for each attribute

### 3. Skills Tab
**Comprehensive Skill System:**
- **38 predefined Dark Heresy skills** including:
  - Combat skills: Acrobatics, Dodge, Parry
  - Social skills: Barter, Charm, Command, Deceive, Intimidate
  - Knowledge skills: Common Lore, Forbidden Lore, Scholastic Lore
  - Technical skills: Medicae, Tech-Use, Security, Operate
  - Survival skills: Awareness, Survival, Tracking, Navigate
  - Stealth skills: Concealment, Silent Move, Disguise
  - And many more specialized skills

**Skill Management:**
- Training status (trained/untrained checkbox)
- Skill ranks/advancement levels (0-5 range)
- Scrollable interface for easy navigation

### 4. Wounds & Movement Tab
**Health Tracking:**
- Current Wounds, Maximum Wounds, Fatigue levels
- All values range from 0-100

**Movement Speeds:**
- Half movement, Full movement, Charge movement, Run movement
- All movement values range from 0-99

### 5. Experience Tab
**Character Progression:**
- Total Experience Points earned
- Spent Experience Points 
- Automatic calculation of Remaining Experience Points
- Support for values up to 100,000 XP
- Real-time remaining XP calculation when values change

### 6. Talents Tab
**Character Abilities:**
- Dynamic list management for character talents
- Add new talents via text input dialog
- Remove selected talents
- Unlimited talent entries

### 7. Gear Tab
**Equipment Management:**
- Dynamic list for general equipment and possessions
- Add/remove functionality
- Text-based equipment descriptions
- Unlimited gear entries

### 8. Weapons Tab
**Advanced Combat Equipment:**
- **Comprehensive weapon editor dialog** with full weapon statistics:
  - Weapon Name
  - Type (Melee/Ranged dropdown)
  - Class (Basic/Pistol/Heavy/Thrown/Melee dropdown)
  - Range specification
  - Rate of Fire (RoF)
  - Damage description
  - Armor Penetration (0-100 numeric)
  - Clip size
  - Reload time
  - Special qualities (free text)

**Weapon Management:**
- Add new weapons via detailed editor
- Edit existing weapons (double-click or Edit button)
- Remove weapons
- Structured data format with pipe-separated storage
- Full weapon statline preservation

### 9. Armour Tab
**Protection System:**
- Armor Points (AP) for four body locations:
  - Head AP (0-20 range)
  - Arms AP (0-20 range) 
  - Body AP (0-20 range)
  - Legs AP (0-20 range)

### 10. Psyker Tab
**Psychic Powers Management:**
- Psy Rating (0-10 range)
- Psychic Powers list management
- Add/remove individual powers
- Simple power name storage system

### 11. Status Tab
**Character Condition Tracking:**
- **Corruption Points** (0-100 range)
- **Insanity Points** (0-100 range)
- **Mutations list** - dynamic add/remove functionality
- **Mental Disorders list** - dynamic add/remove functionality

## Data Persistence Features

**File Format:**
- Human-readable INI-style `.txt` format
- Cross-platform file compatibility
- Easy manual editing if needed
- UTF-8 encoding support

**File Operations:**
- Create new character sheets
- Open existing character files
- Save current character
- Save As with new filename
- Automatic directory creation for save paths

## User Interface Features

**Visual Design:**
- **Dark/grimdark theme** appropriate for Warhammer 40K setting
- Custom color scheme with dark backgrounds and gold accents
- Organized tabbed interface for easy navigation
- Responsive layout with proper widget sizing

**Usability:**
- Intuitive form-based data entry
- Scrollable areas for long lists (skills, equipment)
- Modal dialogs for complex data entry (weapons)
- Confirmation dialogs for save operations
- Input validation (weapon name requirement)

## Technical Architecture

**Modular Design:**
- `main.py` - GUI components and application logic (711 lines)
- `models.py` - Data structures and character model (443 lines)
- `storage.py` - File I/O operations (37 lines)
- Clean separation of concerns

**Data Models:**
- Comprehensive dataclass-based character representation
- Type safety with proper data validation
- Conversion methods for file persistence
- Default skill lists and character templates

## Planned Features (Roadmap)
- Change tracking for unsaved modifications
- Input validation and better UX (dropdown menus for homeworlds)
- Dark/Light theme toggle
- Additional character sheet sections as needed

## Development & Distribution
- Virtual environment support
- Simple dependency management (only requires PySide6>=6.6)
- Standalone executable creation via PyInstaller
- Cross-platform compatibility (Python/Qt based)

This application provides a complete, offline solution for managing Dark Heresy character sheets with a professional, game-appropriate interface and comprehensive data management capabilities.