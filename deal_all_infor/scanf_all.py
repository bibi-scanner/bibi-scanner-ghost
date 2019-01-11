#coding=utf-8
# from deal_all_infor.ip_to_port import scanf_ip_port
# from deal_json.store import store_infor
from ip_deal.scanf_class import getIPsFromRange
from ip_deal.ping_func import ping_ip
from concurrent.futures import ThreadPoolExecutor
from port_deal.test_port import checkPort
# from port_deal.port_detail import checkWarn
from deal_json.store import store_ip_port
import threading
import importlib
# from script.redis_unauth import redis_unauth
import  time

class scanTask():
    def __init__(self, id, ips_all, start_port, end_port, plugins):
        self.id = id
        self.ips_all = ips_all
        self.start_port = start_port
        self.end_port = end_port

        self.ips = []

        self.progress = 0
        self.lock = threading.Lock()
        self.scanHostCount = 0
        self.scanOverHostCount = 0
        self.scanPortCount = 0
        self.scanOverPortCount = 0
        self.scanWarnCount = 0
        self.scanWarnOverCount = 0
        self.result = ScanResult().add_ip()
        self.plugins = plugins


    def checkHosts(self):
        ips = getIPsFromRange(self.ips_all)
        self.scanHostCount = len(ips)
        self.scanOverHostCount = 0
        list_Host = []
        with ThreadPoolExecutor(50) as executor1:
            result_list = executor1.map(self.pingIP, ips)
            for result in result_list:
               if(result["result"]):
                    self.result["numberOfHosts"] = self.result["numberOfHosts"] + 1
                    result_Host = HostResult(result["ip"])

                    list_Host.append(result_Host.add_Host())
                    self.result["hosts"] = list_Host
                    # result_Host.add_Host()

    def pingIP(self, ip):
        result = ping_ip(ip)
        self.lock.acquire()
        self.scanOverHostCount = self.scanOverHostCount + 1
        self.progress = self.scanOverHostCount / self.scanHostCount * 0.33 + 0
        self.lock.release()
        # print(str(self.progress))
        return {
            "ip": ip,
            "result": result
        }

    def getNeedScanURLs(self):
        hosts = self.result["hosts"]
        urls = []
        startPorts = self.start_port
        endPorts = self.end_port
        for host in hosts:
            for i in range(startPorts, endPorts + 1):
                urls.append({
                    "ip": host["host"],
                    "port": i
                })
        return urls

    #检查接口
    def checkPorts(self):
        urls = self.getNeedScanURLs()
        self.scanPortCount = len(urls)
        self.scanOverPortCount = 0
        list_hosts_tmp = self.result["hosts"]
        index = 0

        with ThreadPoolExecutor(8000) as executor1:
            result_list = executor1.map(self.pingPort, urls)
            for result in result_list:
                if (result["result"]):
                    self.result["numberOfPorts"] = self.result["numberOfPorts"] + 1
                    for dic_host_tmp in list_hosts_tmp:
                        if(dic_host_tmp["host"] == result["ip"]):
                            list_port_tmp= dic_host_tmp["ports"]
                            dic_host_tmp["numberOfPorts"] = dic_host_tmp["numberOfPorts"] + 1
                            result_port = PortResult(result["port"])
                            list_poty_tmp = dic_host_tmp["ports"]
                            list_port_tmp.append(result_port.add_Port())
                            dic_host_tmp["ports"] = list_port_tmp
                            break

    def pingPort(self, ipport):
        result = checkPort(ipport["ip"], ipport["port"])
        self.lock.acquire()
        self.scanOverPortCount = self.scanOverPortCount + 1
        self.progress = self.scanOverPortCount / self.scanPortCount * 0.33 + 0.33
        self.lock.release()
        print(str(self.progress))
        return {
            "ip": ipport["ip"],
            "port": ipport["port"],
            "result": result
        }

    def scanNeedPortURLs(self):
        hosts = self.result["hosts"]
        URLs = []
        for host in hosts:
            for port in host["ports"]:
                URLs.append({
                    "ip": host["host"],
                    "port": port["port"]
                })
        return URLs

    def checkWarns(self):
        urls = self.scanNeedPortURLs()
        self.scanWarnCount = len(urls)
        self.scanOverWarnCount = 0
        dict_host_warn = self.result

        with ThreadPoolExecutor(30) as executor1:
            result_list = executor1.map(self.pingWarn, urls)
            for result in result_list:
                if(result!=None):
                    dict_host_warn["numberOfWarnings"] = dict_host_warn["numberOfWarnings"] + 1
                    for host in dict_host_warn["hosts"]:
                        if(result["ip"]==host["host"]):
                            host["numberOfWarnings"] = host["numberOfWarnings"] + 1
                            for port in host["ports"]:
                                list_warn_tmp = port["warnings"]
                                if(port["port"]==result["port"]):
                                    list_warn_tmp = port["warnings"]
                                    list_warn_tmp.append(WarnResult(result["description"], result["plugin"]).add_Warn())
                                    port["warnings"] = list_warn_tmp
                                    port["numberOfWarnings"] = port["numberOfWarnings"] + 1
                else:
                    continue

    def pingWarn(self,ipport):
        for i in self.plugins:
            model = importlib.import_module("plugins."+i)
            result = model.poc(ipport["ip"], ipport["port"])
            self.lock.acquire()
            self.scanWarnOverCount = self.scanWarnOverCount + 1
            self.progress = self.scanWarnOverCount / self.scanWarnCount * 0.33 + 0.66
            # print(str(self.progress))
            self.lock.release()
            if(result["result"]):
                return {
                    "ip": ipport["ip"],
                    "port": ipport["port"],
                    "description": result["info"],
                    "plugin": i
            }
            else:
                return None

    def run(self):
        self.checkHosts()
        self.checkPorts()
        self.checkWarns()
        self.progress = 1
        print(str(self.progress))
        store_ip_port(self.result)
        self.end()

    def end(self):
        print("do no thing")

    # def scanf_part(self):
    #     """
    #     把得到的结果进行整理输出成json文件
    #     :return: json文件
    #     """
    #     scanf_all_hosts = scanf_ip_port(self.ips_all, self.start_port, self.end_port)
    #     dict_host_all = scanf_all_hosts.ports_live()
    #     infor_json = store_infor(dict_host_all)
    #     infor_json.store_ip_port()


class ScanResult():

    def __init__(self):
        self.numberOfHosts = 0
        self.numberOfPorts = 0
        self.numberOfWarnings = 0
        self.hosts = []

    def add_ip(self):
        dict_scanf = {}
        dict_scanf["numberOfHosts"] = self.numberOfHosts
        dict_scanf["numberOfPorts"] = self.numberOfPorts
        dict_scanf["numberOfWarnings"] = self.numberOfWarnings
        dict_scanf["hosts"] = self.hosts
        return dict_scanf


class HostResult():

    def __init__(self, ip):
        self.host = ip
        self.numberOfPorts = 0
        self.numberOfWarnings = 0
        self.ports = []

    def add_Host(self):
        dict_Host={}
        dict_Host["host"] = self.host
        dict_Host["numberOfPorts"] = self.numberOfPorts
        dict_Host["numberOfWarnings"] = self.numberOfWarnings
        dict_Host["ports"] = self.ports
        return dict_Host

class PortResult():

    def __init__(self, port):
        self.port = port
        self.numberOfWarnings = 0
        self.warnings = []

    def add_Port(self):
        dict_port = {}
        dict_port["port"] = self.port
        dict_port["numberOfWarnings"] = self.numberOfWarnings
        dict_port["warnings"] = self.warnings
        return dict_port

class WarnResult():
    def __init__(self, description, plugin):
        self.description = description
        self.plugin = plugin

    def add_Warn(self):
        dict_Warn = {}
        dict_Warn["description"] = self.description
        dict_Warn["plugin"] = self.plugin
        return dict_Warn



if __name__ == "__main__":
    task = scanTask("123", "10.10.9.233", 0, 10000, [])
    print("start:   " + str(time.time()))
    task.run()
    print("end:   " + str(time.time()))