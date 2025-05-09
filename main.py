import requests, json, time, smtplib, yaml, os,random
from email.mime.text import MIMEText

SEEN_FILE = "seen.json"

# Load seen message IDs from disk
def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()

# Save seen message IDs to disk
def save_seen(seen_ids):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_ids), f)

seen = load_seen()

# CARRIER_GATEWAYS = {
#     'att': 'txt.att.net',
#     'verizon': 'vtext.com',
#     'tmobile': 'tmomail.net',
#     'sprint': 'messaging.sprintpcs.com',
#     'boost': 'sms.myboostmobile.com',
#     'cricket': 'sms.cricketwireless.net',
#     'uscellular': 'email.uscc.net',
# }
cookies = {
    'csrftoken': 'WP9c2tS6s_CbZkwLZclCd8',
    'datr': '9TkeaIrsAR-oWcvo79GdRvi_',
    'ig_did': '9E30DCA7-1135-4EE4-92B6-05567D2B9E9E',
    #'sessionid': ''  # REQUIRED
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.instagram.com',
    'referer': 'https://www.instagram.com/channel/AbarSVcaXm1LFLpL/?igsh=MWN6aWNnMjl6aDBzdg%3D%3D',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'x-asbd-id': '359341',
    'x-csrftoken': 'WP9c2tS6s_CbZkwLZclCd8',
    'x-fb-friendly-name': 'PolarisChannelLinkRootQuery',
    'x-fb-lsd': 'AVoRdVwWGDo',
    'x-ig-app-id': '936619743392459',
}

data = {
    'av': '0',
    '__d': 'www',
    '__user': '0',
    '__a': '1',
    '__req': '3',
    '__hs': '20217.HYP:instagram_web_pkg.2.1...0',
    'dpr': '1',
    '__ccg': 'EXCELLENT',
    '__rev': '1022682976',
    '__s': 'ppww68:gv43vi:a4wfw9',
    '__hsi': '7502497755513665163',
    '__dyn': '7xeXzWwlEnwn8yEbFp41twpUnwgU7SbzEdF8aUco2qwJyE2OwpUe8hwaG0riq1ew6ywMwto2awgo9oO0n24oaEd86a3a1YwBgao6C0Mo2swtUd8-U2exi4UaEW2G0AEco4i5o7G4-5o4q3y1Sw62wLyESE7i3u2C2J08O321LwTwKG1pg2Xwr86C1mg6LhA6bwIDzUnAwHK6E5y4UrwHwcObyo1iE',
    '__csr': '...',
    '__comet_req': '7',
    'lsd': 'AVoRdVwWGDo',
    'jazoest': '2986',
    '__spin_r': '1022682976',
    '__spin_b': 'trunk',
    '__spin_t': '1746811381',
    '__jssesw': '157',
    '__crn': 'comet.igweb.PolarisChannelLinkRoute',
    'fb_api_caller_class': 'RelayModern',
    'fb_api_req_friendly_name': 'PolarisChannelLinkRootQuery',
    'variables': '{"input":{"num_items":20,"thread_igid":7264681630251492}}',
    'server_timestamps': 'true',
    'doc_id': '29349007078047465',
}

seen = set()

def check_messages():
    response = requests.post('https://www.instagram.com/api/graphql', cookies=cookies, headers=headers, data=data)

    try:
        result = response.json()
        items = result["data"]["xfb_igd_channel_web_preview"]["channel_preview"]["items"]
    except Exception:
        print("Invalid response:", response.text[:300])
        return

    updated = False

    for item in items:
        mid = item.get("message_id")
        if mid in seen or item.get("item_type") != "LINK":
            continue

        full = json.loads(item["full_item_dict"])
        link_text = full.get("link", {}).get("text", "")
        if any(domain in link_text for domain in ["gofile.io/d/", "pillowcase.su", "krakenfiles.com/view/"]):
            print("FOUND MATCH:", link_text)
            settings = load_settings()
            send_sms(link_text, settings)
            print("Sleeping for 1 Min")
            updated = True
            time.sleep(60)

        seen.add(mid)

    if updated:
        save_seen(seen)


def load_settings(file_path='settings.yaml'):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def send_sms(message, settings):
    CARRIER_GATEWAYS = {
        'att': 'txt.att.net',
        'verizon': 'vtext.com',
        'tmobile': 'tmomail.net',
        'sprint': 'messaging.sprintpcs.com',
        'boost': 'sms.myboostmobile.com',
        'cricket': 'sms.cricketwireless.net',
        'uscellular': 'email.uscc.net',
    }

    phone_number = settings['PHONE_NUMBER']
    email = settings['IMAP_EMAIL']
    password = settings['IMAP_PASSWORD']
    carrier = settings['TYPE']

    if carrier not in CARRIER_GATEWAYS:
        raise ValueError(f"Unsupported carrier '{carrier}'.")

    to_sms = f"{phone_number}@{CARRIER_GATEWAYS[carrier]}"
    subject = f"New Uzi Leak Detected ⚠️{random.randint(1,9999)}"

    msg = MIMEText(message, _charset="utf-8")
    msg["From"] = email
    msg["To"] = to_sms
    msg["Subject"] = subject

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, to_sms, msg.as_string())
            print(f"✅ Sent to {to_sms}")
    except Exception as e:
        print(f"❌ Failed to send: {e}")




# Repeat every 2 hours
while True:
    check_messages()
    print("Sleeping for 2 Hours...")
    time.sleep(2 * 60 * 60)
