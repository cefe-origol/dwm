from os import system as run
from set_bar import *
from sys import argv

def change_volume(x):
    if(x > 0):
        run(f'pamixer --increase {x}')
    else:
        run(f'pamixer --decrease {-x}')
    a = output('pamixer --get-volume')
    run(f'xsetroot -name "󰕾 {a}"')



def main():
    change_volume(int(argv[1]))

if __name__ == "__main__":
    main()
