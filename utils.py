import json
from aiogram import Bot
from aiogram.enums import ParseMode

def get_bot() -> Bot:
    config = json.load(open('config.json', 'rb'))
    return Bot(config["bot_token"], parse_mode=ParseMode.HTML, session=None)

def name_formatter(value):
    value = value.split()
    try:
        value.remove('')
    except:
        pass
    result = []
    for k,i in enumerate(value):
        if k == 0:
            result.append(f'{i[0:1].upper()}{i[1:len(i)].lower()}')
        else:
            result.append(i.lower())
    return ' '.join(result)

def chunks(s, n):
    result = []
    for start in range(0, len(s), n):
        result.append(s[start:start+n])
    return result