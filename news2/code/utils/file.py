import json

def write_to_csv(data,website,keyword):
    with open('data_%s_%s.json'%(website,keyword),'a+') as file:
        file.write(json.dumps(data))

def load_csv(file):
    with open(file,'r') as f:
        data = json.load(f)
        return data