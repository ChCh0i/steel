<img width="567" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/fbc63c5f-3ad2-431c-b0ff-1444fbe29da9"># wifinetic
![js](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

<img width="1470" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/ed2e98e7-d808-4c7d-abfb-772d7cc5b3e1">

## 개요 
 - hackthebox machin문제인 wifinetic 문제 wirte up 입니다.
 - user까지 접근하는데 조금 의아했던게 권한상승을 배우는 목적으로 풀어보는 문제인데 passwd파일을 제공해주고 config값을 준다는게 의아?했던 문제입니다.
 - 문제를 해결하는데있어서 네트워크를 구성하는 linux기본 베이스가 있어야하고
 - 어떤식으로 root에 접근하는지 갈피도 잡기힘든 문제였지만 문제제목을보고 힌트를 얻었습니다.

## scan
```
┌[choejun-won@choejuncBookAir] [/dev/ttys000] 
└[~/Downloads/etc]> nmap -sC -sT -sV -Pn 10.10.11.247
Starting Nmap 7.94 ( https://nmap.org ) at 2024-01-25 13:42 KST
Stats: 0:00:54 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 77.18% done; ETC: 13:43 (0:00:16 remaining)
Stats: 0:00:56 elapsed; 0 hosts completed (1 up), 1 undergoing Connect Scan
Connect Scan Timing: About 82.13% done; ETC: 13:43 (0:00:12 remaining)
Nmap scan report for 10.10.11.247
Host is up (0.21s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT   STATE SERVICE    VERSION
21/tcp open  ftp        vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| -rw-r--r--    1 ftp      ftp          4434 Jul 31 11:03 MigrateOpenWrt.txt
| -rw-r--r--    1 ftp      ftp       2501210 Jul 31 11:03 ProjectGreatMigration.pdf
| -rw-r--r--    1 ftp      ftp         60857 Jul 31 11:03 ProjectOpenWRT.pdf
| -rw-r--r--    1 ftp      ftp         40960 Sep 11 15:25 backup-OpenWrt-2023-07-26.tar
|_-rw-r--r--    1 ftp      ftp         52946 Jul 31 11:03 employees_wellness.pdf
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.14.5
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 48:ad:d5:b8:3a:9f:bc:be:f7:e8:20:1e:f6:bf:de:ae (RSA)
|   256 b7:89:6c:0b:20:ed:49:b2:c1:86:7c:29:92:74:1c:1f (ECDSA)
|_  256 18:cd:9d:08:a6:21:a8:b8:b6:f7:9f:8d:40:51:54:fb (ED25519)
53/tcp open  tcpwrapped
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

 - ftp 서버내에 파일이 존재하는것을 확인하였고 아래의 이미지처럼 접근이 가능하다는것을 알고 파일을 내 로컬로 가져와 분석하였습니다.
 - 두번째로는 port 22번 ssh가 열려있는것을 확인할수있었습니다.
 - guest로 ssh를 통하여 bash에 접근하라는것을 예상할수있습니다.
ftp://ip
<img width="917" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/c8cd29db-c2c0-47bc-80d9-d5ef5076b78f">
 - ftp 서버안의 backup파일이 압축되있는것을 확인하고 압축을 풀어서 Tree구조를 확인하였을때 내용은 다음과 같다.

```
.
├── config
│   ├── dhcp
│   ├── dropbear
│   ├── firewall
│   ├── luci
│   ├── network
│   ├── rpcd
│   ├── system
│   ├── ucitrack
│   ├── uhttpd
│   └── wireless
├── dropbear
│   ├── dropbear_ed25519_host_key
│   └── dropbear_rsa_host_key
├── group
├── hosts
├── inittab
├── luci-uploads
├── nftables.d
│   ├── 10-custom-filter-chains.nft
│   └── README
├── opkg
│   └── keys
│       └── 4d017e6f1ed5d616
├── passwd
├── profile
├── rc.local
├── shells
├── shinit
├── sysctl.conf
├── uhttpd.crt
└── uhttpd.key
```
 - 오디팅하다 중요해보이는 파일을 보았을때 해당 내용들이 담긴것을 확인할수있었습니다.

 - passwd
```
root:x:0:0:root:/root:/bin/ash
daemon:*:1:1:daemon:/var:/bin/false
ftp:*:55:55:ftp:/home/ftp:/bin/false
network:*:101:101:network:/var:/bin/false
nobody:*:65534:65534:nobody:/var:/bin/false
ntp:x:123:123:ntp:/var/run/ntp:/bin/false
dnsmasq:x:453:453:dnsmasq:/var/run/dnsmasq:/bin/false
logd:x:514:514:logd:/var/run/logd:/bin/false
ubus:x:81:81:ubus:/var/run/ubus:/bin/false
netadmin:x:999:999::/home/netadmin:/bin/false
```

 - wireless
```

config wifi-device 'radio0'
	option type 'mac80211'
	option path 'virtual/mac80211_hwsim/hwsim0'
	option cell_density '0'
	option channel 'auto'
	option band '2g'
	option txpower '20'

config wifi-device 'radio1'
	option type 'mac80211'
	option path 'virtual/mac80211_hwsim/hwsim1'
	option channel '36'
	option band '5g'
	option htmode 'HE80'
	option cell_density '0'

config wifi-iface 'wifinet0'
	option device 'radio0'
	option mode 'ap'
	option ssid 'OpenWrt'
	option encryption 'psk'
	option key 'VeRyUniUqWiFIPasswrd1!'
	option wps_pushbutton '1'

config wifi-iface 'wifinet1'
	option device 'radio1'
	option mode 'sta'
	option network 'wwan'
	option ssid 'OpenWrt'
	option encryption 'psk'
	option key 'VeRyUniUqWiFIPasswrd1!'
```

 - ```passwd```파일의 내용을보면 /etc/passwd 의 파일을 그대로 가져온것을 알수있었고 ```ftp & netadmin``` 의 work dir이 /home/* 인것을 알수있었고
 - ```ftp```는 ```file transfer protocol```로 해당 프로토콜을 통하여 서버에있던 파일을 다운받았었고 netadmin이 ssh server work dir인것을 예상할수있었다.
 - 2 번째 로는 ssh server에 접속하기위한 password인데 wireless 파일을 확인해보면 ```iwconf```의 내용의 iface를 가져온것을 확인할수있고 해당 무선lan 의 passkey가 담긴것을 확인할수있고
 - 해당 passkey를 ssh password 로 접속하니 아래와같이 ```user```권한으로 bash에 접근이 가능한것을 확인할수있다.
<img width="568" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/be16d7c0-086b-4774-8034-eda7c44620c8">
 - 이제 user_key & root_key 를 얻으면 정상적인 문제해결이 가능하다 일단 work_dir 에서 파일을 확인하면 user.txt를 확인할수있었고
<img width="567" alt="image" src="https://github.com/ChCh0i/steel/assets/108965611/27849b25-dd24-44b4-8b93-d237e72dbab4">
 - root.txt는 일반 권한으로 접근이불가능한 root dir에 있을것으로 예상된다.
 - 아까 문제를 소개할때 제목에서 힌트를 얻었다고 말했다 ```wifinetic``` 일단 문제 제목만봐도 무선lan에 관하여 연관지어 문제를 의도하였고
 - 제공되는 ftp파일로만봐도 무선lan iface관련인것을 알수있다.
 - iwconfig
