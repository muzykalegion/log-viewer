import argparse
import ast
import datetime

import matplotlib.dates
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


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

    with open(filename, 'r+') as file:
        for line in file:
            if ZERO_ALT in line:
                break
        for line in file:
            # print(line.rstrip())
            if 'ALT:' in line:
                alt_idx = line.find('ALT:')
                time_str = line[:alt_idx].strip()
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
                        for i in range(6):
                            nextLine = next(file)
                    except StopIteration:
                        time_array.pop()
                        alt_array.pop()
                        break
                chs = ast.literal_eval(nextLine) if nextLine.startswith('[') else [0, 0, 988]
                throttle_array.append(chs[2])
                pitch_array.append(chs[1])

    print(time_array)
    print(alt_array)
    print(throttle_array)
    print(pitch_array)
    return time_array, alt_array, throttle_array, pitch_array
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

    filepath = args.filepath if args.filepath else 'LOGS/15.05.24/flight10.log'
    times, alts, throttles, pitches = parse_log(filepath)

    fig, ax = plt.subplots(3, 1)
    mtimes = mdates.date2num(times)

    ax[0].plot(mtimes, throttles, '-g')
    ax[0].legend(['Throttle'])
    ax[0].set_ylim(988, 2012)

    ax[1].plot(mtimes, alts, ':b')
    ax[1].legend(['Altitude'])
    ax[1].set_ylim(-2, 25)

    ax[2].plot(mtimes, pitches, ':c')
    ax[2].legend(['Pitch'])

    sec_loc = matplotlib.dates.SecondLocator(interval=5)
    sec_formatter = mdates.DateFormatter('%H:%M:%S.%f')

    ax[0].xaxis.set_major_locator(sec_loc)
    ax[0].xaxis.set_major_formatter(sec_formatter)
    ax[1].xaxis.set_major_locator(sec_loc)
    ax[1].xaxis.set_major_formatter(sec_formatter)
    ax[2].xaxis.set_major_locator(sec_loc)
    ax[2].xaxis.set_major_formatter(sec_formatter)
    plt.gcf().autofmt_xdate(rotation=90)
    plt.title(filepath, x=0.1, y=3.5)
    plt.show()
