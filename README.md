
# Uzi Leak Monitor 📲⚠️

A Python script that monitors a specific **Instagram broadcast channel** for **Lil Uzi Vert music leaks** (or other media links) — and instantly **sends an SMS alert** to your phone when a new leak is posted.

---

## 💡 Why I Built This

I'm a huge **Lil Uzi Vert** fan, but I was always **late to his leaks** — especially when they dropped on Instagram broadcast channels. I wanted something that could:
- Monitor for **new links** like GoFile, Pillowcase, KrakenFiles
- Alert me instantly by **text message**
- Run automatically every couple hours

Now it does exactly that, and I’m sharing it with other fans and devs who want the same.

---

## 🔍 What It Does

- Connects to **Instagram’s internal API** to scan the last 20 messages of a specific channel.
- Checks for **music leak links** (`gofile.io/d/`, `pillowcase.su`, `krakenfiles.com/view/`).
- Avoids duplicate alerts by **tracking seen messages** across restarts.
- Sends you an **SMS alert with a custom subject** when new links are detected.
- Runs on a 2-hour loop (but you can change this easily).

---

## 🛠 Requirements

- Python 3.8+
- A Gmail account with **App Passwords enabled**
- A U.S. phone number with a supported carrier (see below)

---

## 📦 Installation

1. **Clone this repo:**

```bash
git clone https://github.com/yourname/uzi-leak-monitor.git
cd uzi-leak-monitor
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Create your `settings.yaml`:**

Create a file in the same folder called `settings.yaml`:

```yaml
IMAP_EMAIL: your_email@gmail.com
IMAP_PASSWORD: your_app_password_here
PHONE_NUMBER: your_number_here  # e.g. 3125551234
TYPE: your_carrier_here         # e.g. verizon, att, tmobile
```

---

## 📧 Gmail Setup (IMPORTANT)

This script sends SMS via Gmail's SMTP server. For it to work:

1. Go to: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Generate an App Password under **Mail → Other (e.g. UziBot)**
3. Paste the app password into `IMAP_PASSWORD` in your YAML file

⚠️ Do **not** use your real Gmail password — use an App Password!

---

## 📱 Supported Carriers

Use one of the following values for `TYPE` in your YAML:

| Carrier      | TYPE value     |
|--------------|----------------|
| AT&T         | `att`          |
| Verizon      | `verizon`      |
| T-Mobile     | `tmobile`      |
| Sprint       | `sprint`       |
| Boost Mobile | `boost`        |
| Cricket      | `cricket`      |
| US Cellular  | `uscellular`   |

If your carrier isn't listed, you can look up their email-to-SMS gateway and add it in the script.

---

## ▶️ Running the Script

Once your settings are ready:

```bash
python main.py
```

It will:
- Monitor the Instagram channel
- Print found matches
- Text you when a new leak appears
- Wait 2 hours and repeat

---

## 🧠 Notes

- Avoid spamming messages — there's a **cooldown** to prevent T-Mobile or other carriers from blocking you.
- Script tracks duplicates using a `seen.json` file.
- You can modify the target Instagram channel by changing the `data['variables']` payload in `main.py`.

---

## 🤝 Contributions Welcome

Want to:
- Add Discord alerts?
- Monitor more than one channel?
- Turn this into a Flask web app?

Feel free to fork and open a PR.

---

## 🖤 Shoutout

For the fans that stay up all night waiting for Uzi to drop — this one's for you.
