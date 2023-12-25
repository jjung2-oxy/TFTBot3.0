import Levenshtein
import sys


set10_champs = [
    "Annie", "Corki", "Evelynn", "Jinx", "Kennen", "K'Sante", "Lillia", "Nami", "Olaf", "Tahm Kench", "Taric", "Vi", "Yasuo",
    "Aphelios", "Bard", "Garen", "Gnar", "Gragas", "Jax", "Kai'Sa", "Katarina", "Kayle", "Pantheon", "Senna", "Seraphine", "Twitch",
    "Amumu", "Ekko", "Lulu", "Lux", "Miss Fortune", "Mordekaiser", "Neeko", "Riven", "Samira", "Sett", "Urgot", "Vex", "Yone",
    "Ahri", "Akali K/DA", "Akali True-DMG", "Blitzcrank", "Caitlyn", "Ezreal", "Karthus", "Poppy", "Thresh", "Twisted Fate", "Viego", "Zac", "Zed",
    "Illaoi", "Jhin", "Kayn", "Lucian", "Qiyana", "Sona", "Yorick", "Ziggs"
]

set9_champs = [
    "Cassiopeia", "Cho'Gath", "Graves", "Illaoi", "Irelia", "Jhin", "Kayle", "Malzahar", "Milio", "Orianna", "Poppy", "Renekton", "Samira",
    "Ashe", "Galio", "Jinx", "Kassadin", "Naafiri", "Qiyana", "Sett", "Soraka", "Swain", "Taliyah", "Twisted Fate", "Vi", "Warwick",
    "Darius", "Ekko", "Jayce", "Karma", "Katarina", "Miss Fortune", "Nautilus", "Neeko", "Quinn", "Rek'Sai", "Sona", "Taric", "Vel'Koz",
    "Aphelios", "Azir", "Fiora", "Jarvan IV", "Kai'Sa", "Mordekaiser", "Nasus", "Nilah", "Sejuani", "Shen", "Silco", "Xayah",
    "Aatrox", "Ahri", "Bel'Veth", "Gangplank", "Heimerdinger", "K'Sante", "Ryze", "Sion"
]

def create_champion_dict(set10_champs, cost_details):
    champion_dict = {}

    for cost, champs in enumerate(cost_details, start=1):
        for champ_detail in champs:
            # Splitting the champion detail at '(' to separate the name and the traits
            name, traits = champ_detail.split(' (')
            # Removing the closing parenthesis and splitting traits by ', '
            traits = traits[:-1].split(', ')
            # Adding the champion to the dictionary
            champion_dict[name] = {"cost": cost, "traits": traits}

    return champion_dict


cost_1 = [
    "Annie (Spellweaver, Emo)", 
    "Corki (Big Shot, 8-Bit)", 
    "Evelynn (Crowd Diver, K/DA)", 
    "Jinx (Rapidfire, Punk)", 
    "Kennen (Superfan, Guardian, True Damage)", 
    "K'Sante (Sentinel, HEARTSTEEL)", 
    "Lillia (Superfan, Sentinel, K/DA)", 
    "Nami (Dazzler, Disco)", 
    "Olaf (Bruiser, Pentakill)", 
    "Tahm Kench (Bruiser, Country)", 
    "Taric (Guardian, Disco)", 
    "Vi (Mosher, Punk)", 
    "Yasuo (Edgelord, True Damage)"
]

cost_2 = [
    "Aphelios (Rapidfire, HEARTSTEEL)", 
    "Bard (Dazzler, Jazz)", 
    "Garen (Sentinel, 8-bit)", 
    "Gnar (Superfan, Mosher, Pentakill)", 
    "Gragas (Spellweaver, Bruiser, Disco)", 
    "Jax (Mosher, EDM)", 
    "Kai'Sa (Big Shot, K/DA)", 
    "Katarina (Crowd Diver, Country)", 
    "Kayle (Edgelord, Pentakill)", 
    "Pantheon (Guardian, Punk)", 
    "Senna (Rapidfire, True Damage)", 
    "Seraphine (Spellweaver, K/DA)", 
    "Twitch (Executioner, Punk)"
]

cost_3 = [
    "Amumu (Guardian, Emo)", 
    "Ekko (Spellweaver, Sentinel, True Damage)", 
    "Lulu (Spellweaver, Hyperpop)", 
    "Lux (Dazzler, EDM)", 
    "Miss Fortune (Big Shot, Jazz)", 
    "Mordekaiser (Sentinel, Pentakill)", 
    "Neeko (Superfan, Guardian, K/DA)", 
    "Riven (Edgelord, 8-bit)", 
    "Samira (Executioner, Country)", 
    "Sett (Bruiser, Mosher, HEARTSTEEL)", 
    "Urgot (Mosher, Country)", 
    "Vex (Executioner, Emo)", 
    "Yone (Edgelord, Crowd Diver, HEARTSTEEL)"
]

cost_4 = [
    "Ahri (Spellweaver, K/DA)", 
    "Akali K/DA (Breakout, Executioner, K/DA)", 
    "Akali True-DMG (Breakout, Executioner, True Damage)", 
    "Blitzcrank (Sentinel, Disco)", 
    "Caitlyn (Rapidfire, 8-Bit)", 
    "Ezreal (Big Shot, HEARTSTEEL)", 
    "Karthus (Executioner, Pentakill)", 
    "Poppy (Mosher, Emo)", 
    "Thresh (Guardian, Country)", 
    "Twisted Fate (Dazzler, Disco)", 
    "Viego (Edgelord, Pentakill)", 
    "Zac (Bruiser, EDM)", 
    "Zed (Crowd Diver, EDM)"
]

cost_5 = [
    "Illaoi (Bruiser, ILLBEATS)", 
    "Jhin (Big Shot, Maestro)", 
    "Kayn (Wildcard, Edgelord, HEARTSTEEL)", 
    "Lucian (Rapidfire, Jazz)", 
    "Qiyana (Crowd Diver, True Damage)", 
    "Sona (Spellweaver, Mixmaster)", 
    "Yorick (Mosher, Guardian, Pentakill)", 
    "Ziggs (Dazzler, Hyperpop)"
]


cost_details = [cost_1, cost_2, cost_3, cost_4, cost_5]  # Add all cost lists here

# Create the dictionary
champion_info = create_champion_dict(set10_champs, cost_details)

champPool = {"1_cost":29, "2_cost":22, "3_cost":18, "4_cost":12, "5_cost":10}

def find_closest(target, string_list):
    try:
        closest_string = None
        min_distance = float('inf')

        for s in string_list:
            distance = Levenshtein.distance(target, s)
            if distance < min_distance:
                min_distance = distance
                closest_string = s

        return closest_string
    except Exception as e:
        print(f"Error in find_closest: {e}", file=sys.stderr)
        return None