import os

project_home = "{}/Documents/myprojects/access_logs_sla"\
    .format(os.environ['HOME'])
month = "06"
year = "2020"
start_day = 20
# actual DAY_END is DAY_END - 1
end_day = 23
start_hour = 0
# actual HOUR_END is HOUR_END - 1
end_hour = 24
