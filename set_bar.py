# I've already done this with bash. Will be redoing it in python because of:
# - Familiarity in the language
# - Easier to change code
# - Faster than rust to compile

from os import system as run

def output(command):
    # There's probably a better way of doing this
    # I don't know about it, and I don't really care
    run(command+"> a")
    f = open('a')
    t = f.read()
    f.close()
    run('rm a')
    return t;

def time():
    from time import strftime, gmtime
    t = strftime("%Y-%m-%d %H:%M", gmtime())
    return t

def battery():
    BATTERY_FOLDER = '/sys/class/power_supply/BAT0/'
    # check battery level
    f = open(BATTERY_FOLDER+'capacity')
    level = int(f.read())
    f.close()
    # check if battery is charging
    f = open(BATTERY_FOLDER+'status')
    charging = (f.read()[:-1] == 'Charging')
    f.close()
    # add symbols
    if charging: 
        symbol = '󰂄'
    elif level < 90:
        symbol = chr(983162 + (level//10))
    else:
        symbol = '󰁹'
    return f'{level}% {symbol}'

def network_info():
    # check network name
    network = output('nmcli')
    try:
        name = network.split('\n')[0].split('connected to ')[1]
    except:
        return ""
    # check network type
    n = name.lower()
    net_type = []
    if '5.8' in n:
        net_type.append('5.8 GHz')
    elif '2.4' in n:
        net_type.append('2.4 GHz')
    if 'xt' in n:
        net_type.append('ext')
    net_type = ' '.join(net_type)
    # ping domain
    DOMAIN = "1.1.1.1"
    ping_str = output(f'ping -c 1 -W 0.5 {DOMAIN}')
    try:
        ping = ping_str.split('mdev = ')[1].split('.')[0]
        ping_str = ping+'ms '
    except:
        return '󱛅 '+f"({net_type})" if net_type else ''
    
    return f'{net_type} {ping_str} '


def set_bar():
    DATETIME = time()
    BATTERY = battery()
    NETWORK = network_info()
    layout = [NETWORK, DATETIME, BATTERY]
    layout = map(lambda x: x if x else '', layout)
    STRING = '|'.join(layout)
    run(f'xsetroot -name "{STRING}"')

def main():
    from time import sleep
    while True:
        set_bar()
        sleep(25)

if __name__ == "__main__":
    main()
