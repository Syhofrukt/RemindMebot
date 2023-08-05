import asyncio
from database import table_handler, get_connection
import datetime



#22.06.2023 12:50 +03:00


class TimeZone(datetime.tzinfo):
    def __init__(self):
        self.timedelt = 0
    def utcoffset(self, dt):
        return datetime.timedelta(hours=self.timedelt)

time_managment = TimeZone()



class RemindHandler:
    def __init__(self):
        pass

    def blueprint_create(self, callback_query):
        with get_connection() as conn:
            table_handler.make_blueprint(data=[
                callback_query.from_user.id, callback_query.data, None, None, 1
            ], conn=conn)

    async def remind_set(self, data: str, timezonee: str):

        data3 = data + ' ' + timezonee
        data1 = data3.split('.')
        data2 = data1[2].split()
        hour_minutes = data2[1].split(':')

        day = data1[0]
        month = data1[1]
        year = data2[0]
        hour = hour_minutes[0]
        minutes = hour_minutes[1]
        tz_hour = data2[2]
        time_managment.timedelt = int(tz_hour)
        date_time = datetime.datetime(int(year), int(month), int(day), int(hour), int(minutes), second=0, microsecond=0,
                                      tzinfo=time_managment)

        utc_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=int(tz_hour))))

        difference = datetime.datetime.timestamp(date_time) - datetime.datetime.timestamp(utc_now)

        if difference < 0:
            raise AttributeError('Difference between given time and utc is negative (given date is in Past)')

        sleep = await asyncio.sleep(difference, result='I am reminding you about your message, as you wished me to'
                                               '\nMessage: {}')

        return sleep

    def remind_delete(self):
        pass


