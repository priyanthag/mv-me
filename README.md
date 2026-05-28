# mv-me

A script that moves the mouse cursor randomly to keep the screen active.

## Requirements

- Python 3
- `pyautogui` package

### Install dependencies

Create a virtual environment, activate it, then install all dependencies from `requirements.txt`:

```bash
python3 -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Run forever

```bash
./start.sh
```

or directly:

```bash
python3 mouse-position.py
```

### Run for a limited time

Pass `--stop-after` with the number of minutes:

```bash
python3 mouse-position.py --stop-after 30
```

This will stop the mouse movement after 30 minutes.

When `--stop-after` is used, the script also prints a countdown every 2 seconds after movement starts.

### Delay the start

Pass `--start-after` with the number of minutes to wait before the mouse starts moving:

```bash
python3 mouse-position.py --start-after 5
```

This will wait 5 minutes before starting to move the mouse, then run forever. During that delay, the script prints a countdown every 2 seconds.

### Combine both options

```bash
python3 mouse-position.py --start-after 5 --stop-after 30
```

This will wait 5 minutes, then move the mouse for 30 minutes before stopping.

During the run, it prints the remaining stop time every 2 seconds.

### Stop manually

Press `Ctrl-C` at any time to quit.
