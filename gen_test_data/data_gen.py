import random
import os
from properties import *

# API's = 60
# Client_ID's = 3000. Client ID's between 800000 and 802999.
# time in ms = [1 to 18000]
# Data log file content format: client_id API_name time_in_ms
# directory structure: {mm}{dd}{yyyy}/log_{hr}.out

for day in range(start_day, end_day):
    date_format = "{}{}{}".format(month, day, year)
    log_dir = "{}/gen_test_data/data/{}".format(project_home, date_format)
    try:
        os.makedirs(log_dir)
    except OSError as e:
        print("Dir creation Exception: {}".format(e))
    for hour in range(start_hour, end_hour):
        log_name = "{}/log_{}.out".format(log_dir, str(hour).zfill(2))
        print("Generating test data file: {}".format(log_name))
        lines_to_write = []
        # Generates 5 Million lines in every hr data log file with
        # client ID between 800000 to 802999, 60 API's and time taken
        # between 1ms to 18,000ms.
        for _ in range(0, 5000000):
            lines_to_write.append("{} api_{} {}\n".format(
                random.randrange(800000, 802999),
                random.randrange(1, 60),
                random.randint(1, 18000))
                                  )
        with open(log_name, 'w') as f:
            f.writelines(lines_to_write)
