from collections import defaultdict
import os
# file: {mm}{dd}{yyyy}
# line: hour Client_id API total_API_req's avg_resp (all, 0-5s, 5s-10s, > 10s)
# Date hr client_id API max_time count avg (all, lt_1, 1_3, 3_5, gt_5)
home = os.environ['HOME']
data_path = "{}/Documents/myprojects/access_logs_sla/gen_test_data/data/".format(home)

# format = {"client_id":
#             {"api_name": {"total": "int", "avg": "int", "total_lt_1": "int", "avg_lt_1": "int"},
#              },
# }


for day in range(20, 23):
    log_dir = "{}/Documents/myprojects/access_logs_sla/gen_test_data/data/06{}2020".format(home, day)
    out_file = "{}/Documents/myprojects/access_logs_sla/output/06{}2020.csv".format(home, day)
    try:
        os.makedirs("{}/Documents/myprojects/access_logs_sla/output".format(home))
    except OSError as e:
        print("Dir creation Exception: {}".format(e))
    with open(out_file, 'w') as f:
        f.write("Date, Hour, client_ID, API, max_resp, total, total_lt_1, total_1_3, total_3_5, total_gt_5, avg, avg_lt_1, avg_1_3, avg_3_5, avg_gt_5\n")

    for hour in range(0, 24):
        agg_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        log_name = "{}/log_{}.out".format(log_dir, hour)
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
                if agg_dict[client_id][api_name]["total"] > 0:
                    agg_dict[client_id][api_name]["avg"] = float(agg_dict[client_id][api_name]["resp_sum"] / (agg_dict[client_id][api_name]["total"] * 1000))
                    agg_dict[client_id][api_name]["avg"] = round(agg_dict[client_id][api_name]["avg"], 2)
                    del agg_dict[client_id][api_name]["resp_sum"]
                else:
                    agg_dict[client_id][api_name]["avg"] = 0
                if agg_dict[client_id][api_name]["total_lt_1"] > 0:
                    agg_dict[client_id][api_name]["avg_lt_1"] = agg_dict[client_id][api_name]["resp_sum_lt_1"] / (agg_dict[client_id][api_name]["total_lt_1"] * 1000)
                    agg_dict[client_id][api_name]["avg_lt_1"] = round(agg_dict[client_id][api_name]["avg_lt_1"], 2)
                    del agg_dict[client_id][api_name]["resp_sum_lt_1"]
                else:
                    agg_dict[client_id][api_name]["avg_lt_1"] = 0
                if agg_dict[client_id][api_name]["total_1_3"] > 0:
                    agg_dict[client_id][api_name]["avg_1_3"] = agg_dict[client_id][api_name]["resp_sum_1_3"] / (agg_dict[client_id][api_name]["total_1_3"] * 1000)
                    agg_dict[client_id][api_name]["avg_1_3"] = round(agg_dict[client_id][api_name]["avg_1_3"], 2)
                    del agg_dict[client_id][api_name]["resp_sum_1_3"]
                else:
                    agg_dict[client_id][api_name]["avg_1_3"] = 0
                if agg_dict[client_id][api_name]["total_3_5"] > 0:
                    agg_dict[client_id][api_name]["avg_3_5"] = agg_dict[client_id][api_name]["resp_sum_3_5"] / (agg_dict[client_id][api_name]["total_3_5"] * 1000)
                    agg_dict[client_id][api_name]["avg_3_5"] = round(agg_dict[client_id][api_name]["avg_3_5"], 2)
                    del agg_dict[client_id][api_name]["resp_sum_3_5"]
                else:
                    agg_dict[client_id][api_name]["avg_3_5"] = 0
                if agg_dict[client_id][api_name]["total_gt_5"] > 0:
                    agg_dict[client_id][api_name]["avg_gt_5"] = agg_dict[client_id][api_name]["resp_sum_gt_5"] / (agg_dict[client_id][api_name]["total_gt_5"] * 1000)
                    agg_dict[client_id][api_name]["avg_gt_5"] = round(agg_dict[client_id][api_name]["avg_gt_5"], 2)
                    del agg_dict[client_id][api_name]["resp_sum_gt_5"]
                else:
                    agg_dict[client_id][api_name]["avg_gt_5"] = 0
                out_line = "06{}2020, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(day,
                                                                                                       hour,
                                                                                                       client_id,
                                                                                                       api_name,
                                                                                                       agg_dict[client_id][api_name]["max_resp"],
                                                                                                       agg_dict[client_id][api_name]["total"],
                                                                                                       agg_dict[client_id][api_name]["total_lt_1"],
                                                                                                       agg_dict[client_id][api_name]["total_1_3"],
                                                                                                       agg_dict[client_id][api_name]["total_3_5"],
                                                                                                       agg_dict[client_id][api_name]["total_gt_5"],
                                                                                                       agg_dict[client_id][api_name]["avg"],
                                                                                                       agg_dict[client_id][api_name]["avg_lt_1"],
                                                                                                       agg_dict[client_id][api_name]["avg_1_3"],
                                                                                                       agg_dict[client_id][api_name]["avg_3_5"],
                                                                                                       agg_dict[client_id][api_name]["avg_gt_5"],
                                                                                                       )
                out_lines.append(out_line)
        # Writing per hr of data in one single go rather than one line
        # at a time to save time. (4hrs vs 20secs)
        with open(out_file, 'a') as f:
            f.writelines(out_lines)
