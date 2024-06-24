import discord
from discord.ext import commands
import roll_commands as rs
import support_commands as sc
import settings

TOKEN = 'bot token'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Creates an embed to format a general roll's outcome to be sent to discord. Includes the rolls, whether it was a success or failure, if willpower was used, and how many successes were gained.
def create_embed(member, pool, difficulty, result, sux, willpower):
    if sux > 0:
        outcome = 'Success'
        embed_color = discord.Color.green()
    elif sux == 0:
        outcome = 'Failure'
        embed_color = discord.Color.red()
    else:
        outcome = 'Botch'
        embed_color = discord.Color.red()
        if  sux <= -5:
            outcome = 'Ultra botch LMAO'
    embed = discord.Embed(
        color=embed_color,
        title=f'Pool {pool} | Diff {difficulty}',
        description=f'**Rolls**\n' +
        f'{result}\n\n' +
        f'**Successes**\n' +
        f'{sux}\n' +
        f'```{outcome}```'
    )
    if willpower:
        embed.set_footer='**Willpower used'
    embed.set_author(name=member.display_name, icon_url=member.avatar)


    return embed

def create_attack_embed(member, pool, result, difficulty, willpower):
    if len(result) == 2: # attack_roll, dmg_dice
        embed_color = discord.Color.red()
        outcome = 'Miss'

        embed = discord.Embed(
        color=embed_color,
        title=f'Pool {pool} | Diff {difficulty}',
        description=f'**Rolls**\n' +
        f'{result[0]}\n\n' +
        f'**Successes**\n' +
        f'{result[1]}\n' +
        f'```{outcome}```'
        )
    elif len(result) == 3: # attack_roll, defense_roll, no_hits
        embed_color = discord.Color.red()
        outcome = 'Defended'

        embed = discord.Embed(
        color=embed_color,
        title=f'Pool {pool} | Diff {difficulty}',
        description=f'**Attack Rolls**\n' +
        f'{result[0]}\n\n' +
        f'**Defense Rolls**\n' +
        f'{result[1]}\n\n' +
        f'**Successes**\n' +
        f'{result[2]}\n' +
        f'```{outcome}```'
        )
    elif len(result) == 6: # attack_roll, defense_roll, dmg_dice, dmg_roll, soak_roll, inflicted_dmg
        embed_color = discord.Color.green()
        outcome = 'Hit'

        embed = discord.Embed(
        color=embed_color,
        title=f'Pool {pool} | Diff {difficulty}',
        description=f'**Attack Rolls**\n' +
        f'{result[0]}\n\n' +
        f'**Defense Rolls**\n' +
        f'{result[1]}\n\n' +
        f'**Successes**\n' +
        f'{result[2]}\n' +
        f'**Damage Rolls**\n' +
        f'{result[3]}\n\n' +
        f'**Soak Rolls**\n' +
        f'{result[4]}\n\n' +
        f'**Damage Done**\n' +
        f'{result[5]}\n\n' +
        f'```{outcome}```'
        )
    if willpower:
        embed.set_footer='**Willpower used'
    embed.set_author(name=member.display_name, icon_url=member.avatar)
    return embed
    

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    bot.tree.copy_global_to(guild=settings.GUILD_ID2)
    await bot.tree.sync(guild=settings.GUILD_ID2)
    

@bot.tree.command(name='roll', description='Command for simple rolls.', )
async def roll(interaction: discord.Interaction, pool: int, difficulty: int=6, willpower: bool=False):
    """Descriptions for command arguments
    Args:
        pool (int): How many dice you want to roll. [Usually Attribute + Ability]
        difficulty (int): Number a dice needs to roll to count as a success. [Default is 6]
        willpower (bool): Provides a guaranteed and uncancelable success.
    """
    result, sux = rs.roll(pool, difficulty, willpower)
    roll_embed = create_embed(interaction.user, pool, difficulty, result, sux, willpower)
    roll_emojis = sc.emoji_creation(result, difficulty)

    await interaction.response.send_message(f'{roll_emojis}', embed=roll_embed)

@bot.tree.command(name='attack', description='Generic attack roll', )
async def attack(interaction: discord.Interaction, pool: int, damage: int, soak: int, difficulty: int=6, defense: int=0, willpower: bool=False):
    """Descriptions for command arguments
    Args:
        pool (int): How many dice you want to roll. (Dexterity + Brawl/Melee/Firearms)
        damage (int): Base damage of your chosen attack.
        soak (int): Soak pool of your target. (Stamina + Fortitude).
        difficulty (int): Number a dice needs to roll to count as a success.
        defense (int): Dice pool for your target's defensive action (if any). (Dexterity + Brawl/Athletics/Melee)
        willpower (bool): Provides a guaranteed and uncancelable success to the attack roll.
    """
    result = rs.attack(pool, difficulty, damage, soak, defense, willpower)
    roll_embed = create_attack_embed(interaction.user, pool, result, difficulty, willpower)
    roll_emojis = sc.emoji_creation(result[0], difficulty)

    await interaction.response.send_message(f'{roll_emojis}', embed=roll_embed)
    

bot.run(TOKEN)