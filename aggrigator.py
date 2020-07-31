from collections import defaultdict
import os
from properties import *
# file: {mm}{dd}{yyyy}/log_0.out
# Output format:
# Date hr client_id API max_time count avg (all, lt_1, 1_3, 3_5, gt_5)

data_path = "{}/data/".format(project_home)
reports_dir = "{}/reports".format(project_home)

try:
    os.makedirs(reports_dir)
except OSError as e:
    print("Dir creation Exception: {}".format(e))

for day in range(start_day, end_day):
    date_format = "{}{}{}".format(month, day, year)
    data_dir = "{}/data/{}".format(project_home, date_format)
    report_file = "{}/{}.csv".format(reports_dir, date_format)
    header = "Date, Hour, client_ID, API, max_resp, total, total_lt_1, " \
             "total_1_3, total_3_5, total_gt_5, avg, avg_lt_1, avg_1_3, " \
             "avg_3_5, avg_gt_5\n"
    with open(report_file, 'w') as f:
        f.write(header)

    for hour in range(start_hour, end_hour):
        # Format of agg_dict
        # {"client_id":
        #   {"api_name": {"total": val, "avg": val, "total_lt_1": val, ...},
        #   },
        # }
        # Using default dict to create dictionary here. Which means default
        # value of agg_dict["client_id"]["api_name"][*] = 0.0
        agg_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        log_name = "{}/log_{}.out".format(data_dir, str(hour).zfill(2))
        print("Adding report data for date:{}, hr:{} to {}".format(date_format,
                                                                   hour,
                                                                   report_file)
              )
        out_lines = []
        with open(log_name, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_list = line.split()

                client_id = line_list[0]
                api_name = line_list[1]
                resp_time = int(line_list[2])
                if resp_time > agg_dict[client_id][api_name]["max_resp"]:
                    agg_dict[client_id][api_name]["max_resp"] = resp_time
                agg_dict[client_id][api_name]["resp_sum"] += resp_time
                agg_dict[client_id][api_name]["total"] += 1
                if resp_time <= 1000:
                    agg_dict[client_id][api_name]["resp_sum_lt_1"] += resp_time
                    agg_dict[client_id][api_name]["total_lt_1"] += 1
                elif resp_time > 1000 and resp_time <= 3000:
                    agg_dict[client_id][api_name]["resp_sum_1_3"] += resp_time
                    agg_dict[client_id][api_name]["total_1_3"] += 1
                elif resp_time > 3000 and resp_time <= 5000:
                    agg_dict[client_id][api_name]["resp_sum_3_5"] += resp_time
                    agg_dict[client_id][api_name]["total_3_5"] += 1
                else:
                    agg_dict[client_id][api_name]["resp_sum_gt_5"] += resp_time
                    agg_dict[line_list[0]][api_name]["total_gt_5"] += 1

        for client_id in agg_dict:
            for api_name in agg_dict[client_id]:
                # Using client_api var to shorten line lenght for below code
                # and redability
                client_api = agg_dict[client_id][api_name]
                if client_api["total"] > 0:
                    avg = client_api["resp_sum"] / (client_api["total"] * 1000)
                    avg = round(avg, 2)
                    del agg_dict[client_id][api_name]["resp_sum"]
                else:
                    avg = 0
                if client_api["total_lt_1"] > 0:
                    avg_lt_1 = client_api["resp_sum_lt_1"] /\
                        (client_api["total_lt_1"] * 1000)
                    avg_lt_1 = round(avg_lt_1, 2)
                    del agg_dict[client_id][api_name]["resp_sum_lt_1"]
                else:
                    avg_lt_1 = 0
                if client_api["total_1_3"] > 0:
                    avg_1_3 = client_api["resp_sum_1_3"] /\
                        (client_api["total_1_3"] * 1000)
                    avg_1_3 = round(avg_1_3, 2)
                    del agg_dict[client_id][api_name]["resp_sum_1_3"]
                else:
                    avg_1_3 = 0
                if client_api["total_3_5"] > 0:
                    avg_3_5 = client_api["resp_sum_3_5"] /\
                        (client_api["total_3_5"] * 1000)
                    avg_3_5 = round(avg_3_5, 2)
                    del agg_dict[client_id][api_name]["resp_sum_3_5"]
                else:
                    avg_3_5 = 0
                if client_api["total_gt_5"] > 0:
                    avg_gt_5 = client_api["resp_sum_gt_5"] /\
                        (client_api["total_gt_5"] * 1000)
                    avg_gt_5 = round(avg_gt_5, 2)
                    del agg_dict[client_id][api_name]["resp_sum_gt_5"]
                else:
                    avg_gt_5 = 0
                out_line = "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, " \
                           "{}, {}, {}, {}\n".format(date_format,
                                                     hour,
                                                     client_id,
                                                     api_name,
                                                     client_api["max_resp"],
                                                     client_api["total"],
                                                     client_api["total_lt_1"],
                                                     client_api["total_1_3"],
                                                     client_api["total_3_5"],
                                                     client_api["total_gt_5"],
                                                     avg,
                                                     avg_lt_1,
                                                     avg_1_3,
                                                     avg_3_5,
                                                     avg_gt_5,
                                                     )
                out_lines.append(out_line)
        # Writing per hr of data in one single go rather than one line at a
        # time to save time. (4hrs vs 20secs when writing 180k lines)
        with open(report_file, 'a') as f:
            f.writelines(out_lines)
