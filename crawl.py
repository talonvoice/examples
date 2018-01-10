from talon.voice import Context, Key, Rep, Str, press
ctx = Context('crawl')

import time
import threading
import string

from .std import alpha_alt
# alpha = {k: k for k in string.lowercase}
alpha = {}
alpha.update(dict(zip(alpha_alt, string.ascii_lowercase)))
alpha.update({'sky %s' % word: letter for word, letter in zip(alpha_alt, string.ascii_uppercase)})
alpha.update({'level %d' % k: str(k) for k in range(1, 30)})

# TODO: numbers are used for dungeon levels
# TODO: repeat numbers should change based on whether it was the same phrase?
# TODO: I don't want to put parens around top-level ORs

# TODO: ["next song", "roam"] should work.
# TODO: better debug

def Text(m):
    Str(' '.join(map(str, m.dgndictation[0]._words)))(None)

keymap = {}
keymap.update(alpha)
keymap.update({
    '(right hand | right angle | rangle)': '>',
    '(left hand | left angle | leangle)': '<',

    'minus': '-',
    'plus': '+',
    'bang': '!',
    'dollar': '$',
    'underscore': '_',

    'up':     'k',
    'down':   'j',
    'left':   'h',
    'right':  'l',
    'upple':  'y',
    'downle': 'b',
    'upper':  'u',
    'downer': 'n',

    'way up':     'K',
    'way down':   'J',
    'way left':   'H',
    'way right':  'L',
    'way upple':  'U',
    'way downle': 'B',
    'way upper':  'U',
    'way downer': 'N',

    '(escape | back)': Key('esc'),
    '(enter | shock | ok)': Key('enter'),
    'tarp': Key('tab'),
    '(question mark | question | questo)': '?',
    '(star | asterisk)': '*',
    '(dot | period)': '.',

    '(wander | explore | roam)': 'o',
    '(rest | sleep)': '5',
    'wait': '.',
    '(inventory | invent)': 'i',
    'auto': Key('tab'),
    'fight': Key(' '.join(['tab'] * 10)),
    'stand [and] fight': Key(' '.join(['shift-tab'] * 10)),
    'eat [food]': 'e',
    '(quaff | drink)': 'q',
    'quiver': 'Q',
    'reed': 'r',
    'skills': 'm',
    '(stats | attributes | (char | character) sheet)': '%',
    '(god | piety | religion)': '^',
    'pray': '>',
    'speed': '@',
    'shopping list': '$',

    'cast': 'z',
    'cast last': Key('z . enter'), 'recast': Key('z . enter'),
    'cast (one | a)': 'za',
    'cast (two | b)': 'zb',
    'cast (three | c)': 'zc',
    'cast (four | d)': 'zd',
    'cast (five | e)': 'ze',
    'cast (six | f)': 'zf',
    'cast (seven | g)': 'zg',
    'cast (eight | h)': 'zh',

    'autocast one': Key('z a enter'),
    'autocast two': Key('z b enter'),
    'autocast three': Key('z c enter'),
    'autocast four': Key('z d enter'),
    'autocast five': Key('z e enter'),
    'autocast six': Key('z f enter'),
    'autocast seven': Key('z g enter'),
    'autocast eight': Key('z h enter'),

    'ability': 'a',
    '(mutations | innate abilities)': 'A',

    'talk': 't',
    'shout': 'tt',
    'wear': 'W',
    'wield': 'w',
    'switch weapon': '\'',
    '(memorize | memo)': 'M',
    'put on': 'P',
    'take off': 'T',
    'remove': 'R',
    'drop': 'd',

    # need a rule for letter, as well as this templated string form
    # also, rule functions might need to be passed the entire context, or the chain of contexts that led to them
    # 'drop <letter>': 'd {letter}',

    'evoke': 'V',
    '(evoke weapon | reach)': 'v',

    'fire': 'f',
    '(fire invent | fire inventory | fire item)': 'F',
    'open': 'O',
    'close': 'C',
    'messages': Key('ctrl-p'),

    'look down': ';',
    'examine': 'x',
    'map': 'X',
    'visible [(items | features)]': Key('ctrl-x'),

    '(get | grab | pick up)': 'g',

    'find': Key('ctrl-f'),
    'find plate': Key('ctrl-f p l a t e enter'),
    'find armour': Key('ctrl-f a r m o u r enter'),
    'find blade': Key('ctrl-f b l a d e enter'),
    'find sword': Key('ctrl-f s w o r d enter'),
    'find dagger': Key('ctrl-f d a g g e r enter'),
    'find axe': Key('ctrl-f a x e enter'),
    'find altar': Key('ctrl-f a l t a r enter'),
    'find artifact': Key('ctrl-f a r t i f enter'),
    'find brand': Key('ctrl-f b r a n d enter'),
    'find corpse': Key('ctrl-f c o r p s e enter'),

    'type <dgndictation>': Text,

    'travel': 'G',
    'travel [to] dungeon': 'Gd',
    'travel [to] temple': 'Gt',
    'travel [to] [(orc | orcish)] mines': 'Go',
    'travel [to] lair': 'Gl',
    'travel [to] swamp': 'Gs',
    'travel [to] (spider nest | spider | nest)': 'Gn',
    'travel [to] (slime pits | slime | pits)': 'Gm',
    'travel [to] (elven halls | elven | halls)': 'Ge',
    'travel [to] vaults': 'Gv',
    'travel [to] depths': 'Gu',
    'deepest': '$',
    
    'down stairs': '>',
    'up stairs': '<',

    'yes': 'Y',
    'no': 'N',

    '(cut | chop)': 'c',
    'all': 'a',
    'edible': 'e',
    'choosy': 'c',

    '(adjust | rename)': '=',
    'items': 'i',
    'spells': 's',
    'abilities': 'a',

    'autopickup': Key('ctrl-a'),
    'item knowledge': '\\',

#    'twice': Rep(1),
#    'thrice': Rep(2),
#    'times four': Rep(3),
#    'times five': Rep(4),
#    'times six': Rep(5),
#    'ten': Rep(9),

    '(str | strength)': 's',
    '(int | intel | intelligence)': 'i',
    '(dex | dexterity)': 'd',
})

keymap.update({str(k): Rep(k - 1) for k in range(2, 11)})

'''
stepping = False
def stepthread():
    global stepping
    while stepping:
        press('f6')
        time.sleep(1)

def slowstep(j):
    global stepping
    stepping = True
    threading.Thread(target=stepthread).start()

def stopstep(j):
    global stepping
    if stepping:
        stepping = False
    else:
        press('esc')

keymap.update({
    'slow step': slowstep,
    'halt': stopstep,
})
'''

ctx.keymap(keymap)

def unload(): ctx.disable()
