from shodan import Shodan
import requests
try:
    import queue
except ImportError:
    import Queue as queue
import threading
import argparse
import json


def get_args():
    parser = argparse.ArgumentParser(description="Use Shodan.io to track down vulnerable instances of SickChill/Rage")
    parser.add_argument('API_KEY', metavar="API", help="The API_KEY for Shodan")
    parser.add_argument('-t', '--timeout', metavar="TIMEOUT", nargs=1, help="The timeout to use for the HTTP requests "
                                                                            "to the targets found", default=10)
    args = parser.parse_args()
    return args


def get_targets():
    targets = queue.Queue()
    with open("shodan_data.json") as fp:
        data = fp.readlines()
        for row in data:
            host = json.loads(row)
            targets.put({'ip': host['ip_str'], 'port': host['port']})
    return targets


def search_targets(api):
    print("[+] Looking for targets using Shodan API.")
    query = "Server: TornadoServer and Location: /home"
    print("[+] Query = %s" % query)
    targets = queue.Queue()
    total = api.search(query)['total']
    pages = total/100 + 1
    for i in range(1, int(pages)):
        search_result = api.search(query, page=i)
        print("[+] Querying results for page %s" % i)
        for host in search_result['matches']:
            targets.put({'ip': host['ip_str'], 'port': host['port']})
    return targets


def find_targets(api):
    print("[+] Looking for targets using Shodan API.")
    query = "Server: TornadoServer and Location: /home"
    print("[+] Query = %s" % query)
    targets = queue.Queue()
    dict = api.search(query)
    print("[+] Found %s targets." % dict['total'])
    for host in api.search_cursor(query):
        targets.put({'ip': host['ip_str'], 'port': host['port']})
    return targets


def test_targets(target_queue, result_list, req_timeout):
    while not target_queue.empty():
        target = target_queue.get()
        if check_target(target, "sicklist.txt", req_timeout):
            result_list.append(target)


def check_target(target, outfile, req_timeout):
    url = "http://%s:%s/config/postProcessing/" % (target['ip'], target['port'])
    try:
        response = requests.get(url, timeout=req_timeout)
        if response.status_code != 200:
            print("[-] Request failed. http://%s:%s seems down." % (target['ip'], target['port']))
            return False
        else:
            print("[+] Request succeeded. http://%s:%s is up." % (target['ip'], target['port']))
            with open(outfile, "a") as fp:
                fp.write("%s:%s\n" % (target['ip'], target['port']))
            fp.close()
            return True
    except requests.exceptions.ConnectionError:
        print("[-] Request failed. http://%s:%s seems down." % (target['ip'], target['port']))
        return False
    except requests.exceptions.Timeout:
        print("[-] Request failed. http://%s:%s seems down." % (target['ip'], target['port']))
        return False


def main():
    # Get arguments - shodan API
    args = get_args()
    api = Shodan(args.API_KEY)
    timeout = float(args.timeout[0])
    # Query shodan and find targets
    raw_targets = search_targets(api)
    # raw_targets = get_targets()
    print("[+] Found %s targets." % raw_targets.qsize())
    # Now let's query post processing configuration to remove false positives.
    verified_targets = []
    threads = 10
    for i in range(threads):
        t = threading.Thread(target=test_targets(raw_targets, verified_targets, timeout))
        t.start()
    print("[+] Verification finished. Verified %s targets." % len(verified_targets))


if __name__ == '__main__':
    main()
