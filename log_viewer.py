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
    baro_array = []
    alt_array = []
    throttle_array = []
    pitch_array = []
    day = datetime.date(2024, 5, 15)
    ZERO_ALT = 'ALT:  0.0' if isOldFile(filename) else 'ALT: 0.0'
    TIMESTAMP_FORMAT = '%HH:%MM:%SS' if isOldFile(filename) else '%H:%M:%S.%f'
    config_line = ''

    with open(filename, 'r+', errors='ignore') as file:
        for line in file:
            if line.startswith('Delay='):
                config_line = line
            if ZERO_ALT in line:
                break
        for line in file:
            # print(line.rstrip())
            if 'GROUND_ALT:' in line:
                gr_alt_idx = line.find('GROUND_ALT:')
                time_str = line[:gr_alt_idx].strip()
                time = datetime.datetime.strptime(time_str, TIMESTAMP_FORMAT).time()
                alt_str = line[gr_alt_idx:].replace('GROUND_ALT: ', '').strip()
                gr_alt_str = alt_str[:5]
                baro_alt_idx = alt_str.find('BARO_ALT: ')
                fc_alt_idx = alt_str.find('FC_ALT: ')
                tm_alt_idx = alt_str.find('TEMP: ')
                baro_alt_str = alt_str[baro_alt_idx+10:fc_alt_idx-2]
                fc_alt_str = alt_str[fc_alt_idx+8:tm_alt_idx-2]
                baro_alt = float(baro_alt_str) - float(gr_alt_str)
                time = datetime.datetime.combine(day, time)
                fc_alt = float(fc_alt_str)
                time_array.append(time)
                baro_array.append(baro_alt)
                alt_array.append(fc_alt)
                if isOldFile(filename) or True:
                    nextLine = next(file)
                else:
                    try:
                        for i in range(6):
                            nextLine = next(file)
                    except StopIteration:
                        time_array.pop()
                        alt_array.pop()
                        baro_array.pop()
                        break
                if nextLine.startswith('['):
                    chs = ast.literal_eval(nextLine)
                    throttle_array.append(chs[2])
                    pitch_array.append(chs[1])
                else:
                    time_array.pop()
                    alt_array.pop()
                    baro_array.pop()

    print(time_array)
    print(baro_array)
    print(alt_array)
    print(throttle_array)
    print(pitch_array)
    return time_array, baro_array, alt_array, throttle_array, pitch_array, config_line
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
    log_name = '2024-09-04--17-48-46'
    filepath = args.filepath if args.filepath else f'LOGS/board/{log_name}.log'
    times, baro, alts, throttles, pitches, cfg_line = parse_log(filepath)

    number_of_plots = 2
    fig, ax = plt.subplots(number_of_plots, 1, sharex=True)
    mtimes = mdates.date2num(times)

    ax[0].plot(mtimes, throttles, '-g')
    ax[0].legend(['Throttle'])
    ax[0].set_ylim(988, 2012)
    ax[0].set_ylim(988, 1700)

    ax[1].plot(mtimes, alts, ':b')
    ax[1].plot(mtimes, baro, '-r')
    ax[1].legend(['Altitude', 'Baro'])
    ax[1].set_ylim(-0.5, 30)

    # ax[2].plot(mtimes, pitches, ':c')
    # ax[2].legend(['Pitch'])

    sec_loc = matplotlib.dates.SecondLocator(interval=1)
    sec_formatter = mdates.DateFormatter('%H:%M:%S.%f')

    ax[0].xaxis.set_major_locator(sec_loc)
    ax[0].xaxis.set_major_formatter(sec_formatter)
    ax[1].xaxis.set_major_locator(sec_loc)
    ax[1].xaxis.set_major_formatter(sec_formatter)
    # ax[2].xaxis.set_major_locator(sec_loc)
    # ax[2].xaxis.set_major_formatter(sec_formatter)
    plt.gcf().autofmt_xdate(rotation=90)
    plt.text(x=10, y=10, s=cfg_line, fontsize=12)
    plt.show()
