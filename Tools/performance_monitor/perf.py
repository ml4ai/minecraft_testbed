import time
import docker
import sys
import os

client = docker.from_env()
containers = client.containers.list(all=True)
print(containers)
encoding = 'utf-8'

# get performance data
def get_perf_data(stats):
    perf_data = {}
    perf_data["read_time"] = stats["read"]
    perf_data["name"] = stats["name"][1:]
    perf_data["pids_stats"] = stats["pids_stats"]["current"] if "current" in stats["pids_stats"] else 0
    perf_data["cpu_stats_total_usage"] = stats["cpu_stats"]["cpu_usage"]["total_usage"]
    perf_data["system_cpu_usage"] = stats["cpu_stats"]["system_cpu_usage"] if "system_cpu_usage" in stats["cpu_stats"] else 0
    perf_data["memory_stats_usage"] = stats["memory_stats"]["usage"] if "usage" in stats["memory_stats"] else 0
    if "stats" in stats["memory_stats"]:
        perf_data["total_mapped_file"] = stats["memory_stats"]["stats"]["total_mapped_file"]
        perf_data["total_rss"] = stats["memory_stats"]["stats"]["total_rss"]
    else:
        perf_data["total_mapped_file"] = 0
        perf_data["total_rss"] = 0
    perf_data["memory_stats_max"] = stats["memory_stats"]["max_usage"] if "max_usage" in stats["memory_stats"] else 0
    perf_data["blkio_read"] = next((x for x in stats["blkio_stats"]["io_service_bytes_recursive"] if x["op"] == "Read"), None) \
                                if "io_service_types_recursive" in stats["blkio_stats"] else 0
    perf_data["blkio_write"] = next((x for x in stats["blkio_stats"]["io_service_bytes_recursive"] if x["op"] == "Write"), None) \
                                if "io_service_types_recursive" in stats["blkio_stats"] else 0
    return perf_data

f = open("perf_monitor.csv", "w")
f.write("index,read_time,name,pids_stats,cpu_stats_total_usage,system_cpu_usage,memory_stats_usage,total_mapped_file,total_rss,memory_stats_max,blkio_read,blkio_write\n")

# collect n points of data
time_points = 100
for x in range(time_points):
    for c in containers:
        #print(c.attrs['Id'] + " : " + c.attrs['Name'][1:])
        stats_dict = get_perf_data(c.stats(stream=False))
        f.write(str(x)+","+str(stats_dict["read_time"])+","+ \
        str(stats_dict["name"])+","+ \
        str(stats_dict["pids_stats"])+","+ \
        str(stats_dict["cpu_stats_total_usage"])+","+ \
        str(stats_dict["system_cpu_usage"])+","+ \
        str(stats_dict["memory_stats_usage"])+","+ \
        str(stats_dict["total_mapped_file"])+","+ \
        str(stats_dict["total_rss"])+","+ \
        str(stats_dict["memory_stats_max"])+","+ \
        str(stats_dict["blkio_read"])+","+ \
        str(stats_dict["blkio_write"]))
        f.write("\n")
        #container = client.containers.get(c.attrs['Id'])

    time.sleep(10)
f.close()


