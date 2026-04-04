# Agent.md - mv-me Project Guide

**Project Name:** mv-me
**Language:** Python 3
**Purpose:** A utility script that automatically moves the mouse cursor to random positions to keep the screen active and prevent sleep/lock situations.

---

## Project Overview

This is a simple, standalone Python script that:
- Moves the mouse pointer to random positions on screen
- Runs continuously or for a limited duration
- Can delay the start before beginning movement
- Displays progress/status messages with formatted time durations

**Use Cases:**
- Prevent computer from going to sleep during long-running processes
- Keep screen active during presentations or demonstrations
- Avoid lock screen timeouts

---

## Project Structure

```
mv-me/
├── mouse-position.py      # Main script (executable)
├── start.sh               # Bash wrapper to run the script
├── README.md              # User documentation
├── agent.md               # This file - for AI model development
├── .venv/                 # Python virtual environment (local only)
├── .git/                  # Git repository
└── .gitignore             # Git ignore rules
```

---

## Dependencies

- **Python 3.x** - Required version
- **pyautogui** - Package for mouse control and automation

**Installation:**
```bash
python3 -m venv ./.venv
source ./.venv/bin/activate
python3 -m pip install pyautogui
```

---

## Code Structure

### Main File: `mouse-position.py`

#### Command-Line Arguments
- `--stop-after MINUTES` - Stop the script after N minutes (optional)
- `--start-after MINUTES` - Wait N minutes before starting (optional)
- Both arguments can be combined

#### Key Functions

**`format_duration(total_seconds)`** (lines 13-21)
- Converts seconds to human-readable format
- Returns: `"Xh Ym Zs"`, `"Xm Ys"`, or `"Xs"` depending on magnitude
- Used for all time display messages

#### Main Logic Flow

1. **Parse arguments** (lines 5-10)
2. **Initial messages** (lines 26-30)
   - Shows if --start-after and/or --stop-after are provided
   - Uses `format_duration()` for readable time display
3. **Start delay** (lines 32-38)
   - If `--start-after` specified, displays countdown every 2 seconds
   - Uses `format_duration()` for the countdown display
4. **Movement loop** (lines 41-66)
   - Generates random coordinates between (100, 500)
   - Moves mouse to that position over 1 second
   - Waits 10 seconds between moves
   - Displays remaining stop time every 2 seconds (if --stop-after used)
5. **Graceful shutdown** (lines 68-69)
   - Catches Ctrl-C and exits cleanly

---

## Recent Changes

### Time Display Formatting
All time-based messages now use the `format_duration()` function for consistent, human-readable output:
- "Will start after 2h 5m 30s."
- "Starting in 1h 30m 45s..."
- "Script will stop in 3h 15m 22s."
- "Will stop after 1h 0m 0s."

This improves UX by showing time in a more intuitive format instead of raw seconds or minutes.

---

## Development Guidelines

### When Adding Features

1. **Time Display** - Always use `format_duration()` for any time-based messages
2. **Argument Parsing** - Use `argparse` for new command-line options
3. **User Feedback** - Print status messages to keep the user informed
4. **Error Handling** - Use try-except blocks for clean exit handling

### Code Style

- Simple, procedural approach preferred
- Avoid unnecessary abstractions for one-off operations
- Keep functions focused and readable
- Comments only needed for non-obvious logic

### Testing Recommendations

When making changes:
1. Test with `--start-after 1 --stop-after 1` for quick validation
2. Verify format_duration works correctly for various time values
3. Test Ctrl-C interrupt handling
4. Verify messages are printed at expected intervals

### Common Tasks

**Adding a new option:**
```python
parser.add_argument('--new-option', type=int, default=None, help='description')
```

**Adding time-based message:**
```python
print(f'Message: {format_duration(seconds)}.')
```

**Modifying movement behavior:**
- Random coordinates range: lines 43-44
- Movement duration: line 46 (currently 1 second)
- Wait between moves: line 58 (currently 10 seconds)
- Status update frequency: line 36 and 66 (currently 2 seconds)

---

## Running the Script

### Basic Usage
```bash
python3 mouse-position.py
```

### With Options
```bash
# Run for 30 minutes
python3 mouse-position.py --stop-after 30

# Wait 5 minutes, then run forever
python3 mouse-position.py --start-after 5

# Wait 5 minutes, then run for 30 minutes
python3 mouse-position.py --start-after 5 --stop-after 30
```

### Using Wrapper
```bash
./start.sh  # Runs without any options (forever)
```

---

## Important Notes

- The script runs indefinitely unless `--stop-after` is specified
- Screen coordinates are hardcoded (100-500 range) - modify in lines 43-44 if needed
- Movement happens over 1 second to appear smooth
- Status updates occur every 2 seconds (adjustable in loop logic)
- Ctrl-C always stops the script gracefully
