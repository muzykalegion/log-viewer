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
    accel_array = []
    day = datetime.date(2024, 5, 15)
    ZERO_ALT = 'ALT:  0.0' if isOldFile(filename) else 'ALT: 0.0'
    TIMESTAMP_FORMAT = '%HH:%MM:%SS' if isOldFile(filename) else '%H:%M:%S.%f'
    config_line = ''

    with open(filename, 'r+', errors='ignore', encoding='utf-8') as file:
        # nnum = 0
        for num, line in enumerate(file):
            # nnum = num
            if line.startswith('Delay='):
                config_line = line
            if ZERO_ALT in line:
                break

        for num, line in enumerate(file):
            # print(line.rstrip())
            # print(nnum + num)
            if 'Navigation got ALT:' in line:
                alt_idx = line.find('Navigation got ALT:')
                time_str = line[:alt_idx].strip()
                alt_str = line[alt_idx:].replace('Navigation got ALT:', '').strip()
                time = datetime.datetime.strptime(time_str, TIMESTAMP_FORMAT).time()
                time = datetime.datetime.combine(day, time)
                alt = float(alt_str)
                time_array.append(time)
                alt_array.append(alt)
                nextLine = next(file)
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
                while 'ACC:' not in nextLine:
                    nextLine = next(file)
                acc_idx = nextLine.find('ACC:')
                acc_str = nextLine[acc_idx:].replace('ACC:', '').strip()
                acc = ast.literal_eval(acc_str)
                accel_array.append(float(acc[2] / 512))  # z axis

    print(len(time_array), time_array)
    print(len(alt_array),alt_array)
    print(len(throttle_array),throttle_array)
    print(len(pitch_array), pitch_array)
    print(len(accel_array),accel_array)
    return time_array, alt_array, throttle_array, pitch_array, accel_array, config_line


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='Relative path fo a file, e.g. LOGS/27.05.24/1.log')
    args = parser.parse_args()
    log_name = '2024-10-10--21-49-18'
    filepath = args.filepath if args.filepath else f'LOGS/board/{log_name}.log'
    times, alts, throttles, pitches, acc_zs, cfg_line = parse_log(filepath)

    number_of_plots = 2
    fig, ax = plt.subplots(number_of_plots, 1, sharex=True)
    mtimes = mdates.date2num(times)

    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 12,
            }

    ax[0].scatter(mtimes, throttles, s=1, c='green')
    ax[0].legend(['Throttle'])
    ax[0].set_ylim(988, 2012)
    ax[0].text(0.1, 1.2, cfg_line, fontsize=14, transform=ax[0].transAxes, va='top')

    ax[1].scatter(mtimes, alts, s=1, c='blue')
    ax[1].scatter(mtimes, acc_zs, s=1, c='brown')
    ax[1].legend(['Altitude', 'Accelerometer'])
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
