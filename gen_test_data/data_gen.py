import random
import os
import gc
# API's = 60
# Client_ID's = 3000
# time in ms = [10 to 18000]
# print(random.randrange(800000, 802999))
# file content format: client_id API time
# directory structure: {mm}{dd}{yyyy}/log_{hr}.out

# Note: change hr range 0, 23 to 0, 24
home = os.environ['HOME']

for day in range(20, 23):
    log_dir = "{}/Documents/myprojects/access_logs_sla/gen_test_data/data/06{}2020".format(home, day)
    try:
        os.makedirs(log_dir)
    except OSError as e:
        print("Dir creation Exception: {}".format(e))
    for hour in range(0, 23):
        log_name = "{}/log_{}.out".format(log_dir, hour)
        with open(log_name, 'w') as f:
            for _ in range(0, 5000000):
                f.write("{} api_{} {}\n".format(
                    random.randrange(800000, 802999),
                    random.randrange(1, 60),
                    random.randint(1, 18000)
                            )
                        )
