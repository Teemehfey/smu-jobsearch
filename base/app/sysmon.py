from flask import Flask
from collections import namedtuple
import json, requests, socket, os
from flask import render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from app import app
import psutil as pu
import daemon

cpuTuple = namedtuple('cpuTuple', 'core, used')
memTuple = namedtuple('memTuple', 'total, used')
diskPartTuple = namedtuple('diskPartTuple', 'device, mountpoint, fstype, total, percent')
networkTuple = namedtuple('networkTuple', 'device, sent, recv, pkg_sent, pkg_recv')
processTuple = namedtuple('processTuple', 'pid, name, status, user, memory')

def bytes2human(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')

@app.route('/sysmon/cpu/json')
def get_cpu_info():
    cpu_info = cpuTuple(core=pu.cpu_count(), used=pu.cpu_percent())
    return json.dumps(cpu_info._asdict())

@app.route('/sysmon/memory/json')
def get_memory_info():
    mem_info = memTuple(total=bytes2human(pu.virtual_memory().total), used=pu.virtual_memory().percent)
    return json.dumps(mem_info._asdict())

@app.route('/sysmon/partition/json')
def get_partition_info():
    partitions = list()
    for part in pu.disk_partitions():
        partitions.append(diskPartTuple(
                    device=part.device,
                    mountpoint=part.mountpoint,
                    fstype=part.fstype,
                    total=bytes2human(
                        pu.disk_usage(part.mountpoint).total),
                    percent=pu.disk_usage(part.mountpoint).percent))
    return json.dumps(partitions)

@app.route('/sysmon/network/json')
def get_networks_info():
    networks = list()
    for k, v in pu.net_io_counters(pernic=True).items():
        if k == 'lo': continue
        networks.append(networkTuple(
                    device=k,
                    sent=bytes2human(v.bytes_sent),
                    recv=bytes2human(v.bytes_recv),
                    pkg_sent=v.packets_sent,
                    pkg_recv=v.packets_recv))

    # print(networks)
    return json.dumps(networks)

@app.route('/sysmon/process/json')
def get_process_info():
    processes = list()
    for process in pu.process_iter():
        # print(process)
        try:
            percent = process.memory_percent()
            # print(percent)
        except AccessDenied:
            percent = "Access Denied"
        else:
            percent = int(percent)
        if percent > -1:
            processes.append(processTuple(
                    pid=process.pid,
                    name=process.name(),
                    status=process.status(),
                    user=process.username(),
                    memory=percent))

    processes_sorted = sorted( processes, key=lambda p: p.memory, reverse=True)
    # print(processes_sorted)
    return json.dumps(processes_sorted)

@app.route('/sysmon')
def sysmon_dashboard():
    return render_template('sysmon_dashboard.html')


@app.route('/serverstatus',methods=['GET','POST'])
def serverstatus():
    return 'OK'
