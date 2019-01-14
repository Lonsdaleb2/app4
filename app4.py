import asyncio
import glob
from discord.ext import commands
from discord import Game
from discord.ext.commands import Bot
import pickle
import math
import random
from trade_class import trade_goods
import re
import datetime
import matplotlib.pyplot as plt
from math import *

BOT_PREFIX = ("!")
TOKEN = 'NTIxNjkyMTgwNzE3MjQwMzM0.DvEKQQ.Oc-wmzMhj4wHe6vb-F5r0AoPY6A'

client = Bot(command_prefix=BOT_PREFIX)
server_time_check = datetime.datetime.now()


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="say !help"))
    print("Logged in as " + client.user.name)
    print(client.user.name)
    print(client.user.id)
    print('------')
    global name_file
    name_file = (open('male_npcs.txt').readlines())


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("------\nCurrent servers @ " + server_time_check.strftime("%Y-%m-%d %H:%M:%S") + " :")
        for server in client.servers:
            print("- " + server.name)
        await asyncio.sleep(3600)  # import asyncio required


common_electronics = trade_goods("Common_Electronics", ["All"], "2d6*10", 20000, ["In", 2, "Ht", 3, "Ri", 1],
                                 ["Na", 2, "Lt", 1, "Po", 1], "Simple electronics, basic computers.")
common_industrial = trade_goods("Common_Industrial", ["All"], "2d6*10", 10000, ["Na", 2, "In", 5],
                                ["Ni", 3, "Ag", 2],
                                "Machine components and common spare parts.")
common_manufactured = trade_goods("Common_Manufactured Goods", ["All"], "2d6*10", 20000, ["Na", 2, "In", 5],
                                  ["Ni", 3, "Ag", 2], "Household appliances, clothing, etc.")
common_raw = trade_goods("Common_Raw_Materials", ["All"], "2d6*20", 5000, ["Na", 3, "Ga", 2], ["In", 2, "Po", 2],
                         "Metals, chemicals, plastics, other basic materials.")
common_consumables = trade_goods("Common_Consumables", ["All"], "2d6*20", 500,
                                 ["Ag", 3, "Wa", 2, "Ga", 1, "As", -4],
                                 ["As", 1, "Fl", 1, "Ie", 1, "Hi", 1], "Food, drink and other agri products.")
common_ore = trade_goods("Common_Ore", ["All"], "2d6*20", 1000, ["As", 4], ["In", 3, "Ni", 1],
                         "Ore bearing common metals.")

advanced_electronics = trade_goods("Advanced_Electronics", ["In", "Ht"], "1d6*5", 100000,
                                   ["In", 2, "Ht", 3, "Ri", 1],
                                   ["Na", 2, "Lt", 1, "Po", 1], "Advanced sensors and computers up to TL15.")
advanced_machine = trade_goods("Advanced_Machine_Parts", ["In", "Ht"], "1d6*5", 75000, ["In", 2, "Ht", 1],
                               ["As", 2, "Ni", 1], "Machine components, spare parts up to TL15.")
advanced_manufactured = trade_goods("Advanced_Manufacturing_Goods", ["In", "Ht"], "1d6*5", 100000, ["In", 1],
                                    ["Hi", 1, "Ri", 2], "Devices and clothing incorporating advanced tech.")
advanced_weapons = trade_goods("Advanced_Weapons", ["In", "Ht"], "1d6*5", 150000, ["Ht", 2],
                               ["Po", 1, "Amber", 2, "Red", 4],
                               "Firearms, explosives, ammo, artillery. Military grade.")
advanced_vehicles = trade_goods("Advanced_Vehicles", ["In", "Ht"], "1d6*5", 180000, ["Ht", 2],
                                ["As", 2, "Ri", 2], "Air/rafts, spacecraft, grav tanks, vehicles up to TL15.")
biochemicals = trade_goods("Biochemicals", ["Ag", "Wa"], "1d6*5", 50000, ["Ag", 1, "Wa", 2],
                           ["In", 2], "Biofuels, organic chemicals, extracts.")
crystals_gems = trade_goods("Crystals_&_Gems", ["As", "De", "Ie"], "1d6*5", 20000, ["As", 2, "De", 1, "Ie", 1],
                            ["In", 3, "Ri", 2], "Diamonds, synthetics or natural gemstones.")
cybernetics = trade_goods("Cybernetics", ["Ht"], "1d6", 250000, ["Ht", 1], ["As", 1, "Ie", 1, "Ri", 2],
                          "Cybernetic components, replacement limbs.")
animals = trade_goods("Animals", ["Ag", "Ga"], "1d6*10", 10000, ["Ag", 2], ["Lo", 3],
                      "Riding animals, beasts of burden, exotic pets.")
luxury_consumables = trade_goods("Luxury_Consumables", ["Ag", "Ga", "Wa"], "1d6*10", 20000,
                                 ["Ag", 2, "Wa", 1], ["Ri", 2, "Hi", 2], "Rare foods, fine liquors.")
luxury_goods = trade_goods("Luxury_Goods", ["Hi"], "1d6", 200000, ["Hi", 1], ["Ri", 4],
                           "Rare or extremely high-quality manufactured goods.")
medical_supplies = trade_goods("Medical_Supplies", ["Hi", "Ht"], "1d6*5", 50000, ["Ht", 2],
                               ["In", 2, "Ri", 1, "Po", 1],
                               "Diagnostic equipment, basic drugs, cloning tech.")
petrochemicals = trade_goods("Petrochemicals", ["De", "Fl", "Ie", "Wa"], "1d6*10", 10000, ["De", 2],
                             ["In", 2, "Ag", 1, "Lt", 2], "Oil, liquid fuels.")
pharma = trade_goods("Pharmaceuticals", ["As", "De", "Hi", "Wa"], "1d6", 100000, ["As", 2, "Hi", 1],
                     ["Ri", 2, "Lt", 1], "Drugs, medical supplies, fast/slow drugs, anagathatics.")
polymers = trade_goods("Polymers", ["In"], "1d6*10", 7000, ["In", 1], ["Ri", 2, "Ni", 1],
                       "Plastics and other synthetics.")
precious_metals = trade_goods("Precious_Metals", ["As", "De", "Ie", "Fl"], "1d6", 50000,
                              ["As", 3, "De", 1, "Ie", 2], ["Ri", 3, "In", 2, "Ht", 1],
                              "Gold, silver, platinum, rare elements.")
radioactives = trade_goods("Radioactives", ["As", "De", "Lo"], "1d6", 1000000, ["As", 2, "Lo", 2],
                           ["In", 3, "Ht", 1, "Ni", -2, "Ag", -3], "Uranium, plutonium, unobtanium, rare elements.")
robots = trade_goods("Robots", ["All"], "1d6*5", 400000, ["In", 1], ["Ag", 2, "Ht", 1],
                     "Industrial and personal robots and drones.")
spices = trade_goods("Spices", ["Ga", "De", "Wa"], "1d6*10", 6000, ["De", 2], ["Hi", 2, "Ri", 3, "Po", 3],
                     "Preservatives, luxury food additives, natural drugs.")
textiles = trade_goods("Textiles", ["Ag", "Ni"], "1d6*20", 3000, ["Ag", 7], ["Hi", 3, "Na", 2],
                       "Clothing and fabrics.")
uncommon_ore = trade_goods("Uncommon_Ore", ["As", "Ie"], "1d6*10", 5000, ["As", 4], ["In", 3, "Ni", 1],
                           "Ore containing precious or valuable metals.")
uncommon_raw = trade_goods("Uncommon_Raw_Materials", ["Ag", "De", "Wa"], "1d6*10", 20000, ["Ag", 2, "Wa", 1], [
    "In", 2, "Ht", 1], "Valuable metals, rare elements.")
wood = trade_goods("Wood", ["Ag", "Ga"], "1d6*20", 1000, ["Ag", 6], ["Ri", 2, "In", 1],
                   "Hard or beautiful woods and plant extracts.")
vehicles = trade_goods("Vehicles", ["In", "Ht"], "1d6*10", 15000, ["In", 2, "Ht", 1], ["Ni", 2, "Hi", 1],
                       "Wheeled, tracked and other vehicles from TL10 or lower.")
illegal_bio = trade_goods("Illegal_Biochemicals", ["Ag", "Wa"], "1d6*5", 50000, ["Wa", 2], ["In", 6],
                          "Dangerous chemicals, extracts from endangered species.")
illegal_cyber = trade_goods("Illegal_Cybernetics", ["Ht"], "1d6", 250000, ["Ht", 1],
                            ["As", 4, "Ie", 4, "Ri", 8, "Amber", 6, "Red", 6],
                            "Combat cybernetics, illegal enhancements.")
illegal_drugs = trade_goods("Illegal_Drugs", ["As", "Hi", "De", "Wa"], "1d6", 100000,
                            ["As", 1, "De", 1, "Ga", 1, "Wa", 1], ["Ri", 6, "Hi", 6],
                            "Addictive drugs, combat drugs.")
illegal_luxuries = trade_goods("Illegal_Luxuries", ["Ag", "Ga", "Wa"], "1d6", 50000,
                               ["Ag", 2, "Wa", 1], ["Ri", 6, "Hi", 4], "Debauched or addictive luxuries.")
illegal_weapons = trade_goods("Illegal_Weapons", ["In", "Ht"], "1d6*5", 150000, ["Ht", 2],
                              ["Po", 6, "Amber", 8, "Red", 10], "Weapons of mass destruction, naval weapons.")
exotics = trade_goods("Exotics", ["Special", 1], "1d6", 10, ["Special", 1], ["Special", 1], "Special.")


# 35 entries


class MGT2e:
    "Commands created with the MGT2e ruleset."

    @commands.command(name="Buying goods",
                      description="Automates buying of Traveller trade goods.",
                      brief="!buy - What trade goods are available",
                      aliases=["buying", "buy"],
                      pass_context=True)  # context will mention the original messenger.
    async def buying(self, context):

        purchase_list_buying = {
            0: 1.75,
            1: 1.5,
            2: 1.35,
            3: 1.25,
            4: 1.2,
            5: 1.15,
            6: 1.1,
            7: 1.05,
            8: 1,
            9: 0.95,
            10: 0.9,
            11: 0.85,
            12: 0.8,
            13: 0.75,
            14: 0.7,
            15: 0.65,
            16: 0.6,
            17: 0.55,
            18: 0.5,
            19: 0.45,
            20: 0.4,
            21: 0.35,
            22: 0.3,
            23: 0.25
        }

        await client.say(context.message.author.mention + "\n"
                         + "Please enter your worlds Trade Codes below separated by a space.\n")
        await asyncio.sleep(1)
        user_input = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        user_input_2 = user_input.content
        user_list = user_input_2.split()

        await client.say(context.message.author.mention + "\n"
                         + "What is your Broker skill modifier? -3/0/1/2...\n")
        await asyncio.sleep(1)
        broker_entry_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        broker_entry = broker_entry_2.content

        await client.say(context.message.author.mention + "\n"
                         + "Are you looking for a black-market merchant? yes/no \n")
        await asyncio.sleep(1)
        b_t_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        b_t = b_t_2.content

        if b_t == "no":
            trader_value = 30
        else:
            trader_value = 5

        master_trade_goods_list = []

        if trader_value == 30:
            master_trade_goods_list.append(common_electronics)  # 0
            master_trade_goods_list.append(common_industrial)  # 1
            master_trade_goods_list.append(common_manufactured)  # 2
            master_trade_goods_list.append(common_raw)  # 3
            master_trade_goods_list.append(common_consumables)  # 4
            master_trade_goods_list.append(common_ore)  # 5
            master_trade_goods_list.append(advanced_electronics)  # 6
            master_trade_goods_list.append(advanced_machine)  # 7
            master_trade_goods_list.append(advanced_manufactured)  # 8
            master_trade_goods_list.append(advanced_weapons)  # 9
            master_trade_goods_list.append(advanced_vehicles)  # 10
            master_trade_goods_list.append(biochemicals)  # 11
            master_trade_goods_list.append(crystals_gems)  # 12
            master_trade_goods_list.append(cybernetics)  # 13
            master_trade_goods_list.append(animals)  # 14
            master_trade_goods_list.append(luxury_consumables)  # 15
            master_trade_goods_list.append(luxury_goods)  # 16
            master_trade_goods_list.append(medical_supplies)  # 17
            master_trade_goods_list.append(petrochemicals)  # 18
            master_trade_goods_list.append(pharma)  # 19
            master_trade_goods_list.append(polymers)  # 20
            master_trade_goods_list.append(precious_metals)  # 21
            master_trade_goods_list.append(radioactives)  # 22
            master_trade_goods_list.append(robots)  # 23
            master_trade_goods_list.append(spices)  # 24
            master_trade_goods_list.append(textiles)  # 25
            master_trade_goods_list.append(uncommon_ore)  # 26
            master_trade_goods_list.append(uncommon_raw)  # 27
            master_trade_goods_list.append(wood)  # 28
            master_trade_goods_list.append(vehicles)  # 29
            master_trade_goods_list.append(exotics)  # 30
        if trader_value == 5:
            master_trade_goods_list.append(illegal_bio)  # 31
            master_trade_goods_list.append(illegal_cyber)  # 32
            master_trade_goods_list.append(illegal_drugs)  # 33
            master_trade_goods_list.append(illegal_luxuries)  # 34
            master_trade_goods_list.append(illegal_weapons)  # 35

        print(master_trade_goods_list)

        a = 0
        x = 0
        j = 0
        trade_list_all = []
        while x <= trader_value:
            x += 1

            if "All" in master_trade_goods_list[j].availability:
                temp_all = master_trade_goods_list[j].type
                temp_all_codes = master_trade_goods_list[j].purchase_dm_list
                temp_price = master_trade_goods_list[j].base_price
                temp_quantity = master_trade_goods_list[j].tons
                temp_sale = master_trade_goods_list[j].sale_dm_list

                trade_list_all.append(temp_all)
                trade_list_all.append(temp_price)
                trade_list_all.append(temp_quantity)
                trade_list_all.append(temp_all_codes)
                trade_list_all.append(temp_sale)
                j += 1
        print("All list complete")

        a = 0
        j = 0
        k = 0
        x = 0
        while j < trader_value:
            print(master_trade_goods_list[j].type)
            if a >= len(user_list):
                print("A limit has been reached, moving onto next J")
                a = 0
                j += 1
            elif user_list[a] in master_trade_goods_list[j].availability:
                print(user_list[a] + " is in ")
                print(master_trade_goods_list[j].availability)
                temp_any = master_trade_goods_list[j].type
                temp_any_codes = master_trade_goods_list[j].purchase_dm_list
                temp_any_price = master_trade_goods_list[j].base_price
                temp_any_quantity = master_trade_goods_list[j].tons
                temp_sale_codes = master_trade_goods_list[j].sale_dm_list

                trade_list_all.append(temp_any)
                trade_list_all.append(temp_any_price)
                trade_list_all.append(temp_any_quantity)
                trade_list_all.append(temp_any_codes)
                trade_list_all.append(temp_sale_codes)
                a += 0
                j += 1
                print("Match has been found. Moving to next J")
            elif user_list[a] not in master_trade_goods_list[j].availability:
                print(user_list[a] + " is not in ")
                print(master_trade_goods_list[j].availability)
                a += 1

        random_goods_list = []
        random_roll = random.randint(1, 6)
        a = 1
        print(random_roll)
        while a <= random_roll:
            random_goods_roll = random.randint(0, (trader_value - 1))
            print(random_goods_roll)
            random_goods_name = master_trade_goods_list[random_goods_roll].type
            random_goods_price = master_trade_goods_list[random_goods_roll].base_price
            random_goods_quan = master_trade_goods_list[random_goods_roll].tons
            random_goods_codes = master_trade_goods_list[random_goods_roll].purchase_dm_list
            random_sale_codes = master_trade_goods_list[random_goods_roll].sale_dm_list

            random_goods_list.append(random_goods_name)
            random_goods_list.append(random_goods_price)
            random_goods_list.append(random_goods_quan)
            random_goods_list.append(random_goods_codes)
            random_goods_list.append(random_sale_codes)
            a += 1
            print(random_goods_list)

        trade_list_all.extend(random_goods_list)

        print("Starting trade list")
        print(trade_list_all)

        new_list = []  # this sees which purchase trade code modifiers need to be added
        maths_list = []
        a = 0
        y = 3
        z = 0
        print(trade_list_all[2][0])
        while y <= len(trade_list_all):
            if a >= len(user_list):
                print("A is not in XY and is greater than user length")
                y += 5
                z = 0
                a = 0
                if len(new_list) >= 1:
                    modifier_number_string = "+".join(new_list)
                    print(modifier_number_string)
                    price_temp = eval(modifier_number_string)
                    maths_list.append(price_temp)
                    new_list.clear()
                    print(maths_list)
                else:
                    maths_list.append(8)
            elif user_list[a] == trade_list_all[y][z]:
                new_list.append(str(trade_list_all[y][z + 1]))
                a += 1
                z = 0
                print("A is in Y,Z")
                print(new_list)
            elif user_list[a] != trade_list_all[y][z]:
                z += 2
                print("A is not in Y,Z")
                if z >= len(trade_list_all[y]):
                    a += 1
                    z = 0
                    print("Resetting Z")
        print("This is the proper list")
        print(maths_list)

        new_list = []
        maths_list_2 = []
        a = 0
        y = 4
        z = 0
        print(trade_list_all[2][0])
        while y <= len(trade_list_all):
            if a >= len(user_list):
                print("A is not in XY and is greater than user length")
                y += 5
                z = 0
                a = 0
                if len(new_list) >= 1:
                    modifier_number_string = "+".join(new_list)
                    print(modifier_number_string)
                    price_temp = eval(modifier_number_string)
                    maths_list_2.append(price_temp)
                    new_list.clear()
                    print(maths_list_2)
                else:
                    maths_list_2.append(0)
            elif user_list[a] == trade_list_all[y][z]:
                new_list.append(str(trade_list_all[y][z + 1]))
                a += 1
                z = 0
                print("A is in Y,Z")
                print(new_list)
            elif user_list[a] != trade_list_all[y][z]:
                z += 2
                print("A is not in Y,Z")
                if z >= len(trade_list_all[y]):
                    a += 1
                    z = 0
                    print("Resetting Z")
        print("This is the sales modifier list")
        print(maths_list_2)
        print(maths_list)

        a = 0
        while a < len(maths_list):
            dice_roll = eval(
                str(random.randint(1, 6)) + "+" + str(random.randint(1, 6)) + "+" + str(random.randint(1, 6)))
            dice_plus_mod = str(dice_roll) + "+" + str(broker_entry) + "-" + str(maths_list_2[a])
            dice_plus_mod = eval(dice_plus_mod)
            temp_number = str(maths_list[a])
            maths_list[a] = (eval((temp_number) + "+" + str(dice_plus_mod)))
            a += 1
            print(maths_list)  # this takes the maths_list and adds the players own modifiers, then runs
            # it through the modifier dict (dice roll and broker skill)

        a = 0
        x = 1
        while x <= len(maths_list):
            x += 1
            replacement = maths_list[a]
            if replacement >= 23:
                b = 0.25
            elif replacement <= 0:
                b = 0.25
            else:
                b = purchase_list_buying.get(replacement)
            maths_list[a] = b
            a += 1
        print(maths_list)  # this gives us the %-based modifiers to tweak the goods base cost. 0.5/1.15 etc

        a = 0
        c = 1
        while a < len(maths_list):
            replacement = float((maths_list[a]))
            trade_list_all[c] = "- Cr " + str(round(replacement * int(trade_list_all[c]))) + "/ton,"
            a += 1
            c += 5
        print(trade_list_all)  # this puts the modified prices into the original list.

        b = 3
        while b <= len(trade_list_all):
            trade_list_all.remove(trade_list_all[b])
            b += 4
        print("First trade list")
        print(trade_list_all)  # this removes the trade codes

        b = 3
        while b <= len(trade_list_all):
            trade_list_all.remove(trade_list_all[b])
            b += 3
        print("Second trade list")
        print(trade_list_all)  # this removes the 2nd set of trade codes, giving us just item and its cost.

        h = 2
        dice_holding_pen = []
        while h <= len(trade_list_all):
            temp_dice = trade_list_all[h]
            dice_holding_pen.append(temp_dice)
            dice_holding_pen.append(h)
            print(dice_holding_pen)
            h += 3

        #########start of dice maths
        print(dice_holding_pen)
        dice_holding_pen_2 = []
        AA = 0
        BB = 0
        while AA <= len(dice_holding_pen):
            AA += 2
            if AA <= len(dice_holding_pen):
                dice = str(dice_holding_pen[BB])
                dice = dice.replace("*", " multiply ")
                dicelist = re.sub("[^\w]", " ", dice).split()
                print("The input. Splitting each piece to be worked on separately. ")
                print(dicelist)

                dice_coords = []  # this shows where the dice belong in the original dicelist
                space = " "
                a = 1
                b = 0
                letters = set("d")
                while a <= len(dicelist):
                    a += 1
                    for w in dicelist:
                        if letters & set(w):
                            dice_location = dicelist.index(w)
                            print(w + " " + str(dice_location))
                            dicelist[dice_location] = space
                            dice_coords.append(w)
                            dice_coords.append(dice_location)
                            b += 1
                            print(dice_coords)

                the_dice_var = dice_coords[0::2]
                the_location_var = dice_coords[1::2]
                print("Location of dice and what dice need to be rolled:")
                print(the_location_var)
                print(the_dice_var)

                quantity_1 = 0
                dice_post_while = []
                while quantity_1 < len(the_dice_var):
                    the_dice_var_while = the_dice_var[quantity_1].split("d")
                    quantity_1 += 1
                    dice_post_while.append(the_dice_var_while)
                print(dice_post_while)

                quantity_2 = 0
                times_to_roll = []
                dice_type = []
                while quantity_2 < len(dice_post_while):
                    times_to_roll_while = dice_post_while[quantity_2][0]
                    dice_type_while = dice_post_while[quantity_2][1]
                    quantity_2 += 1
                    times_to_roll.append(times_to_roll_while)
                    dice_type.append(dice_type_while)
                print("Number of times the dice need to rolled and what type they are.")
                print(times_to_roll)
                print(dice_type)
                print("The generated dice:")

                roll_entry = 0
                master_dice_numbers = []
                j = 1
                a = len(times_to_roll)
                while j <= a:
                    j += 1
                    x = 1
                    dice_numbers = []
                    master_dice_numbers.append(dice_numbers)
                    t = times_to_roll[roll_entry]
                    d = dice_type[roll_entry]
                    roll_entry += 1

                    while x <= int(t):
                        roll = random.randint(1, int((d)))
                        dice_total = 0
                        dice_total += roll
                        x += 1
                        dice_numbers.append(dice_total)
                    print(dice_numbers)
                print(
                    "Master list for the now generated dice numbers. These will use the above location_var to put them back into"
                    " their original place")
                print(master_dice_numbers)

                x = 1
                e = 0
                d = 0
                while x <= len(the_location_var):
                    c = int(the_location_var[e])
                    b = (master_dice_numbers[d])
                    dicelist[c] = b  # insert location, then thing you want to insert
                    x += 1
                    e += 1
                    d += 1

                x = 1
                a = 0
                while x <= len(the_location_var):
                    Q = the_location_var[a]
                    dice_string = "+".join(str(e) for e in (dicelist[Q]))  # - to turn a list into a string
                    dicelist[Q] = ("(" + dice_string + ")")
                    x += 1
                    a += 1
                print(
                    "The original entry list, now with all of the generated numbers. Just needs to be put back together.")
                print(dicelist)

                dicelist = "".join(dicelist)

                sum_of_dice = dicelist.replace("multiply", "*")
                print("The finished article.")
                print(sum_of_dice)
                dicelist = str(eval(sum_of_dice))
                print("The sum.")
                print(dicelist)
                dice_holding_pen_2.append(dicelist + " tons.\n")  # Eg: " + "**" + special +"**")
                print(dice_holding_pen_2)
                BB += 2

        print("does this work")
        g = 0
        h = 0
        while g < len(dice_holding_pen_2):
            dice_holding_pen[h] = (dice_holding_pen_2[g])
            g += 1
            h += 2

        print(dice_holding_pen)

        p = 2
        m = 0
        while p <= len(trade_list_all):
            trade_list_all[p] = dice_holding_pen[m]
            p += 3
            m += 2

        print(
            trade_list_all)  # now we have the goods, their adjusted costs, and generated tons that are available to buy
        final_length = len(trade_list_all)
        random_insert = final_length - (random_roll * 3)
        trade_list_all.insert(random_insert, "\n Below are random goods that are only available for a limited time. \n")

        trade_list_string = " ".join(trade_list_all)

        await client.say(context.message.author.mention + " here are the goods currently available from the merchant.\n"
                         + trade_list_string)
        print(trade_list_string)

    @commands.command(name="Selling goods",
                      description="Automates selling of Traveller trade goods.",
                      brief="!sell - Selling price of goods",
                      aliases=["selling", "sell"],
                      pass_context=True)  # context will mention the original messenger.
    async def selling(self, context):

        master_trade_goods_list = []
        master_trade_goods_list.append(common_electronics)  # 0
        master_trade_goods_list.append(common_industrial)  # 1
        master_trade_goods_list.append(common_manufactured)  # 2
        master_trade_goods_list.append(common_raw)  # 3
        master_trade_goods_list.append(common_consumables)  # 4
        master_trade_goods_list.append(common_ore)  # 5
        master_trade_goods_list.append(advanced_electronics)  # 6
        master_trade_goods_list.append(advanced_machine)  # 7
        master_trade_goods_list.append(advanced_manufactured)  # 8
        master_trade_goods_list.append(advanced_weapons)  # 9
        master_trade_goods_list.append(advanced_vehicles)  # 10
        master_trade_goods_list.append(biochemicals)  # 11
        master_trade_goods_list.append(crystals_gems)  # 12
        master_trade_goods_list.append(cybernetics)  # 13
        master_trade_goods_list.append(animals)  # 14
        master_trade_goods_list.append(luxury_consumables)  # 15
        master_trade_goods_list.append(luxury_goods)  # 16
        master_trade_goods_list.append(medical_supplies)  # 17
        master_trade_goods_list.append(petrochemicals)  # 18
        master_trade_goods_list.append(pharma)  # 19
        master_trade_goods_list.append(polymers)  # 20
        master_trade_goods_list.append(precious_metals)  # 21
        master_trade_goods_list.append(radioactives)  # 22
        master_trade_goods_list.append(robots)  # 23
        master_trade_goods_list.append(spices)  # 24
        master_trade_goods_list.append(textiles)  # 25
        master_trade_goods_list.append(uncommon_ore)  # 26
        master_trade_goods_list.append(uncommon_raw)  # 27
        master_trade_goods_list.append(wood)  # 28
        master_trade_goods_list.append(vehicles)  # 29
        master_trade_goods_list.append(exotics)  # 30
        master_trade_goods_list.append(illegal_bio)  # 31
        master_trade_goods_list.append(illegal_cyber)  # 32
        master_trade_goods_list.append(illegal_drugs)  # 33
        master_trade_goods_list.append(illegal_luxuries)  # 34
        master_trade_goods_list.append(illegal_weapons)  # 35

        print(master_trade_goods_list)

        await client.say(context.message.author.mention + "\n"
                         + "Please enter your worlds Trade Codes below, separated by a space.\n")
        await asyncio.sleep(1)
        user_input_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        user_input = user_input_2.content
        user_list = user_input.split()

        await client.say(context.message.author.mention + "\n"
                         + "What is your Broker skill modifier?  -3/0/1/2... \n")
        await asyncio.sleep(1)
        broker_entry_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        broker_entry = broker_entry_2.content

        await client.say(context.message.author.mention + "\n"
                         + "What good/s are you selling? \n Separate each entry with a space and use underscores for gaps within a name. Eg: Wood Illegal_Weapons \n")
        await asyncio.sleep(1)
        arg_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        arg = arg_2.content
        arg = arg.split()
        print(arg)

        purchase_list_buying = {
            0: 0.4,
            1: 0.45,
            2: 0.5,
            3: 0.55,
            4: 0.6,
            5: 0.65,
            6: 0.7,
            7: 0.75,
            8: 0.8,
            9: 0.85,
            10: 0.9,
            11: 1,
            12: 1.05,
            13: 1.1,
            14: 1.15,
            15: 1.2,
            16: 1.25,
            17: 1.3,
            18: 1.35,
            19: 1.4,
            20: 1.45,
            21: 1.5,
            22: 1.55,
            23: 1.6,
        }

        selling_list = []
        j = 0
        a = 0

        while j < len(master_trade_goods_list):
            if a >= len(arg):
                a = 0
                j += 1
                print("A is too long. Moving to next J")
            elif arg[a].lower() == (master_trade_goods_list[j].type).lower():
                temp_all_codes = master_trade_goods_list[j].sale_dm_list
                temp_price = master_trade_goods_list[j].base_price
                temp_sale_codes = master_trade_goods_list[j].purchase_dm_list

                selling_list.append(arg[a])
                selling_list.append(temp_price)
                selling_list.append(temp_all_codes)
                selling_list.append(temp_sale_codes)
                print("Found a match. Resetting A and moving to next J")
                j += 1
                a += 0

            elif arg[a].lower() != (master_trade_goods_list[j].type).lower():
                print("No")
                a += 1
        print(selling_list)

        new_list = []  # this sees which purchase trade code modifiers need to be added
        maths_list = []
        a = 0
        y = 2
        z = 0

        while y <= len(selling_list):
            if a >= len(user_list):
                print("A is not in XY and is greater than user length")
                y += 4
                z = 0
                a = 0
                if len(new_list) >= 1:
                    modifier_number_string = "+".join(new_list)
                    print(modifier_number_string)
                    price_temp = eval(modifier_number_string)
                    maths_list.append(price_temp)
                    new_list.clear()
                    print(maths_list)
                else:
                    maths_list.append(11)
            elif user_list[a] == selling_list[y][z]:
                new_list.append(str(selling_list[y][z + 1]))
                a += 1
                z = 0
                print("A is in Y,Z")
                print(new_list)
            elif user_list[a] != selling_list[y][z]:
                z += 2
                print("A is not in Y,Z")
                if z >= len(selling_list[y]):
                    a += 1
                    z = 0
                    print("Resetting Z")
        print("This is the selling list")
        print(maths_list)

        new_list = []
        maths_list_2 = []
        a = 0
        y = 3
        z = 0

        while y <= len(selling_list):
            if a >= len(user_list):
                print("A is not in XY and is greater than user length")
                y += 4
                z = 0
                a = 0
                if len(new_list) >= 1:
                    modifier_number_string = "+".join(new_list)
                    print(modifier_number_string)
                    price_temp = eval(modifier_number_string)
                    maths_list_2.append(price_temp)
                    new_list.clear()
                    print(maths_list_2)
                else:
                    maths_list_2.append(0)
            elif user_list[a] == selling_list[y][z]:
                new_list.append(str((selling_list[y][z + 1])))
                a += 1
                z = 0
                print("A is in Y,Z")
                print(new_list)
            elif user_list[a] != selling_list[y][z]:
                z += 2
                print("A is not in Y,Z")
                if z >= len(selling_list[y]):
                    a += 1
                    z = 0
                    print("Resetting Z")
        print("This is the purchase modifier list")
        print(maths_list_2)
        print(maths_list)

        a = 0
        while a < len(maths_list):
            dice_roll = eval(
                str(random.randint(1, 6)) + "+" + str(random.randint(1, 6)) + "+" + str(random.randint(1, 6)))
            dice_plus_mod = str(dice_roll) + "+" + str(broker_entry) + "-" + str(maths_list_2[a])
            dice_plus_mod = eval(dice_plus_mod)
            temp_number = str(maths_list[a])
            maths_list[a] = (eval((temp_number) + "+" + str(dice_plus_mod)))
            a += 1
            print(
                maths_list)  # this takes the maths_list and adds the players own modifiers, then runns it through the modifier dict (dice roll and broker skill)

        a = 0
        x = 1
        while x <= len(maths_list):
            x += 1
            replacement = maths_list[a]
            if replacement >= 23:
                b = 1.6
            elif replacement <= 0:
                b = 0.3
            else:
                b = purchase_list_buying.get(replacement)
            maths_list[a] = b
            a += 1
        print(maths_list)  # this gives us the %-based modifiers to tweak the goods base cost. 0.5/1.15 etc

        a = 0
        c = 1
        while a < len(maths_list):
            replacement = float((maths_list[a]))
            selling_list[c] = "- Cr " + str(round(replacement * int(selling_list[c]))) + "/ton.\n"
            a += 1
            c += 4
        print(selling_list)  # this puts the modified prices into the original list.

        b = 2
        while b < len(selling_list):
            selling_list.remove(selling_list[b])
            b += 3
            print("del pls")
        print(selling_list)  # this removes the trade codes

        b = 2
        while b <= len(selling_list):
            selling_list.remove(selling_list[b])
            b += 2
        print(selling_list)  # this removes the 2nd set of trade codes, giving us just item and its cost.

        selling_list_string = " ".join(selling_list)
        print(selling_list_string)
        await client.say(
            context.message.author.mention + " the local trader you have found will buy your goods for the following prices:\n"
            + selling_list_string)

    


client.add_cog(MGT2e())


class Universal:
    "Universal commands that don't rely on specific rules."

    @commands.command(name="UWP Translator",
                      description="Converts UWP numbers using the following format:\n "
                                  "Starport Planet-Size Atmosphere Hydroponics Population Government Law-Level Tech-Level",
                      brief="!uwp - Translates UWP",
                      aliases=["UWP", "uwp"],
                      pass_context=True)
    async def uwp(self, context, starqual, plansize, atmostype, hydro, pop, gov, law, tech):  # input variable

        starport_quality = {
            "0": "None",
            "A": "Excellent: Refined Fuel, Full Shipyard, Full repairs",
            "B": "Good: Refined Fuel, Spacecraft Shipyard, Full repairs",
            "C": "Average: Unrefined Fuel, Smallcraft shipyard, Full repairs",
            "D": "Poor: Unrefined Fuel, Limited Repairs",
            "E": "Frontier: No fuel, no repairs",
        }
        planet_size = {
            "0": "<1000km, 0g, No Gravity",
            "1": "1600km, 0.05g, Low Gravity",
            "2": "3200km, 0.15g, Low Gravity",
            "3": "4800km, 0.25g, Low Gravity",
            "4": "6400km, 0.35g, Low Gravity",
            "5": "8000km, 0.45g, Low Gravity",
            "6": "9600km, 0.7g, Low Gravity",
            "7": "11200km, 0.9g, Standard Gravity",
            "8": "12800km, 1.0g, Standard Gravity",
            "9": "14400km, 1.25g, Standard Gravity",
            "A": "16000km, 1.4g, High Gravity"
        }
        atmosphere_type = {
            "0": "None, Pressure: None, Protection: Vacc Suit",
            "1": "Trace, Pressure: 0.05, Protection: Vacc Suit",
            "2": "V.Thin & Tainted, Pressure: 0.2, Protection: Respirator & Filter",
            "3": "V.Thin, Pressure: 0.2, Protection: Respirator",
            "4": "Thin & Tainted, Pressure: 0.6, Protection: Filter",
            "5": "Thin, Pressure: 0.6, Protection: -",
            "6": "Standard, Pressure: 1.0, Protection: -",
            "7": "Tainted, Pressure: 1.0, Protection: Filter",
            "8": "Dense, Pressure: 2.0, Protection: -",
            "9": "Dense & Tainted, Pressure: 2.0, Protection: Filter",
            "A": "Exotic, Pressure: Varies, Protection: Air Supply",
            "B": "Corrosive, Pressure: Varies, Protection: Vacc Suit",
            "C": "Insidious, Pressure: Varies, Protection: Vacc Suit",
            "D": "V.Dense, Pressure: 2.5+, Protection: -",
            "E": "Low, Pressure: <0.5, Protection: -",
            "F": "Unusual, Pressure: Varies, Protection: -",
        }
        hydrographic_perc = {
            "0": "0-5%",
            "1": "6-15%",
            "2": "16-25%",
            "3": "26-35%",
            "4": "36-45%",
            "5": "46-55%",
            "6": "56-65%",
            "7": "66-75%",
            "8": "76-85%",
            "9": "86-95%",
            "A": "96-100%",
        }
        population_amount = {
            "0": "<10",
            "1": "~100",
            "2": "~1k",
            "3": "~10k",
            "4": "~100k",
            "5": "~1 mil",
            "6": "~10 mil",
            "7": "~100 mil",
            "8": "~1 bil",
            "9": "~10 bil",
            "A": "~100 bil",
            "B": "~1 tril",
            "C": "~10 tril",
            "D": "~100 tril",
            "E": "~1 quadril",
            "F": "~10 quadril",
        }
        government_type = {
            "0": "None, Contraband: None",
            "1": "Coorporation, Contraband: Drugs, Travellers, Weapons",
            "2": "Participating Democracy, Contraband: Drugs",
            "3": "Self-perpetuating Oligarchy, Contraband: Tech, Travellers, Weapons",
            "4": "Representative Democracy, Contraband: Drugs, Psionics, Weapons",
            "5": "Feudal Technocracy, Contraband: Computers, Tech, Weapons",
            "6": "Captive Government, Contraband: Tech, Travellers, Weapons",
            "7": "Balkanization, Contraband: Varies",
            "8": "Civil Service Bureacracy, Contraband: Drugs, Weapons",
            "9": "Impersonal Bureacracy, Contraband: Drugs, Psionics, Tech, Travellers, Weapons",
            "A": "Charismatic Dictator, Contraband: None ",
            "B": "Non-Charismatic Dictator, Contraband: Computers, Tech, Weapons",
            "C": "Charismatic Oligarchy, Contraband: Weapons",
            "D": "Religious Dictatorship, Contraband: Varies",
            "E": "Religious Autocracy, Contraband: Varies",
            "F": "Totalitarian Oligarchy, Contraband: Varies",
        }
        law_level = {
            "0": "Banned Weapons: -, Banned Armour: - ",
            "1": "Banned Weapons: -, Banned Armour: Battle Dress ",
            "2": "Banned Weapons: Portable Energy & Lasers, Banned Armour: Combat Armour ",
            "3": "Banned Weapons: Military Weapons, Banned Armour: Flak ",
            "4": "Banned Weapons: Light assault weapons & SMGs, Banned Armour: Cloth ",
            "5": "Banned Weapons: Personal concealed weapons, Banned Armour: Mesh ",
            "6": "Banned Weapons: All firearms apart from shotguns & stunners, Banned Armour: - ",
            "7": "Banned Weapons: Shotguns, Banned Armour: - ",
            "8": "Banned Weapons: All bladed weapons, stunners, Banned Armour: All visible armour ",
            "9": "Banned Weapons: All weapons, Banned Armour: All armour ",
        }
        tech_level = {
            "0": "**TL0**: Primitive - simple tools.",
            "1": "**TL1**: Primitive - basic weapons.",
            "2": "**TL2**: Primitive - Renaissance-era",
            "3": "**TL3**: Primitive - Early Industrial Revolution, Steam power",
            "4": "**TL4**: Industrial - Late Industrial Revolution, Radio & Plastics",
            "5": "**TL5**: Industrial - Early Atomic-Era, Electricity & Simple computing",
            "6": "**TL6**: Industrial - Late Atomic-Era, Fission power & Advanced computing",
            "7": "**TL7**: Pre-Stellar - Reliable telecommunications satellites, Common computing",
            "8": "**TL8**: Pre-Stellar - Reaching other worlds, Space habitats, No terraforming",
            "9": "**TL9**: Pre-Stellar - Gravity manipulation, Jump drive, Colonising worlds",
            "10": "**TL10**: Early Stellar - Visiting other systems, Orbital factories, Stable colonies",
            "11": "**TL11**: Early Stellar - Early A.I, Space elevators, Jump-2 travel ",
            "12": "**TL12**: Average Stellar - Weather manipulation, Plasma weapons, Fusion guns, Jump-3",
            "13": "**TL13**: Average Stellar - Full battle armour, Cloning, Underwater spacecraft, Jump-4",
            "14": "**Tl14**: Average Stellar - Man-portable fusion, Flying cities, Jump-5",
            "15": "**TL15**: High Stellar - Synthetic anagathics, Black Globe technology, Jump-6"
        }

        starport = starport_quality.get(starqual)
        planet = planet_size.get(plansize)
        atmosphere = atmosphere_type.get(atmostype)
        hydrographics = hydrographic_perc.get(hydro)
        population = population_amount.get(pop)
        government = government_type.get(gov)
        law_output = law_level.get(law)
        tech_output = tech_level.get(tech)

        uwp_output = (", your UWP code:\n "
                      + "**Starport**(" + starqual + "): " + starport + "\n"
                      + "**Planet Info**(" + plansize + "): " + planet + "\n"
                      + "**Atmosphere**(" + atmostype + "): " + atmosphere + "\n"
                      + "**Hydrographics**(" + hydro + "): " + hydrographics + "\n"
                      + "**Population**(" + pop + "): " + population + "\n"
                      + "**Government**(" + gov + "): " + government + "\n"
                      + "**Law Level**(" + law + "): " + law_output + "\n"
                      + tech_output)

        await client.say(context.message.author.mention + uwp_output)  # print

    @uwp.error
    async def uwp_handler(self, error, context):
        if isinstance(error, commands.MissingRequiredArgument):
            await client.say(context.message.author.mention + ", your UWP code is incorrect. "
                                                              "```Please use the format: !uwp X X X X X X X X \n"
                                                              "\tEg. !uwp A 1 2 3 4 5 6 7```")
    
    
    
    
    
    @commands.command(name="system map",
                    description="Generates a map of a solar system",
                    brief="!map - create or call a map",
                    aliases=["map"],
                    pass_context=True)
    async def system_map(self, context):
        earth_orb_time = 365  # how many days it takes for a full orbit of the sun
        print("Command fired")

        planet_start = 0  # degrees

        await client.say(context.message.author.mention + " Enter the system name/ID. Use underscores for spaces. ")
        system_id_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        system_id = system_id_2.content
        system_list = []
        if system_id + ".p" not in str(glob.glob("*.p")):  # this section checks and finds the persistent file.
            print("File not found")
            x = 1

            await client.say(
                context.message.author.mention + " Solar system does not yet exist. How many planets are in this system?")
            number_of_planets_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            number_of_planets = number_of_planets_2.content
            await client.say(
                context.message.author.mention + " Do you want to - A: Enter the system data yourself? B: Use science to help generate it? A/B ")
            check = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            check = check.content
            if check.lower() == "a":
                x = 1
                while x <= int(number_of_planets):
                    system_list.append(planet_start + random.randint(1, 359))
                    await client.say(context.message.author.mention + " How many days does planet number " + str(
                        x) + " take to orbit the sun?")
                    days_of_rotation_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
                    days_of_rotation = days_of_rotation_2.content
                    system_list.append(days_of_rotation)
                    await client.say(context.message.author.mention + " How far away is planet number " + str(
                        x) + " from the sun? Use KM.")
                    planet_distance_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
                    planet_distance = planet_distance_2.content
                    system_list.append(planet_distance)
                    x += 1
            elif check.lower() == "b":
                await client.say(
                    context.message.author.mention + " What is the relative mass of the system's star? (Sol = 1)")
                star_mass_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
                star_mass = star_mass_2.content
                x = 1
                while x <= int(number_of_planets):
                    system_list.append(planet_start + random.randint(1, 359))
                    await client.say(context.message.author.mention + " How many AU is planet " + str(
                        x) + " from the star? (1 AU = 1500mil km)")
                    planet_distance_au_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
                    planet_distance_au = planet_distance_au_2.content
                    planet_distance_km = float(planet_distance_au) * 1500000000
                    days_of_rotation = sqrt((float(planet_distance_au)** 3) / float(star_mass))
                    days_of_rotation = days_of_rotation * 365
                    system_list.append(round(days_of_rotation, 2))
                    system_list.append(planet_distance_km)
                    x += 1
            print("system created")
            time_passed = False
            print(system_list)
            pickle.dump(system_list,open(system_id + ".p", "wb"))  # if it doesnt exist, creates a file and dumps data in.
            print("pickle dumped")
        else:
            print("File found.")
            time_passed = True

        system_list = pickle.load(open(system_id + ".p", "rb"))  # opens the persistent file to draw the data
        print("Pickle file loaded")

        system_planets = system_list[0::3]
        system_orbit_time = system_list[1::3]
        half_system_list = len(system_list) / 3
        if time_passed == True:
            await client.say(
                context.message.author.mention + " How many days have passed since you were last in this system? ")
            days_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            days = days_2.content
            x = 0
            y = 0
            while x < half_system_list:
                orbit_degrees = (360 / (int(system_orbit_time[x]))) * (int(days))
                degrees_1 = system_planets[x] + orbit_degrees
                if degrees_1 >= 360:
                    degrees_1 = degrees_1 - 360  # when earth goes beyond 360 degrees, reset it to 0 for a new cycle.
                system_planets[x] = degrees_1
                system_list[y] = round(system_planets[x], 2)
                y += 3
                print(system_list)
                x += 1
        else:
            days = 0

        print(system_list)

        a = 1
        b = 0
        while a <= len(system_list) / 3:
            print("Planet " + str(a) + " is " + str(system_list[b]) + " degrees.")
            b += 3
            a += 1

        line_points = []
        a = 0
        b = 0
        c = 2
        while a < len(system_list) / 3:
            body_degree = system_list[b]  # degrees
            if 0 < body_degree <= 90:
                body_degree = body_degree
                x = True
                y = True

            elif 90 < body_degree <= 180:
                body_degree = 180 - body_degree
                x = True
                y = False

            elif 180 < body_degree <= 270:
                body_degree = 270 - body_degree
                x = False
                y = False

            elif 270 < body_degree <= 360:
                body_degree = 360 - body_degree
                x = False
                y = True

            body_distance = float(system_list[c]) / 1500000000  # distance from sun in KM
            body_radians = body_degree * (math.pi / 180)
            x_coord = math.sin(body_radians) * body_distance
            y_coord = math.cos(body_radians) * body_distance
            if x == False:
                x_coord = 0 - x_coord
            elif x == True:
                x_coord = x_coord
            if y == False:
                y_coord = 0 - y_coord
            elif y == True:
                y_coord = y_coord

            line_points.append(x_coord)
            line_points.append(y_coord)
            a += 1
            b += 3
            c += 3

            print(line_points)
        print(line_points)

        sun = plt.Circle((0, 0), 0.2, color='y')

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax = plt.gca()
        ax.cla()


        planet_distance_au = system_list[-1] / 1500000000
        planet_chart = (planet_distance_au)+0.5

        ax.set_xlim((0-planet_chart, planet_chart))
        ax.set_ylim((0-planet_chart, planet_chart))

        ax.add_artist(sun)
        ax.text((-planet_chart-1.5), (planet_chart+0.5), r"System: " + system_id, fontsize=9,
                bbox={'facecolor': 'white', 'edgecolor': 'black', 'pad': 5})

        ax.text(-0.7, (planet_chart), r"0 degrees"+"\n"+"(Coreward)", fontsize=8, bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 2})

        ax.text(-0.9, -(planet_chart+2), r"180 degrees"+"\n"+"(Rimward)", fontsize=8, bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 2})



        a = 0
        b = 2
        while a < len(system_list) / 3:
            distance_au = float(system_list[b]) / 1500000000
            circle = plt.Circle((0, 0), distance_au, color='grey', fill=False) #these are the orbit rings
            ax.add_artist(circle)
            a += 1
            b += 3

        z = 0
        a = 0
        b = 1
        c = 0
        d = 2
        e = 0
        f = -1
        colour_list = ["black", "green", "red", "blue", "pink", "brown", "purple", "orange"]
        planet_text=["Orbit details:\n"]
        while z < len(line_points)/2:
            xx = line_points[a]
            yy = line_points[b]
            distance_au = float(system_list[d]) / 1500000000
            angle = system_list[e]
            circle = plt.Circle((xx, yy), 0.2, color=random.choice(colour_list))
            ax.add_artist(circle)
            planet_text.append("" + str(z + 1) + " : " + str(round(distance_au, 1)) + " AU @ " + str(angle) + " deg.\n")
            #ax.text(planet_chart-1,planet_chart+f ,
            #        r"Planet " + str(z + 1) + ": " + str(round(distance_au, 1)) + " AU @ " + str(angle) + " deg.",
            #        fontsize=8,
            #        bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 3})

            a += 2
            b += 2
            c += 1
            d += 3
            e += 3
            f -= 1
            z += 1
        planet_text = "".join(planet_text)
        ax.text(planet_chart - 1, 0, r""+planet_text,fontsize=8,
                    bbox={'facecolor': 'white', 'edgecolor': 'none', 'pad': 3})


        channel = context.message.channel
        fig.savefig(system_id + '_map.png')
        file = system_id + '_map.png'
        await client.send_file(channel, file, content="", filename=file)

        await asyncio.sleep(1)

        pickle.dump(system_list, open(system_id + ".p", "wb"))

        await client.say(
            context.message.author.mention + " Do you want to calculate a distance between two points? y/n  ")
        distance_check_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        distance_check = distance_check_2.content

        if distance_check.lower() == "y":

            await client.say(context.message.author.mention + " Do you want to input KM or AU? km/au")
            await asyncio.sleep(1)
            au_check_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            au_check = au_check_2.content

            if au_check.lower() == "au":
                au_check = True
            await asyncio.sleep(1)

            await client.say(context.message.author.mention + " First body - Distance from the sun: ")
            await asyncio.sleep(1)
            distance_A_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            distance_A = distance_A_2.content

            await client.say(context.message.author.mention + " First body - Relative angle: ")
            await asyncio.sleep(1)
            sun_degrees_A_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            sun_degrees_A = sun_degrees_A_2.content

            await client.say(context.message.author.mention + " Second body - Distance from the sun:  ")
            await asyncio.sleep(1)
            distance_B_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            distance_B = distance_B_2.content

            await client.say(context.message.author.mention + " Second body - Relative angle: ")
            await asyncio.sleep(1)
            sun_degrees_B_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
            sun_degrees_B = sun_degrees_B_2.content

            if au_check == True:
                distance_A = float(distance_A) * 1500000000
                distance_B = float(distance_B) * 1500000000

            sun_degrees_A = float(sun_degrees_A)
            sun_degrees_B = float(sun_degrees_B)

            sun_degrees_highest = max(sun_degrees_A, sun_degrees_B)
            sun_degrees_lowest = min(sun_degrees_A, sun_degrees_B)

            if sun_degrees_highest <= 180 and sun_degrees_lowest < 180:  # both below 180
                sun_degrees = sun_degrees_highest - sun_degrees_lowest
                print("both below")
            elif sun_degrees_highest >= 180 and sun_degrees_lowest <= 180:  # one above, one below
                sun_degrees = (360 - sun_degrees_highest) + sun_degrees_lowest
                print("one above one below")
            elif sun_degrees_highest > 180 and sun_degrees_lowest >= 180:  # both above 180
                sun_degrees = (360 - sun_degrees_lowest) - (360 - sun_degrees_highest)
                print("both above")

            print("sun degrees")
            print(sun_degrees)

            sun_radians = sun_degrees * (math.pi / 180)
            print("sun radians")
            print(sun_radians)

            if distance_A > distance_B:
                larger_distance = distance_A
                smaller_distance = distance_B
            else:
                larger_distance = distance_B
                smaller_distance = distance_A

            if 0 < sun_degrees < 90:
                z = (math.sin(sun_radians)) * larger_distance
                print(math.sin(sun_radians))
                print("z: " + str(z))

                y_a = math.pow(larger_distance, 2) - math.pow(z, 2)
                y_a = math.sqrt(y_a)
                print("y_a: " + str(y_a))

                y_b = y_a - smaller_distance
                print("y_b: " + str(y_b))

                x_b = math.pow(y_b, 2) + math.pow(z, 2)
                x_b = math.sqrt(x_b)
                x_b = round(x_b, 3)  # round to 3 digits after the decimal place

                x_b_au = round((x_b / 1500000000), 3)
                x_b = "{:,}".format(x_b)

                await client.say(context.message.author.mention +
                                 ": Distance between the two points = \n" + str(x_b) + " KM / " + str(x_b_au) + " AU.")

            if 90 < sun_degrees <= 180:
                new_radians = math.pi - sun_radians
                print(new_radians)

                z = (math.sin(new_radians)) * larger_distance
                print(math.sin(new_radians))
                print("z: " + str(z))

                y_a = math.pow(larger_distance, 2) - math.pow(z, 2)
                y_a = math.sqrt(y_a)
                print("y_a: " + str(y_a))

                y_b = y_a + smaller_distance
                print("y_b: " + str(y_b))

                x_b = math.pow(y_b, 2) + math.pow(z, 2)
                x_b = math.sqrt(x_b)
                x_b = round(x_b, 3)  # round to 3 digits after the decimal place

                x_b_au = round((x_b / 1500000000), 3)
                x_b = "{:,}".format(x_b)

                await client.say(context.message.author.mention +
                                 ": Distance between the two points = \n" + str(x_b) + " KM / " + str(x_b_au) + " AU.")

    @commands.command(name="dice roller",
                      description="Rolls dice",
                      brief="!r XdY - rolls dice",
                      aliases=["r", "roll", "dice"],
                      pass_context=True)  # context will mention the original messenger.
    async def dice_roll(self, context, entry):
        dice = entry
        dice = dice.replace("+", " plus ")
        dice = dice.replace("-", " minus ")
        dice = dice.replace(".", " point ")
        dice = dice.replace("*", " multiply ")
        dice = dice.replace("/", " splitup ")
        dicelist = re.sub("[^\w]", " ", dice).split()
        print("The input. Splitting each piece to be worked on separately. ")
        print(dicelist)

        dice_coords = []  # this shows where the dice belong in the original dicelist
        space = " "
        a = 1
        b = 0
        letters = set("d")
        while a <= len(dicelist):
            a += 1
            for w in dicelist:
                if letters & set(w):
                    dice_location = dicelist.index(w)
                    print(w + " " + str(dice_location))
                    dicelist[dice_location] = space
                    dice_coords.append(w)
                    dice_coords.append(dice_location)
                    b += 1
                    print(dice_coords)

        the_dice_var = dice_coords[0::2]
        the_location_var = dice_coords[1::2]
        print("Location of dice and what dice need to be rolled:")
        print(the_location_var)
        print(the_dice_var)

        quantity_1 = 0
        dice_post_while = []
        while quantity_1 < len(the_dice_var):
            the_dice_var_while = the_dice_var[quantity_1].split("d")
            quantity_1 += 1
            dice_post_while.append(the_dice_var_while)
        print(dice_post_while)

        quantity_2 = 0
        times_to_roll = []
        dice_type = []
        while quantity_2 < len(dice_post_while):
            times_to_roll_while = dice_post_while[quantity_2][0]
            dice_type_while = dice_post_while[quantity_2][1]
            quantity_2 += 1
            times_to_roll.append(times_to_roll_while)
            dice_type.append(dice_type_while)
        print("Number of times the dice need to rolled and what type they are.")
        print(times_to_roll)
        print(dice_type)
        print("The generated dice:")
        roll_entry = 0
        master_dice_numbers = []
        j = 1
        a = len(times_to_roll)
        while j <= a:
            j += 1
            x = 1
            dice_numbers = []
            master_dice_numbers.append(dice_numbers)
            t = times_to_roll[roll_entry]
            d = dice_type[roll_entry]
            roll_entry += 1

            while x <= int(t):
                roll = random.randint(1, int((d)))
                dice_total = 0
                dice_total += roll
                x += 1
                dice_numbers.append(dice_total)
            print(dice_numbers)
        print(
            "Master list for the now generated dice numbers. These will use the above location_var to put them back into"
            " their original place")
        print(master_dice_numbers)

        x = 1
        e = 0
        d = 0
        while x <= len(the_location_var):
            c = int(the_location_var[e])
            b = (master_dice_numbers[d])
            dicelist[c] = b  # insert location, then thing you want to insert
            x += 1
            e += 1
            d += 1

        x = 1
        a = 0
        while x <= len(the_location_var):
            Q = the_location_var[a]
            dice_string = "+".join(str(e) for e in (dicelist[Q]))  # - to turn a list into a string
            dicelist[Q] = ("(" + dice_string + ")")
            x += 1
            a += 1
        print("The original entry list, now with all of the generated numbers. Just needs to be put back together.")
        print(dicelist)

        dicelist = "".join(dicelist)

        sum_of_dice = dicelist.replace("plus", "+")
        sum_of_dice = sum_of_dice.replace("minus", "-")
        sum_of_dice = sum_of_dice.replace("point", ".")  ###
        sum_of_dice = sum_of_dice.replace("multiply", "*")
        sum_of_dice = sum_of_dice.replace("splitup", "/")
        print("The finished article.")
        print(sum_of_dice)
        dicelist = eval(sum_of_dice)
        print("The sum.")
        print(dicelist)

        await client.say(context.message.author.mention + "  :  ``rolling:" + str(entry) + "``  :  "
                         + sum_of_dice
                         + " = "
                         + str(dicelist))

    @commands.command(name="Travel time",
                      description="How long is the journey?",
                      brief="!t - Journey time in space",
                      aliases=["travel", "t", "trav"],
                      pass_context=True)
    async def travel_time(self, context):

        planet_size = {
            "0": 1000,
            "1": 1600,
            "2": 3200,
            "3": 4800,
            "4": 6400,
            "5": 8000,
            "6": 9600,
            "7": 11200,
            "8": 12800,
            "9": 14400,
            "A": 16000
        }

        await client.say(context.message.author.mention +
                         "  Enter a distance (eg: 100km), or a UWP character "
                         "if approaching/departing a planetary jump point : ")
        await asyncio.sleep(1)
        planet_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        planet = planet_2.content

        planet_out = 0
        jump = False
        correct_answer = 0
        while correct_answer == 0:
            if "km" in planet:
                jump = False
                planet = planet.replace("km", "")
                planet_out = int(planet)
                correct_answer += 1
            elif planet in planet_size:
                jump = True
                planet_out_3 = planet_size.get(planet)
                planet_out = (planet_out_3 * 100)  # this adds the extra '100diameter' jump limit zeros
                correct_answer += 1
            elif "km" not in planet and planet not in planet_size:
                await client.say(context.message.author.mention +
                                 "  **ERROR:** Please enter a valid UWP character or "
                                 "a distance with 'km' afterwards. Eg: 1000km ")
                planet_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
                planet = planet_2.content

        await client.say(context.message.author.mention +
                         "What's your ships speed rating? (G) ")
        await asyncio.sleep(0.5)
        speed_2 = await client.wait_for_message(author=context.message.author, channel=context.message.channel)
        speed = speed_2.content
        await asyncio.sleep(1)

        speed = int(speed)  # 1g = 9.81m/s
        maths_speed = speed * 9.81

        distance_sum = (planet_out * 1000)  # converts it from KM to M
        a = round((distance_sum / maths_speed), 9)
        print(a)
        root_subject = math.sqrt(a)
        a = (root_subject * 2)

        seconds = a

        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        if jump == False:
            await client.say(context.message.author.mention +
                             "  Distance to target (d/h/m/s): \n" + "%d:%d:%02d:%02d" % (d, h, m, s) + "\n"
                             + "(Travelling " + str(planet_out) + "km @ " + str(speed) + "G)")
        if jump == True:
            await client.say(context.message.author.mention +
                             "   Distance to/from 100D jump point of category-" + str(
                planet) + " planet: (d/h/m/s): \n" + "%d:%d:%02d:%02d" % (
                                 d, h, m, s) + "\n"
                             + "(Travelling " + str(planet_out) + "km @ " + str(speed) + "G)")

    @commands.command(name="Random NPC",
                      description="Random npc",
                      brief="!npc - generate a random NPC for inspiration",
                      aliases=["npc"],
                      pass_context=True)
    async def random_npc(self, context):

        line = random.choice(name_file)
        name_final = (line)

        gender = ["Male", "Female", "Androgynous"]
        r_gen = random.choice(gender)
        if r_gen == "Male":
            gender_2 = "He"
            gender_pos = "His"
        elif r_gen == "Female":
            gender_2 = "She"
            gender_pos = "Her"
        else:
            gender_2 = "They"
            gender_pos = "Their"
        age_range = ["early", "mid", "late"]
        range = random.choice(age_range)
        age_tens = random.randint(2, 8)
        age_final = (range + " " + str(age_tens) + "0's")

        Colours = [
            "Red",
            "Orange",
            "Yellow",
            "Green",
            "Cyan",
            "Blue",
            "Indigo",
            "Violet",
            "Purple",
            "Magenta",
            "Pink",
            "Brown",
            "White",
            "Gray",
            "Black",
            "Blonde",
        ]

        hair = random.randint(1, 5)
        if hair != 5:
            colour = random.choice(Colours)
            hair_final = (colour + " coloured hair.")
        else:
            hair_final = ("They are bald.")

        clothes_adj = [
            "formal",
            "clean",
            "dirty",
            "torn",
            "informal",
            "tailored",
            "ill fitting",
            "smart",
            "stylish",
            "rumpled",
            "professional",
            "stained",
            "pristine",
            "crisp",
            "new",
            "old",
            "modern",
            "trendy",
            "slimming",
        ]

        clothes = random.choice(clothes_adj)
        clothes_2 = random.choice(clothes_adj)
        if clothes_2 == clothes:
            clothes_2 = random.choice(clothes_adj)
        clothes_final = (gender_pos + " " + "clothes are a mix of " + clothes + " and " + clothes_2 + ".")

        voice_list = [
            "a thick",
            "a light",
            "an educated",
            "a common",
        ]

        voice = random.choice(voice_list)
        if gender_2 == "They":
            h_h = "have"
        else:
            h_h = "has"
        voice_final = gender_2 + " " + h_h + " " + voice + " accent."

        await client.say(context.message.author.mention + ", you meet: " + name_final
                         + r_gen + ", "
                         + age_final + "\n"
                         + hair_final + " "
                         + clothes_final + "\n"
                         + voice_final
                         )

    @commands.command(name="wallet",
                      description="manages your funds",
                      brief="!wallet - keep track of your finances",
                      aliases=["wal", "w"],
                      pass_context=True)
    async def wallet(self, context, command, number, *args):

        user_id = context.message.author.id
        f = str(user_id + ".txt")
        command_list = ["buy", "sell", "transfer", "pay"]

        if user_id + ".p" not in str(glob.glob("*.p")):
            print("File not found")
            current_credits = 0
            pickle.dump(current_credits, open(user_id + ".p", "wb"))
        else:
            print("pickle file found.")

        if f not in str(glob.glob("*.txt")):
            file = open(f, "w")
            file.write("start" + " \n")
            file.close()
        else:
            print("text file found")

        if command == "show":
            current_credits = pickle.load(open(user_id + ".p", "rb"))
            await client.say(context.message.author.mention
                             + " your current wallet is: Cr" + str(current_credits))

        elif command in command_list:
            current_credits = pickle.load(open(user_id + ".p", "rb"))
            current_credits_2 = eval(str(current_credits) + str(number))

            await client.say(context.message.author.mention
                             + " : " + str(current_credits) + " " + str(number) + "\n"
                             + " Your new account total is: Cr" + str(current_credits_2))

            pickle.dump(current_credits_2, open(user_id + ".p", "wb"))

            file = open(f, "a")
            edit_list = []
            edit_list.append(number)
            for args in args:
                edit_list.append(args)
                print(edit_list)
            edit_string = " ".join(str(e) for e in edit_list)
            file.write(edit_string + "\n")
            file.close()

        elif command == "history":

            if number == "income":
                income_list = []
                with open(f) as search:
                    for line in search:
                        if "+" == line[0]:
                            income_list.append(line)
                            income_string = "".join(str(e) for e in income_list)
                await client.say(context.message.author.mention
                                 + " your incoming account log/s are as follows:\n"
                                 + income_string)

            elif number == "outgoing":
                outgoing_list = []
                with open(f) as search:
                    for line in search:
                        if "-" == line[0]:
                            outgoing_list.append(line)
                            outgoing_string = "".join(str(e) for e in outgoing_list)
                await client.say(context.message.author.mention
                                 + " your outgoing account log/s are as follows:\n"
                                 + outgoing_string)

            elif number != "outgoing" or "income":

                file = open(f, "r")
                file_length = int(len(file.readlines()))
                file.close()
                history_var = int(number)
                print("it works?")
                history_count = file_length - history_var
                if history_count <= 0:
                    history_count = 0

                file = open(f, "r")
                requested_transactions = file.readlines()[history_count:]
                print(requested_transactions)
                requested_transactions_string = "".join(str(e) for e in requested_transactions)
                await client.say(context.message.author.mention
                                 + " your last **" + str(history_var) + "** account log/s are as follows:\n"
                                 + "\n"
                                 + requested_transactions_string)
                file.close()

    @wallet.error
    async def wallet_handler(self, error, context):
        if isinstance(error, commands.MissingRequiredArgument):
            await client.say(context.message.author.mention
                             + ", please use the following commands:\n"
                             + "```!wallet show x\n\tShows current balance\n"
                               "!wallet buy/pay/sell +/-X note"
                               "\n\tAdd or subtract X funds, with a note for your account history.\n"
                               "\tEg. !wallet pay -350 new chair for ship"
                               "\n!wallet history income/outgoing/X\n\tView X most recent transaction logs, or only income or outgoing."
                               "\n\tEg. !wallet history 5``` ")


client.add_cog(Universal())


class Homebrew:
    "Homebrew rules created from multiple editions. Use with care."

    @commands.command(name="re-entry/orbit",
                      description="time between surface / orbit",
                      brief="!entry / !orbit A B C D :: inspired by T5",
                      aliases=["entry", "orbit"],
                      pass_context=True)
    async def entry_orbit(self, context, speed, planet, atmos, armour):

        speed = int(speed)
        atmos = int(atmos)
        armour = int(armour)

        if planet == "A":
            planet = 10
        else:
            planet = int(planet)

        planet_size = {
            0: 1000,
            1: 1600,
            2: 3200,
            3: 4800,
            4: 6400,
            5: 8000,
            6: 9600,
            7: 11200,
            8: 12800,
            9: 14400,
            10: 16000
        }

        atmos_type = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            "A": 10,
            "B": 11,
            "C": 12,
            "D": 13,
            "E": 14,
            "F": 15
        }

        speed_percentage = {
            1: 1,
            2: 0.74,
            3: 0.56,
            4: 0.45,
            5: 0.38,
            6: 0.36

        }
        print(speed)
        print(atmos)
        print(planet)
        atmos_2 = atmos_type.get(atmos)
        print(atmos_2)

        safe = (planet + atmos_2) * (planet + 2)
        slow = (planet + atmos_2) * ((planet / 2) + 1)
        fast = planet + atmos_2

        safe_2 = round(safe * speed_percentage.get(speed))
        slow_2 = round(slow * speed_percentage.get(speed))
        fast_2 = round(fast * speed_percentage.get(speed))

        ship_armour = armour
        fast_damage = atmos_2 - ship_armour
        if fast_damage <= 0:
            fast_damage = 0
        fast_total = round(fast_damage * (fast_2 / 2))
        slow_damage = round((atmos_2 / 2) - ship_armour)
        if slow_damage <= 0:
            slow_damage = 0
        slow_total = round(slow_damage * (slow_2 / 4))
        await client.say(context.message.author.mention
                         + " ``speed: " + str(speed)
                         + "G. Planet size: " + str(planet) + " / " + str(planet_size.get(planet)) + "km"
                         + ". Atmosphere: " + str(atmos_2) + "``\n"
                         + "*Travelling between orbit and surface on this planet will take:*\n"
                         + "\tFAST: " + str(fast_2) + " minutes - (" + str(
            fast_damage) + ") damage every 2 minutes = " + str(fast_total) + " damage.\n"
                         + "\tSLOW: " + str(slow_2) + " minutes - (" + str(
            slow_damage) + ") damage every 4 minutes = " + str(slow_total) + " damage. \n"
                         + "\tSAFE: " + str(safe_2) + " minutes - no damage\n"
                         + "*damage = atmos number - armour(" + str(ship_armour) + ")*")

    @entry_orbit.error
    async def entry_orbit_handler(self, error, context):
        if isinstance(error, commands.MissingRequiredArgument):
            await client.say(context.message.author.mention + ", use the following format: "
                             + "```speed rating, UWP planet character, UWP atmosphere character, ship armour. "
                               "\n\teg. !entry 4 3 2 1```")


client.add_cog(Homebrew())

client.loop.create_task(list_servers())

client.run(TOKEN)
