import logging
from collections import namedtuple
from argparse import ArgumentParser

import pendulum
import requests

logging.basicConfig(level=logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logger = logging.getLogger()


def make_cmd_arguments_parser():
    parser_description = 'Script determines who sent tasks between preset time'
    parser = ArgumentParser(description=parser_description)
    parser.add_argument('--start_time', '-s',
                        help='Start value of preset hour (0..23)',
                        type=int,
                        default=0)
    parser.add_argument('--end_time', '-e',
                        help='end value of preset hour (0..23)',
                        type=int,
                        default=6)
    return parser.parse_args()


def load_attempt_json_data(page_number=1):
    api_load_attempts_url = 'https://devman.org/api/challenges/solution_attempts/'
    request = requests.get(api_load_attempts_url,
                           params={'page': page_number})
    return request.json()


def get_attempts_data_generator():
    pages_count = load_attempt_json_data()['number_of_pages']
    for page in range(1, pages_count + 1):
        for user_data in load_attempt_json_data(page)['records']:
            yield {
                'username': user_data['username'],
                'timestamp': user_data['timestamp'],
                'timezone': user_data['timezone']
            }


def get_midnighters_generator(user_attempts_generator, midnight_start_hour=0, midnight_end_hour=6):
    AttemptUserData = namedtuple('AttemptUserData', ['username', 'localized_datetime'])
    for user_attempt_data in user_attempts_generator:
        try:
            attempt_datetime = pendulum.from_timestamp(timestamp=user_attempt_data['timestamp'],
                                                       tz=user_attempt_data['timezone'])
            if midnight_start_hour <= attempt_datetime.hour < midnight_end_hour:
                yield AttemptUserData(username=user_attempt_data['username'],
                                      localized_datetime=attempt_datetime)
        except TypeError as error:
            logging.info('Error: {}. Wrong timestamp user {} '.format(error, user_attempt_data['username']))


if __name__ == '__main__':
    cmd_arguments = make_cmd_arguments_parser()
    midnight_start_hour, midnight_end_hour = cmd_arguments.start_time, cmd_arguments.end_time
    midnight_start_time, midnight_end_time = pendulum.create(hour=midnight_start_hour).to_time_string(),\
                                             pendulum.create(hour=midnight_end_hour).to_time_string()
    print('Users who sent tasks between {} and {}:'.format(midnight_start_time, midnight_end_time))
    for index, midnighter in enumerate(get_midnighters_generator(get_attempts_data_generator(),
                                                                 midnight_start_hour=midnight_start_hour,
                                                                 midnight_end_hour=midnight_end_hour)):
        print('{:3} {} from timezone {} '
              'sent task to review at {}'.format(index,
                                                 midnighter.username,
                                                 midnighter.localized_datetime.timezone_name,
                                                 midnighter.localized_datetime.to_datetime_string()))
