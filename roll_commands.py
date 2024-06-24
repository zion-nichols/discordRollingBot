"""Holds all commands the discord bot will use. Will include a generic roll function and combat rolls, automatically rolling for damage and defense."""

import random
import discord

# Primary rolling function. Adjustable dice pool and difficulty, exploding 10s included.
def roll(pool, difficulty, willpower, tens=0):
    roll_count = []  # Creates an empty list to keep track of what is rolled.
    sux = 0  # Creates a counter for how many rolled dice meet the assigned difficulty.
    for x in range(int(pool)):
        roll_count.append(random.randint(1,10))
    for x in roll_count:
        if x >= difficulty:
            sux += 1
        if x == 1:
            sux -= 1
    if tens < (tens + roll_count.count(10)):  # Checks how many tens have been rerolled for exploding dice. If any new 10s are rolled, this will cause a loop until no 10s are rolled.
        explode, explode_sux = roll(roll_count.count(10), difficulty, False, tens=roll_count.count(10))  # Runs the 'roll' function again, but just for 10s. 
        roll_count.append(explode)  # Adds the new rolls to the list. 
        sux = sux + explode_sux  # Adds any new successes to the old counter.
    if willpower:
        if sux < 0:
            sux = 1
        else:
            sux += 1
    return roll_count, sux

# Attack command for no-sheet rolls. Difficulty, defense, and willpower are optional.
def attack(pool, difficulty, damage, soak, defense, willpower):
    defense_roll = None
    attack_roll, dmg_dice = roll(pool, difficulty, willpower)
    if dmg_dice > 0:
        if defense:
            defense_roll, defense_sux = roll(defense, difficulty, False)
            if (dmg_dice - defense_sux) < 1:
                return attack_roll, defense_roll, (dmg_dice - defense_sux)
            else:
                dmg_dice = dmg_dice - defense_sux
        dmg_roll, dmg = roll((dmg_dice + damage - 1), 6, False)
        soak_roll, soak_sux = roll(soak, 6, False)
        inflicted_dmg = dmg - soak_sux
        return attack_roll, defense_roll, dmg_dice, dmg_roll, soak_roll, inflicted_dmg

    return attack_roll, dmg_dice

# Command for specifically melee attacks.
def melee(split_command):
    for x in range(int(split_command[1])):
        print(random.randint(1,10))
