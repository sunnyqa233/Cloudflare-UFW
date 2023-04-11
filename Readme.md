# Cloudflare-UFW
A python script to help manage UFW rules to open ports only for [Cloudflare](https://www.cloudflare.com/).

## Dependency
* Python >= 3.7
* Python packages listed in `requirements.txt`
* UFW

## Config
There are some settings in `main.py`. Modify it to suit your need.
```python
# UFW rules with this comment is managed by this script.
comment = "cloudflare-ufw-managed"

enable_ipv4 = True  # Open ports for Cloudflare via IPV4
ipv4_list_url = "https://www.cloudflare.com/ips-v4"  # URL to Cloudflare's IPV4 CIDR list
ipv4_tcp_ports = [80, 443]  # Open these TCP ports for Cloudflare via IPV4
ipv4_udp_ports = [443]  # Open these UDP ports for Cloudflare via IPV4

enable_ipv6 = True  # Open ports for Cloudflare via IPV6
ipv6_list_url = "https://www.cloudflare.com/ips-v6"  # URL to Cloudflare's IPV6 CIDR list
ipv6_tcp_ports = [80, 443]  # Open these TCP ports for Cloudflare via IPV6
ipv6_udp_ports = [443]  # Open these UDP ports for Cloudflare via IPV6
```

## Usage
> Warning: I had only tested this script on two of my Debian 11 server. I won't be responsible if this script caused you any lost or damage.
1. Clone this repo.
   ```bash
   git clone https://github.com/sunnyqa233/Cloudflare-UFW.git
   ```
2. Ensure the script its own by root, and only root has it's write permission. (Safety reason)
   ```bash
   chown -R root:root Cloudflare-UFW
   chmod -R 644 Cloudflare-UFW
   ```
3. Install dependency.
   ```
   # Install python3
   apt install python3-pip
   # Install packages listed in requirements.txt
   pip3 install -r Cloudflare-UFW/requirements.txt
   ```
4. Modify settings in `Cloudflare-UFW/main.py` to suit your needs.
5. Run the script.
   ```bash
   python3 Cloudflare-UFW/main.py
   ```
6. Setup crontab to keep this script regularly. (I run it once a day.)  
   You may refer to [this guide](https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e).

## Reminder
For users of `aapanel` or `宝塔面板`. If you have no rules about port 443 in the panel's `security` section, the panel would automatically allow port 443(tcp and udp) to be access from anywhere if you applied SSL certificate.  
Create a placeholder(e.g. Allow 443/tcp access from 127.0.0.1 in the panel) to avoid this issue.

## Dev
If you had any problem using this script, please report it in Issues.
Any pull requests are always welcome.
