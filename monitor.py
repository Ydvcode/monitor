from flask import Flask, jsonify
import platform
import psutil
import datetime

app = Flask(__name__, template_folder='template')


@app.route('/')
def sys_info():
    return ' Welcome to Basic Information'


@app.route('/basic')
def basic_info():
    my_system = platform.uname()
    system = {"System": my_system.system, "Model Name": my_system.node, "Release": my_system.release,
              "Version": my_system.version, "Machine": my_system.machine, "Processor": my_system.processor}

    return system


@app.route('/user')
def user_name():
    user_info = psutil.users()
    user = {"Name": []}
    for value in user_info:
        user["Name"] = value[0]

    return user


@app.route('/cpu')
def cpu_info():
    core = psutil.cpu_count()
    cpu_time = psutil.cpu_times()
    user_time = cpu_time.user / 3600
    system = cpu_time.system / 3600
    idle = cpu_time.idle / 3600
    utilization = psutil.cpu_percent(interval=1, percpu=1)
    cpu_inn = jsonify(
        {"Total Cores in System": core, "Time spent by the user": user_time, "Time spent by the system": system,
         "Idle Time": idle, "The Utilization of each CPU": utilization})

    return cpu_inn


@app.route('/ram')
def ram_info():
    ram_memory = psutil.virtual_memory()
    ram_info = {
        "Total Ram": round((ram_memory.total / 1000000000), 2),
        "Free Ram ": round((ram_memory.free / 1000000000), 2),
        "Used Ram ": round((ram_memory.free / 1000000000), 2)}

    return ram_info


@app.route('/battery')
def battery_info():
    battery_info = dict(psutil.sensors_battery()._asdict())

    return battery_info


@app.route('/boot')
def boot_time():
    boot = {'Boot Date & Time:': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}

    return boot


@app.route('/network')
def net_info():
    net_inf = psutil.net_io_counters(pernic=1, nowrap=1)

    return net_inf


if __name__ == '__main__':
    app.run(debug=True)
