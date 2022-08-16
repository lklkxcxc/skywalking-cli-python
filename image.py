#!/usr/bin/env python3
from cProfile import label
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
import time
import requests

url = "http://skywalking.cn/graphql"
end_time = time.time() + time.timezone
start_time = end_time - 900
start_time = time.strftime("%Y-%m-%d %H%M",time.localtime(start_time))
end_time = time.strftime("%Y-%m-%d %H%M", time.localtime(end_time))
start1_time = time.time() - 900
start1_time = time.strftime("%Y-%m-%d %H%M",time.localtime(start1_time))

p_data = {
	"query": "query queryData($condition: MetricsCondition!, $labels: [String!]!, $duration: Duration!) {\n  \n  readLabeledMetricsValues: readLabeledMetricsValues(\n    condition: $condition,\n    labels: $labels,\n    duration: $duration) {\n    label\n    values {\n      values {value}\n    }\n  }}",
	"variables": {
		"duration": {
			"start": start_time,
			"end": end_time,
			"step": "MINUTE"
		},
		"condition": {
			"name": "service_percentile",
			"entity": {
				"scope": "Service",
				"serviceName": "prod-206-commons-backend",
				"normal": "true"
			}
		},
		"labels": ["0", "1", "2", "3", "4"]
	}
}

result = requests.request(method="post",url=url,json=p_data)
label0 = []
label1 = []
label2 = []
label3 = []
label4 = []
for i in result.json()['data']['readLabeledMetricsValues'][0]['values']['values']:
  label0.append(i['value'])
for i in result.json()['data']['readLabeledMetricsValues'][1]['values']['values']:
  label1.append(i['value'])    
for i in result.json()['data']['readLabeledMetricsValues'][2]['values']['values']:
  label2.append(i['value'])
for i in result.json()['data']['readLabeledMetricsValues'][3]['values']['values']:
  label3.append(i['value'])
for i in result.json()['data']['readLabeledMetricsValues'][4]['values']['values']:
  label4.append(i['value'])

dates = pd.date_range(start1_time,periods=16,freq='T')
dic = {'P50':label0,'P75':label1,'P90':label2,'P95':label3,'P99':label4}
df = pd.DataFrame(dic,index=dates)
ax = df.plot()
fig = ax.get_figure()
fig.savefig(r'percentile')


