#! python3
import pyautogui, time, argparse
import random

try:
    from screeninfo import get_monitors
    HAS_SCREENINFO = True
except ImportError:
    HAS_SCREENINFO = False

parser = argparse.ArgumentParser()
parser.add_argument('--stop-after', type=int, default=None, metavar='MINUTES',
                    help='Stop after this many minutes (default: run forever)')
parser.add_argument('--start-after', type=int, default=None, metavar='MINUTES',
                    help='Start moving mouse after this many minutes (default: start immediately)')
args = parser.parse_args()


def format_duration(total_seconds):
    total_seconds = max(0, int(total_seconds))
    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f'{hours}h {minutes}m {seconds}s'
    if minutes > 0:
        return f'{minutes}m {seconds}s'
    return f'{seconds}s'


def get_active_monitor_center():
    """Return (cx, cy) for the monitor that currently contains the mouse pointer."""
    mx, my = pyautogui.position()

    if HAS_SCREENINFO:
        for m in get_monitors():
            if m.x <= mx < m.x + m.width and m.y <= my < m.y + m.height:
                return m.x + m.width // 2, m.y + m.height // 2
        # Fallback: first monitor
        m = get_monitors()[0]
        return m.x + m.width // 2, m.y + m.height // 2

    # No screeninfo — use pyautogui's primary screen size
    w, h = pyautogui.size()
    return w // 2, h // 2


duration = args.stop_after * 60 if args.stop_after is not None else None

print('Press Ctrl-C to quit.')
if args.start_after is not None:
    print(f'Will start after {format_duration(args.start_after * 60)}.')
if args.stop_after is not None:
    print(f'Will stop after {format_duration(args.stop_after * 60)}.')
try:
    if args.start_after is not None:
        remaining_delay = args.start_after * 60
        while remaining_delay > 0:
            print(f'Starting in {format_duration(remaining_delay)}...')
            sleep_interval = min(2, remaining_delay)
            time.sleep(sleep_interval)
            remaining_delay -= sleep_interval

    end_time = time.time() + duration if duration is not None else None

    # Move to the center of the active monitor once before the loop starts
    cx, cy = get_active_monitor_center()
    print(f'Moving to center of active monitor ({cx}, {cy}).')
    pyautogui.moveTo(cx, cy, 1)

    print('Mouse is moving.')
    while end_time is None or time.time() < end_time:
        cx, cy = get_active_monitor_center()
        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)
        target_x = cx + offset_x
        target_y = cy + offset_y
        print(f'Mouse is moving to ({target_x}, {target_y}).')
        pyautogui.moveTo(target_x, target_y, 1)

        next_move_time = time.time() + 10
        while time.time() < next_move_time:
            if end_time is not None:
                print(f'Script will stop in {format_duration(end_time - time.time())}.')
            sleep_until = next_move_time if end_time is None else min(next_move_time, end_time)
            sleep_interval = sleep_until - time.time()
            if sleep_interval <= 0:
                break
            time.sleep(min(2, sleep_interval))

except KeyboardInterrupt:
    print('\n')
