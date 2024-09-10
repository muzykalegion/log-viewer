import argparse
import ast
import datetime

import matplotlib.dates
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import MultiCursor


def isOldFile(filename):
    return '15.05.24' in filename


def parse_log(filename='LOGS/27.05.24/1.out'):
    time_array = []
    alt_array = []
    throttle_array = []
    pitch_array = []
    day = datetime.date(2024, 5, 15)
    ZERO_ALT = 'ALT:  0.0' if isOldFile(filename) else 'ALT: 0.0'
    TIMESTAMP_FORMAT = '%HH:%MM:%SS' if isOldFile(filename) else '%H:%M:%S.%f'
    config_line = ''

    with open(filename, 'r+', errors='ignore', encoding='utf-8') as file:
        for num, line in enumerate(file):
            if line.startswith('Delay='):
                config_line = line
            if ZERO_ALT in line:
                break
        for line in file:
            # print(line.rstrip())
            if 'ALT:' in line and 'Navigation' not in line:
                alt_idx = line.find('ALT:')
                time_str = line[:alt_idx].strip()
                if time_str.startswith('ation'):
                    continue
                alt_str = line[alt_idx:].replace('ALT:', '').strip()
                time = datetime.datetime.strptime(time_str, TIMESTAMP_FORMAT).time()
                time = datetime.datetime.combine(day, time)
                alt = float(alt_str)
                time_array.append(time)
                alt_array.append(alt)
                if isOldFile(filename):
                    nextLine = next(file)
                else:
                    try:
                        for i in range(7):
                            nextLine = next(file)
                    except StopIteration:
                        time_array.pop()
                        alt_array.pop()
                        break
                if nextLine.startswith('['):
                    try:
                        chs = ast.literal_eval(nextLine)
                    except SyntaxError:
                        print(f'!!! {num} !!!')
                    throttle_array.append(chs[2])
                    pitch_array.append(chs[1])
                else:
                    time_array.pop()
                    alt_array.pop()

    print(time_array)
    print(alt_array)
    print(throttle_array)
    print(pitch_array)
    return time_array, alt_array, throttle_array, pitch_array, config_line
    # lines = [line.rstrip() for line in file]
    # print(lines)
    # for line in lines:


def curve(length):
    TAKEOFF_LIST = np.zeros(10)  # Creating the take off curve
    for t in range(len(TAKEOFF_LIST)):
        TAKEOFF_LIST[t] = (1 - (1 / np.exp(t)))  # act like a cap-charge shape
    return TAKEOFF_LIST.tolist()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='Relative path fo a file, e.g. LOGS/27.05.24/1.log')
    args = parser.parse_args()
    log_name = '2024-09-10--15-57-49'
    filepath = args.filepath if args.filepath else f'LOGS/board/{log_name}.log'
    times, alts, throttles, pitches, cfg_line = parse_log(filepath)

    number_of_plots = 2
    fig, ax = plt.subplots(number_of_plots, 1, sharex=True)
    mtimes = mdates.date2num(times)

    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 12,
            }

    ax[0].plot(mtimes, throttles, '-g')
    ax[0].legend(['Throttle'])
    ax[0].set_ylim(988, 2012)
    ax[0].set_ylim(988, 1700)
    ax[0].text(0.1, 1.2, cfg_line, fontsize=14, transform=ax[0].transAxes, va='top')

    ax[1].plot(mtimes, alts, ':b')
    ax[1].legend(['Altitude'])
    ax[1].set_ylim(-0.5, 20)

    # ax[2].plot(mtimes, pitches, ':c')
    # ax[2].legend(['Pitch'])

    sec_loc = mdates.SecondLocator(interval=1)
    sec_formatter = mdates.DateFormatter('%H:%M:%S.%f')

    ax[0].xaxis.set_major_locator(sec_loc)
    ax[0].xaxis.set_major_formatter(sec_formatter)
    ax[1].xaxis.set_major_locator(sec_loc)
    ax[1].xaxis.set_major_formatter(sec_formatter)
    # ax[2].xaxis.set_major_locator(sec_loc)
    # ax[2].xaxis.set_major_formatter(sec_formatter)
    plt.gcf().autofmt_xdate(rotation=90)

    multi = MultiCursor(fig.canvas, (ax[0], ax[1]), color='r', lw=0.5, horizOn=True, vertOn=True)
    # plt.text(cfg_line,  fontdict=font)
    plt.show()
