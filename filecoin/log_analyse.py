import json
import time
from collections import OrderedDict
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def parse_ts(ts: str) -> float:
    ts = ts.split(".")
    return time.mktime(time.strptime(ts[0], "%Y-%m-%dT%H:%M:%S")) + float("0." + ts[1][0:3])


def sec2str(sec: float) -> str:
    if sec > 3600:
        return "{:.2f} h".format(sec / 3600)
    if sec > 60:
        return "{:.2f} min".format(sec / 60)
    else:
        return "{:.3f} s".format(sec)


def show(data: list, title=""):
    if not data:
        return
    if np.min(data) > 1800:
        arr = np.array([x/3600 for x in data])
        plt.xlabel("duration(hour)")
    elif np.min(data) > 30:
        arr = np.array([x/60 for x in data])
        plt.xlabel("duration(min)")
    else:
        arr = np.array(data)
        plt.xlabel("duration(second)")

    (counts, bins, patch) = plt.hist(x=arr, bins=25, edgecolor='k')
    for i, c in enumerate(counts):
        plt.text(bins[i], c, str(int(c)))

    plt.title(title)
    plt.ylabel("count")
    plt.show()


def analyse_miner_log(path: str, ignores: list, ts_filer: dict, start_from: float = None):
    data = OrderedDict()
    start = 0.0
    end = 0.0
    with open(path, 'r') as f:
        tmp = {}
        for line in f:
            try:
                log = json.loads(line)
                sector = log.get("sectorNumber", None)
                if not sector:
                    continue
                task_type = log.get('taskType', '').replace('seal/v0/', '')
                if task_type in ignores:
                    continue
                ts = parse_ts(log.get('ts'))
                if int(ts) < int(start_from):
                    continue
                if start < 1:
                    start = ts
                end = ts

                worker = log.get("worker")
                log_type = log.get('type')

                if log_type == 'run task start':
                    if sector not in tmp:
                        tmp[sector] = {}
                    tmp[sector][task_type] = ts
                    continue

                if log_type == 'run task end':
                    duration = ts - tmp[sector][task_type]
                    if task_type in ts_filer:
                        if ts_filer[task_type](duration):
                            continue
                    if sector not in data:
                        data[sector] = OrderedDict()
                    data[sector][task_type] = (duration, worker)
                    continue

            except BaseException as e:
                continue

    stat = OrderedDict()
    stat["precommit/1"] = []
    stat["precommit/2"] = []
    stat["commit/1"] = []
    stat["commit/2"] = []
    for sector, v in data.items():
        for task_type, vv in v.items():
            duration, worker = vv
            if task_type not in stat:
                stat[task_type] = []
            stat[task_type].append(duration)
            data[sector][task_type] = f"{sec2str(duration)} @ {worker}"

    avg_sector_duration = 0.0
    for task_type, durations in stat.items():
        if not durations:
            continue
        show(durations, task_type)
        d = sum(durations) / len(durations)
        avg_sector_duration += d
        print(f"{task_type} count: {len(durations)}   avg: {sec2str(d)}")
    print(f"avg sector duration : {sec2str(avg_sector_duration)}")

    # 日志的这段时间内，大概挖出了多少个sector
    # num_sectors = 0.0
    # for task_type, durations in stat.items():
    #     num_sectors += len(durations)
    # num_sectors /= len(stat.keys())

    # 日志的这段时间内，大概挖出了多少个sector
    num_sectors = 0.0
    for task_type, durations in stat.items():
        if not durations:
            continue
        d = sum(durations) / len(durations)
        num_sectors += len(durations) * (d / avg_sector_duration)

    print(f"\nlog analyse duration {sec2str((end-start))}, num_sectors {num_sectors}")
    print("该集群日产出约为: {:.2f} T".format(num_sectors * 32 * (24*3600) / (end-start) / 1024))

    print("\ndetails:")
    print(json.dumps(data, indent='\t'))


def analyse_worker_log(path: str):
    data = OrderedDict()
    start = 0.0
    end = 0.0
    with open(path, 'r') as f:
        tmp = {}
        for line in f:
            try:
                pass
            except BaseException:
                continue
    print("\ndetails:")
    print(json.dumps(data, indent='\t'))


if __name__ == '__main__':
    # 符合 filter 的数据会被剔除掉
    ts_filer = {
        "precommit/1": lambda s: s < 60 * 60,
        "commit/1": lambda s: s > 6 * 60,
        "commit/2": lambda s: s > 15 * 60
    }
    analyse_miner_log("miner_001.log",
                      ignores=['addpiece', 'deal', 'unseal', 'fetch', 'finalize'],
                      ts_filer=ts_filer,
                      start_from=parse_ts('2020-08-08T00:00:00.000'))
    # analyse_worker_log("/Users/apple/Desktop/worker.172.18.23.66.log")


