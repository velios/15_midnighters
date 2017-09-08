from datetime import datetime
from collections import namedtuple
from itertools import chain

import pytz
import requests


def load_attempt_json_data(page_number=1):
    api_load_attemts_url = 'https://devman.org/api/challenges/solution_attempts/'
    r = requests.get(api_load_attemts_url,
                     params={'page': page_number})
    return r.json()


def transform_localize_date_from_timestamp(timestamp, timezone):
    if not timestamp:
        raise TypeError('no value timestamp')
    return pytz.timezone(timezone).fromutc(datetime.utcfromtimestamp(timestamp))


def get_attempts_generator():
    pages = load_attempt_json_data()['number_of_pages']
    return [chain(load_attempt_json_data(4)['records']) for x in range(10)]

    # for user_data in chain(load_attempt_json_data(page)['records'] for page in range(pages)):
    #     yield {
    #         'username': user_data['username'],
    #         'timestamp': user_data['timestamp'],
    #         'timezone': user_data['timezone'],
    #     }


def get_midnighters_list(user_attempts_generator, midnight_start_hour=0, midnight_end_hour=23):
    midnighters_list = []
    AttemptUserData = namedtuple('AttemptUserData', ['username', 'localized_datetime'])
    for user_attempt_data in user_attempts_generator:
        try:
            attempt_datetime = transform_localize_date_from_timestamp(timestamp=user_attempt_data['timestamp'],
                                                                      timezone=user_attempt_data['timezone'])
            if midnight_start_hour <= attempt_datetime.hour <= midnight_end_hour:
                midnighters_list.append(AttemptUserData(username=user_attempt_data['username'],
                                                        localized_datetime=attempt_datetime))
        except:
            pass
    return midnighters_list




if __name__ == '__main__':
    # t = transform_localize_date_from_timestamp(1504080907, 'Asia/Vladivostok')
    # # try:
    #     # a = get_midnighters_list(user_attempts_generator=get_attempts_generator())
    a = get_attempts_generator()
    for i in a:
        print(i)
    # for x, i in enumerate(a):
    #     print('{}=>{}=>{}=>{}'.format(x, i['username'], i['timestamp'], i['timezone']))
    # except TypeError as error:
    #     print(error)
    # except pytz.exceptions.UnknownTimeZoneError as error:
    #     print('Timezone error: value {} set to timezone is incorrect'.format(error))

