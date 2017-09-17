# Night Owls Detector

The script determines which of the users sent task to review in specified time interval. Users provides by [Devman API.](http://devman.org/api/challenges/solution_attempts/http://devman.org/api/challenges/solution_attempts/?page=2)

### How to install

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

### How to use
##### Sample run
```bash
$ python seek_dev_nighters.py -s 4 -e 8
Users who sent tasks between 04:00:00 and 08:00:00:
  0 ТимурДжаганов from timezone Europe/Moscow sent task to review at 2017-09-11 06:14:49
  1 ТимурДжаганов from timezone Europe/Moscow sent task to review at 2017-09-07 05:56:32
  2 RamusikValery from timezone Europe/Moscow sent task to review at 2017-09-07 05:39:18
  ...
```
##### Arguments
```bash
optional arguments:
  -h, --help            show this help message and exit
  --start_time START_TIME, -s START_TIME
                        Start value of preset hour (0..23)
  --end_time END_TIME, -e END_TIME
                        end value of preset hour (0..23)
```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
