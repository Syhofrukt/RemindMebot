from pyrogram import filters

async def filter_startswithint(_, __, message):
    try:
        type(int(message.text[0])) == int

    except ValueError:
        print('Message content is not int')

    else:
        return type(int(message.text[0])) == int


async def filter_notstartswithint(_, __, message):
    try:
        type(int(message.text[0]))

    except ValueError:
        return True

    else:
        print("Message startswith integer")


async def filter_callback_query_get_tz(_, __, callback_query):
    return callback_query.message.text == 'Please choose your timezone'

async def filter_favourite_tz(_, __, callback_query):
    return callback_query.message.text == 'Please choose one timezone from your favourites, for applying it to a remind'



int_filter = filters.create(filter_startswithint)
str_filter = filters.create(filter_notstartswithint)
cq_tz_filter = filters.create(filter_callback_query_get_tz)
favourite_tz_filter = filters.create(filter_favourite_tz)