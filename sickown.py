from shodan import Shodan
import requests
import Queue
import threading
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Use Shodan.io to track down vulnerable instances of SickChill/Rage")
    parser.add_argument('API_KEY', metavar="API", help="The API_KEY for Shodan")
    args = parser.parse_args()
    return args


def find_targets(api):
    print "[+] Looking for targets using Shodan API."
    query = "Server: TornadoServer and Location: /home"
    print "[+] Query = %s" % query
    targets = Queue.Queue()
    for host in api.search_cursor(query):
        targets.put({'ip': host['ip_str'], 'port': host['port']})
    return targets


def test_targets(target_queue, result_list):
    while not target_queue.empty():
        target = target_queue.get()
        if check_target(target):
            result_list.append(target)


def check_target(target, outfile):
    url = "http://%s:%s/config/postProcessing/" % (target['ip'], target['port'])
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print "[-] Request failed. http://%s:%s seems down." % (target['ip'], target['port'])
            return False
        else:
            print "[+] Request succeeded. http://%s:%s is up." % (target['ip'], target['port'])
            with open(outfile, "wa") as fp:
                fp.write("%s:%s\n" % (target['ip'], target['port']))
            fp.close()
            return True
    except requests.exceptions.ConnectionError:
        print "[-] Request failed. http://%s:%s seems down." % (target['ip'], target['port'])
        return False




def main():
    # Get arguments - shodan API
    args = get_args()
    api = Shodan(args.API_KEY)
    # Query shodan and find targets
    raw_targets = find_targets(api)
    print "[+] Found %s targets." % raw_targets.qsize()
    # Now let's query post processing configuration to remove false positives.
    verified_targets = []
    threads = 10
    for i in range(threads):
        t = threading.Thread(target=test_targets(raw_targets, verified_targets))
        t.start()
    print "[+] Verification finished. Verified %s targets." % len(verified_targets)


if __name__ == '__main__':
    main()