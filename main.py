import time

from pyrogram import Client, filters





from filt.validation import Remind
from database import table_handler, get_connection
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from filt.core import int_filter, str_filter, cq_tz_filter, favourite_tz_filter

from core import remind_handler


app = Client("RemindMe_bot", bot_token='6013183448:AAFQiL-LnaWkPPAjIHnTC17jQoOuxinVzms')



UTC_BUTTONS = [

                [InlineKeyboardButton('UTC+0', '+0'), InlineKeyboardButton('UTC+1', '+1'), InlineKeyboardButton('UTC+2', '+2'), InlineKeyboardButton('UTC+3', '+3')],
                [InlineKeyboardButton('UTC+4', '+4'), InlineKeyboardButton('UTC+5', '+5'), InlineKeyboardButton('UTC+6', '+6'), InlineKeyboardButton('UTC+7', '+7')],
                [InlineKeyboardButton('UTC+8', '+8'), InlineKeyboardButton('UTC+9', '+9'), InlineKeyboardButton('UTC+10', '+10'), InlineKeyboardButton('UTC+11', '+11')],
                [InlineKeyboardButton('UTC+12', '+12'), InlineKeyboardButton('UTC-1', '-1'), InlineKeyboardButton('UTC-2', '-2'), InlineKeyboardButton('UTC-3', '-3')],
                [InlineKeyboardButton('UTC-4', '-4'), InlineKeyboardButton('UTC-5', '-5'), InlineKeyboardButton('UTC-6', '-6'), InlineKeyboardButton('UTC-7', '-7')],
                [InlineKeyboardButton('UTC-8', '-8'), InlineKeyboardButton('UTC-9', '-9'), InlineKeyboardButton('UTC-10', '-10'), InlineKeyboardButton('UTC-11', '-11')],
                [InlineKeyboardButton('UTC-12', '-12')]

                    ]



@app.on_message(filters.command('start'))
async def start(client, message):
    await app.send_message(chat_id=message.chat.id, text=
    'Hi! My name is Remind me Bot. As you can see I will help you with reminding your notes and stuff.'
    '\n'
    '\nType /help to see full list of commands.'
    '\nBefore we will start, type /tz to choose your Timezone.')


@app.on_message(filters.command('tz'))
async def start(client, message):
    await app.send_message(chat_id=message.chat.id, text='Please choose your timezone', reply_markup=InlineKeyboardMarkup(UTC_BUTTONS))

#Сделать так, что если уже есть пустая запись с таймзоной, то чтобы она не создавалась второй раз после повторного
#нажатия /старт, для того чтобы лишний раз не заполнять базу пустыми ячейками

    @app.on_callback_query(cq_tz_filter)
    async def get_tz(client, callback_query):
        remind_handler.blueprint_create(callback_query)
        await app.send_message(chat_id=callback_query.message.chat.id,
                               text=f'Ok, set timezone is UTC{callback_query.data}')

@app.on_message(filters.command('help'))
async def help(client, message):
    await app.send_message(chat_id=message.chat.id, text=
    'Full list of commands:'
    '\n/tz - set your timezone'
    '\n/help - see full list of commands'
    '\n/remind - set a new remind of your note')



#Сделать диалоговое окно, если есть несколько таймзон, то чтобы через кнопку пользователь сам выбрал какую менять,
# потому что если этого не сделать, в базе меняються оба значения, и выходит путаница


@app.on_message(filters.command('remind'))
async def get_favourite_timezone(client, message):
    with get_connection() as conn:
        blueprints = table_handler.get_blueprints(data=message.from_user.id, conn=conn)

        if len(blueprints) == 1:
            print(blueprints[0][2])

        if blueprints == []:
            await app.send_message(chat_id=message.chat.id, text="Firstly, you have to set your favourite timezone "
                                                                 "with /tz or /start command\n"
                                                                 "You can choose more than one timezone")

        if len(blueprints) > 1:
            TZ_BUTTONS = [[]]
            for blueprint in blueprints:
                tz = blueprint[2]
                TZ_BUTTONS[0].append(InlineKeyboardButton('UTC{}'.format(tz), '{}'.format(tz)))

            await app.send_message(chat_id=message.chat.id, text=
            'Please choose one timezone from your favourites, for applying it to a remind',
                                   reply_markup=InlineKeyboardMarkup(TZ_BUTTONS))

            @app.on_callback_query(favourite_tz_filter)
            async def get_result(client, callback_query):
                table_handler.create_remind([callback_query.from_user.id, callback_query.data], conn=conn)
                await app.send_message(chat_id=callback_query.message.chat.id,
                                       text="Okay, send me the name of reminder\n"
                                            "\n"
                                            "Name can't start with a number, so incorrect value will be ignored")




    # сделать так чтобы когда вызываеться команда, даже если первое сообщение содержит время, а не название как должно быть, чтобы
    # оно всеравно просило название в первую очередь

                @app.on_message(filters.text & str_filter)
                async def get_message(client, message):
                    name = message.text
                    valid_remind1 = Remind(user_id=message.from_user.id, remind_name=name)
                    await app.send_message(chat_id=message.chat.id, text=
                    f'Your remind name is: {valid_remind1.remind_name}. Next send me at what time you want to get reminded')


                    @app.on_message(filters.text & int_filter)
                    async def get_time(client, message):
                        str_time = message.text
                        try:
                            remind_time = time.strptime(str_time, f'%d.%m.%Y %H:%M')
                        except ValueError:
                            await app.send_message(chat_id=message.chat.id, text='Your date has to fit in requirements:\n'
                                                                                 '"day.month.year hour:minute"')

                        else:
                            valid_remind = Remind(user_id=message.from_user.id, remind_timedata=remind_time)

# Вот тут надо сделать так чтоб если выходит ошибка, то сообщение ОК ваша напоминалка поставлена не выходила (либо удалялась потом)

                            try:
                                await app.send_message(chat_id=message.chat.id, text=f'Ok. Your set time is {str_time}')
                                msg_text = await remind_handler.remind_set(str_time, callback_query.data)


                                with get_connection() as conn:
                                    table_handler.set_name_time(
                                        [message.from_user.id, callback_query.data, valid_remind1.remind_name, str_time], conn=conn
                                    )

                                remind_message = table_handler.get_by_datetime(data=[message.from_user.id, callback_query.data, str_time], conn=conn)[3]


                                await app.send_message(chat_id=message.chat.id, text=msg_text.format(remind_message))
                                # тут должно быть удаление напоминалки с блюпринт = 0 по названию и т.д
                            except AttributeError:
                                await app.send_message(chat_id=message.chat.id, text="You can't put a past date")



# выдает сначала сообщение о том что напоминалка поставлена, а потом если время неправильное, то выдает ошибку, хотя
# первого сообщения и не должно было быть (по идее), если их поменять местами, то при успешной операции, сообщение
# появиться только после того как прийдет сама напоминалка (что делает его бессмысленным)









# Когда много пустых записей, вместо того чтобы вставлять время и имя в одну из них, оно берет все и вставляет в них,
# надо сделать так чтобы брались не все записи, а только по одной, либо сделать так чтобы нельзя было сделать больше
# чем одну запись пустой (ну чтобы в базе хранилась максимум 1 пустая запись от каждого пользователя)

# и если пользователь делает новую запись с новым таймзоном, при том что в базе уже была пустая запись с ДРУГИМ таймзоном
# старая запись с ДРУГИМ таймзоном должна удаляться, (либо можно сделать так чтобы она просто переписывалась через UPDATE)
# (так будет даже лучше)




app.run()







