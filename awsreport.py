import json
import time
import plotly.graph_objs as go
import plotly.plotly as py

# Command to get the AWS statistics data.
# aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --start-time 2018-10-01T23:00:00 --end-time 2018-10-26T23:00:00 --period 3600 --statistics Average --dimensions Name=InstanceId,Value=i-071afd3f185b5d7db > jsondata.txt

path = '/home/hguerrero/jsondata.txt'


def parse_data_to_json(file):
    with open(file) as json_data:
        data = json.load(json_data)
    return data


def sort_data_by_time(json_dict):
    json_dict.sort(key=lambda x: time.mktime(time.strptime(x['Timestamp'], '%Y-%m-%dT%H:%M:%SZ')))
    return json_dict


for row in sort_data_by_time(parse_data_to_json(path)['Datapoints']):
    print(row)
