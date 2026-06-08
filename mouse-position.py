#! python3
import pyautogui, time, argparse, subprocess, sys, random

IDLE_THRESHOLD = 180  # seconds of no movement before script acts

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


duration = args.stop_after * 60 if args.stop_after is not None else None

print('Press Ctrl-C to quit.')
if args.start_after is not None:
    print(f'Will start after {format_duration(args.start_after * 60)}.')
if args.stop_after is not None:
    print(f'Will stop after {format_duration(args.stop_after * 60)}.')

# caffeinate -d keeps the display awake for as long as this script runs (macOS only)
caffeinate = None
if sys.platform == 'darwin':
    caffeinate = subprocess.Popen(['caffeinate', '-d'])
    print('Display sleep prevention active (caffeinate -d).')

try:
    if args.start_after is not None:
        remaining_delay = args.start_after * 60
        while remaining_delay > 0:
            print(f'Starting in {format_duration(remaining_delay)}...')
            sleep_interval = min(2, remaining_delay)
            time.sleep(sleep_interval)
            remaining_delay -= sleep_interval

    end_time = time.time() + duration if duration is not None else None

    last_x, last_y = pyautogui.position()
    last_activity_time = time.time()
    last_log_time = 0  # force an immediate countdown print on first tick
    print(f'Watching from ({last_x}, {last_y}). Will move after {IDLE_THRESHOLD // 60} minutes of inactivity.')

    while end_time is None or time.time() < end_time:
        time.sleep(2)

        if end_time is not None:
            print(f'Script will stop in {format_duration(end_time - time.time())}.')

        current_x, current_y = pyautogui.position()

        # User moved the mouse — reset the idle clock
        if abs(current_x - last_x) > 1 or abs(current_y - last_y) > 1:
            last_x, last_y = current_x, current_y
            last_activity_time = time.time()
            last_log_time = 0  # force countdown print on next tick after reset
            next_move_at = time.strftime('%H:%M:%S', time.localtime(last_activity_time + IDLE_THRESHOLD))
            print(f'User moved mouse to ({last_x}, {last_y}). Idle timer reset. Next move at {next_move_at}.')
            continue

        idle_seconds = time.time() - last_activity_time
        remaining_seconds = max(0, IDLE_THRESHOLD - idle_seconds)

        # Print countdown every 30 seconds
        if time.time() - last_log_time >= 30:
            next_move_at = time.strftime('%H:%M:%S', time.localtime(last_activity_time + IDLE_THRESHOLD))
            print(f'Next mouse move in {format_duration(remaining_seconds)} (at {next_move_at}).')
            last_log_time = time.time()

        if idle_seconds >= IDLE_THRESHOLD:
            origin_x, origin_y = pyautogui.position()
            rand_x = random.randint(100, 500)
            rand_y = random.randint(100, 500)
            print(f'Idle for {format_duration(idle_seconds)}. Moving to ({rand_x}, {rand_y}) then returning.')
            pyautogui.moveTo(rand_x, rand_y, 0.5)
            pyautogui.moveTo(origin_x, origin_y, 0.5)
            last_x, last_y = origin_x, origin_y
            last_activity_time = time.time()
            last_log_time = 0  # force countdown print on next tick after move

except KeyboardInterrupt:
    print('\n')
finally:
    if caffeinate is not None:
        caffeinate.terminate()
