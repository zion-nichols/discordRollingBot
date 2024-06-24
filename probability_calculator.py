from roll_commands import roll
from probability_class import probability_distribution as pd

SAMPLE_SIZE = 1000000

def main():
    while True:
        msg = input('Input pool then difficulty (x-y z-w): ')
        if msg.lower() == 'q':
            print(msg.lower())
            exit()
        pool_range, dif_range = msg.split()
        range_finder(pool_range, dif_range)

def range_finder(pool_range, dif_range):
    st_pool, sp_pool = pool_range.split('-')
    st_dif, sp_dif = dif_range.split('-')

    for x in range(int(st_pool), int(sp_pool)+1):
        for y in range(int(st_dif), int(sp_dif)+1):
            print(f'Pool {x} Difficulty {y} || {roll_count(x, y)}')

def roll_count(pool, difficulty, size=SAMPLE_SIZE):
    counted_sux = 0
    counted_fails = 0
    x = 0
    while x < size:
        z, sux = roll(pool, difficulty, False)
        if sux > 0:
            counted_sux += 1
        else:
            counted_fails += 1
        x += 1
    dist = pd(counted_sux, counted_fails)
    return dist

main()
