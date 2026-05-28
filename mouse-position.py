#! python3
import pyautogui, time, argparse

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
try:
    if args.start_after is not None:
        remaining_delay = args.start_after * 60
        while remaining_delay > 0:
            print(f'Starting in {format_duration(remaining_delay)}...')
            sleep_interval = min(2, remaining_delay)
            time.sleep(sleep_interval)
            remaining_delay -= sleep_interval

    end_time = time.time() + duration if duration is not None else None

    # Snapshot where the pointer is right now — no initial move to center
    base_x, base_y = pyautogui.position()
    last_placed_x, last_placed_y = base_x, base_y
    print(f'Starting at ({base_x}, {base_y}).')

    print('Mouse is moving.')
    while end_time is None or time.time() < end_time:
        origin_x, origin_y = base_x, base_y

        # Move 1 pixel right, then return to exact origin
        print(f'Nudging from ({origin_x}, {origin_y}).')
        pyautogui.moveTo(origin_x + 1, origin_y, 0.1)
        pyautogui.moveTo(origin_x, origin_y, 0.1)
        last_placed_x, last_placed_y = origin_x, origin_y

        next_move_time = time.time() + 120
        while time.time() < next_move_time:
            if end_time is not None:
                print(f'Script will stop in {format_duration(end_time - time.time())}.')
            sleep_until = next_move_time if end_time is None else min(next_move_time, end_time)
            sleep_interval = sleep_until - time.time()
            if sleep_interval <= 0:
                break
            time.sleep(min(2, sleep_interval))

            # If the pointer moved more than 1px from where we left it, the user moved it
            current_x, current_y = pyautogui.position()
            if abs(current_x - last_placed_x) > 1 or abs(current_y - last_placed_y) > 1:
                base_x, base_y = current_x, current_y
                last_placed_x, last_placed_y = current_x, current_y
                print(f'User moved mouse to ({base_x}, {base_y}). Next nudge in 2 minutes.')
                next_move_time = time.time() + 120

except KeyboardInterrupt:
    print('\n')
