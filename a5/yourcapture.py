import json


def process(file):
    with open(file) as json_file:
        json_data = json.load(json_file)
    res = []
    for data in json_data:
        temp = {}
        temp["time"] = data['_source']['layers']['frame']['frame.time_relative']
        try:
            temp["ip_add"] = data['_source']['layers']['ip']['ip.src']
        except:
            temp["ip_add"] = None

        temp["src port"] = data['_source']['layers']["tcp"]["tcp.srcport"]
        temp["des port"] = data['_source']['layers']["tcp"]["tcp.dstport"]
        temp["ack"] = data['_source']['layers']["tcp"]["tcp.ack"]
        temp["seq"] = data['_source']['layers']["tcp"]["tcp.seq"]
        temp["fin Flag"] = data['_source']['layers']["tcp"]["tcp.flags_tree"]["tcp.flags.fin"]
        temp["syn flag"] = data['_source']['layers']["tcp"]["tcp.flags_tree"]["tcp.flags.syn"]
        temp["rst flag"] = data['_source']['layers']["tcp"]["tcp.flags_tree"]["tcp.flags.reset"]
        try:
            if data['_source']['layers']["tls"]:
                temp["tls"] = "1"
        except:
            temp["tls"] = "0"

        res.append(temp)

    streamList = []
    for i in range(len(res)):
        tcp = {}
        data = res[i]
        if data["ack"] == "1" and data["seq"] == "1" and not (data["fin Flag"] == "1") and not (data["rst flag"] == "1") and data["tls"] == "1":
            tcp["port 1"] = data["src port"]
            tcp["port 2"] = data["des port"]
            end1 = 0
            end2 = 0
            tsval = 0
            tcp["start"] = data["time"]
            for j in range(i+1, len(res)):
                data2 = res[j]
                if (data2["src port"] == data["src port"] and data2["des port"] == data["des port"]) and (data2["rst flag"] == "1" or data2["fin Flag"] == "1"):
                    tcp["port 1 to port 2"] = data2["seq"]
                    end1 = data2["time"]
            for k in range(i+1, len(res)):
                data2 = res[k]
                if data2["src port"] == data["des port"] and data2["des port"] == data["src port"] and (data2["rst flag"] == "1" or data2["fin Flag"] == "1"):
                    tcp["port 2 to port 1"] = data2["seq"]
                    end2 = data2["time"]
            tcp["end"] = max(end1, end2)
            tcp["total size"] = int(tcp["port 2 to port 1"]) + \
                int(tcp["port 1 to port 2"])
            tcp["tsval"] = tsval
            streamList.append(tcp)

    tcpList = []

    for i in range(len(streamList)):
        tcp = {}
        streams = []
        tsval = streamList[i]["tsval"]
        streams.append(streamList[i])
        for j in range(i+1, len(streamList)):
            if streamList[j]["tsval"] == tsval:
                streams.append(streamList[j])
        tcp["TCP Connection"] = streams
        tcpList.append(tcp)
    with open('yourlink3.json', 'w') as f:
        json.dump(streamList, f, indent=2)
    return tcpList


process("link3.json")
