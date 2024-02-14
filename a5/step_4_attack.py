import json
import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
def attack(ghost_file, crawl_file):
    def get_ack_counts(file, timer):
        f = open(file)
        totals = []
        last_seen = -1000
        packets = json.load(f)
        mapper = {}
        for packet in packets:
            cur_time = float(packet['_source']['layers']['frame']['frame.time_relative'])
            src_port = packet['_source']['layers']['tcp']['tcp.srcport']
            dst_port = packet['_source']['layers']['tcp']['tcp.dstport']
            if cur_time - last_seen > timer:
                total = sum([max(mapper[x]) for x in mapper.keys()])
                totals.append(total)
                mapper = {}
                last_seen = cur_time
            if dst_port == '443'or dst_port == '80':
                ack_size = float(packet['_source']['layers']['tcp']['tcp.ack'])
                cur_port = src_port
                if cur_port in mapper:
                    mapper[cur_port].append(ack_size)
                else:
                    mapper[cur_port] = [ack_size]
            else:
                ack_size = float(packet['_source']['layers']['tcp']['tcp.seq'])
                cur_port = dst_port
                if cur_port in mapper:
                    mapper[cur_port].append(ack_size)
                else:
                    mapper[cur_port] = [ack_size]


        totals.append(sum([max(mapper[x]) for x in mapper.keys()]))
        return totals

    given_counts = get_ack_counts(ghost_file, 5)[1:]
    scrape_counts = get_ack_counts(crawl_file, 7)[1:]


    def build_graph():
        profile = FirefoxProfile()
        profile.set_preference('browser.cache.disk.enable', False)
        profile.set_preference('browser.cache.memory.enable', False)
        profile.set_preference('browser.cache.offline.enable', False)
        profile.set_preference('network.cookie.cookieBehavior', 2)
        browser = webdriver.Firefox(firefox_profile=profile)
        first_page = 'https://computersecurityclass.com/4645316182537493008.html'
        q = []
        visited = set()
        q.append(first_page)
        page_ordering = []
        while len(q) > 0:
            cur_page = q.pop(0)
            browser.get(cur_page)
            cur_elements = browser.find_elements(By.XPATH, "//a[@href]")
            for cur_element in cur_elements:
                url = cur_element.get_attribute("href")
                if url not in visited and url not in q and url != cur_page:
                    q.append(url)
            new_map = {}
            new_map[cur_page] = [x.get_attribute("href") for x in cur_elements]
            visited.add(cur_page)
            page_ordering.append(new_map)
        complete_map = page_ordering[0]
        for sub_map in page_ordering[1:]:
            complete_map.update(sub_map)
        return complete_map

    neighbors = build_graph()

    sites = neighbors.keys()
    ind_to_file = {}
    file_to_ind = {}
    ind = 0

    for line in sites:
        ind_to_file[ind] = line
        file_to_ind[line] = ind
        ind += 1
    visited_list = []
    cur_url = 'https://computersecurityclass.com/4645316182537493008.html'
    i = 2
    for given_count in given_counts[1:]:
        visited_list.append(cur_url)
        totals = []
        for neighbor in neighbors[cur_url]:
            index_of_neighbor = file_to_ind[neighbor]
            scrape_count = scrape_counts[index_of_neighbor]
            totals.append(abs(given_count - scrape_count))
        cur_url = neighbors[cur_url][np.argmin(totals)]
        i+=1

    visited_list.append(cur_url)
    for line in visited_list:
        print(line)
    return visited_list

print(attack('step3result.json', 'step4_my_trace.json'))
