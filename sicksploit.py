import requests


def test_req(conf):
    url = "http://192.168.1.105:8081/config/postProcessing/savePostProcessing"
    current_dir = conf['tv_download_dir']
    current_extensions = conf['allowed_extensions']
    keys = {
            'allowed_extensions': '',
            'alt_unrar_tool': 'unrar',
            'autopostprocessor_frequency': '11',
            'delete_non_associated_files': 'on',
            'extra_scripts': '/usr/bin/wget ',
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
            'tv_download_dir': '',
            'unpack': '0',
            'unpack_dir': '',
            'unrar_tool': 'unrar',
            'use_icacls': 'on',
            'wdtv_data': '0|0|0|0|0|0|0|0|0|0'
            }
    response = requests.post(url, data=keys)
    print response.status_code


def get_current_conf():
    url = "http://192.168.1.105:8081/config/postProcessing/"
    keys = {'allowed_extensions': '', 'tv_download_dir': ''}
    response = requests.get(url)
    text = response.content
    for line in text.split("\n"):
        for k in keys:
            if k in line:
                items = line.split(" ")
                for i in items:
                    if "value" in i:
                        conf_item = i.split("=")[1].lstrip("\"").rstrip("\"")
                        keys[k] = conf_item
    print keys


get_current_conf()


