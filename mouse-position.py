#! python3
import pyautogui, time, argparse
import random

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
    print('Mouse is moving.')
    while end_time is None or time.time() < end_time:

        random_X = random.randint(100, 500)
        random_Y = random.randint(100, 500)
        print(f'Mouse is moving to ({random_X}, {random_Y}).')
        pyautogui.moveTo(random_X, random_Y, 1)
        # pyautogui.click(random_X, random_Y)
        # pyautogui.press('enter')

        # pyautogui.moveTo(1900, -1000, 1)
        # pyautogui.click(1900, -1000)
        # pyautogui.press('enter')

        # time.sleep(2)
        # pyautogui.moveTo(1900, -600, 1)
        # pyautogui.click(1900, -600)
        # pyautogui.press('enter')
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