import json
import time
import plotly.graph_objs as go
import plotly.offline as py
from plotly import tools

# Command to get the AWS statistics data.
# aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --start-time 2018-10-01T23:00:00 --end-time 2018-10-26T23:00:00 --period 3600 --statistics Maximum --dimensions Name=InstanceId,Value=i-071afd3f185b5d7db > jsondatacpu.txt
# aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name NetworkIn, --start-time 2018-10-01T23:00:00 --end-time 2018-10-30T23:00:00 --period 3600 --statistics Average --dimensions Name=InstanceId,Value=i-071afd3f185b5d7db > jsondatanetin.txt
# aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name NetworkOut --start-time 2018-10-01T23:00:00 --end-time 2018-10-30T23:00:00 --period 3600 --statistics Average --dimensions Name=InstanceId,Value=i-071afd3f185b5d7db > jsondatanetout.txt

base_path = '/home/hguerrero/'

paths = [base_path+'jsondatanetin.txt', base_path+'jsondatanetout.txt', base_path+'jsondatacpu.txt']

instance_name = ''
client = ''

def parse_data_to_json(file):
    with open(file) as json_data:
        data = json.load(json_data)
    return data


def sort_data_by_time(json_dict):
    json_dict.sort(key=lambda x: time.mktime(time.strptime(x['Timestamp'], '%Y-%m-%dT%H:%M:%SZ')))
    return json_dict


cpu = []
ctime = []
netin = []
nitime = []
netout = []
notime = []
count = 0

for path in paths:
    for row in sort_data_by_time(parse_data_to_json(path)['Datapoints']):
        if count == 0:
            netin.append(row['Average'])
            nitime.append(row['Timestamp'])
        elif count == 1:
            netout.append(row['Average'])
            notime.append(row['Timestamp'])
        else:
            cpu.append(row['Maximum'])
            ctime.append(row['Timestamp'])
    count = count+1

#####
# Network Utilization Chart
#####

print(netin, nitime, '\n')

print(netout, notime, '\n')

trace_net_in = go.Scatter(

    x=nitime,
    y=netin,
    name='Network-In'
)

trace_net_out = go.Scatter(

    x=notime,
    y=netout,
    name='Network-Out'
)

# net_layout = go.Layout(title="<b>Window's Server 2016</b> <br> Network Utilization")
# net_data = [trace_net_in, trace_net_out]

# py.offline.plot({"data": data, "layout": layout}, auto_open=False, filename='envases-chart-net-report.html')
# net_chart = py.plot({"data": data, "layout": layout})

#####
# CPU Utilization Chart
#####
print(cpu, ctime, '\n')

trace_cpu = go.Scatter(
    x=ctime,
    y=cpu,
    name='CPU-Percentage'
)

# cpu_layout = go.Layout(title="<b>Window's Server 2016</b> <br> CPU Utilization")
# cpu_layout = dict(
#     title="<b>Window's Server 2016</b> <br> CPU Utilization"
# )

# cpu_chart = py.plot({"data": data, "layout": layout})

chart_report = tools.make_subplots(rows=2, cols=2, specs=[[{}, {}], [{'colspan': 2}, None]],
                                   subplot_titles=('Network In', 'Network Out', 'CPU Utilization'))
chart_report.append_trace(trace_net_in, 1, 1)
chart_report.append_trace(trace_net_out, 1, 2)
chart_report.append_trace(trace_cpu, 2, 1)

chart_report['layout'].update(showlegend=True, title="Window's Server 2016 Resource Report")

py.plot(chart_report, filename='enavases-report.html')
