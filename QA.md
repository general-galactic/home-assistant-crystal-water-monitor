# Crystal Water Monitor – QA Testing Setup

## 1. Run Home Assistant

The easiest option is a VM using the official prebuilt image:

1. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) (free)
2. Download the **Home Assistant OS** `.vdi` image from [home-assistant.io/installation/windows](https://www.home-assistant.io/installation/windows/) (or `/macos` / `/linux`)
3. In VirtualBox: New VM → Use existing virtual hard disk → select the `.vdi` → Start
4. Wait ~5 min, then open [http://homeassistant.local:8123](http://homeassistant.local:8123) in your browser
5. Complete the onboarding wizard (create an account, skip any device discovery)

## 2. Install HACS

1. In HA, go to your **profile** (bottom-left) → enable **Advanced Mode**
2. Go to **Settings → Add-ons → Add-on Store** → search **Terminal & SSH** → Install → enable "Show in sidebar" → Start
3. Open the Terminal and run:
   ```
   wget -O - https://get.hacs.xyz | bash -
   ```
4. Go to **Settings → System → Restart**
5. After restart: **Settings → Devices & Services → Add Integration** → search **HACS**
6. Authorize with GitHub when prompted (you'll need a free GitHub account)

## 3. Install the Crystal Water Monitor Integration

1. In HA sidebar, click **HACS**
2. Click the **⋮ menu** (top right) → **Custom repositories**
3. Add:
   - URL: `https://github.com/general-galactic/home-assistant-crystal-water-monitor`
   - Category: **Integration**
4. Search for **Crystal Water Monitor** in HACS → Install → Restart HA
5. Go to **Settings → Devices & Services → Add Integration** → search **Crystal Water Monitor** → follow setup prompts

## 4. What to Test

- [ ] Integration installs without errors
- [ ] Setup flow completes successfully with valid credentials
- [ ] Setup flow shows appropriate errors with invalid credentials
- [ ] Sensor data loads and updates
- [ ] Integration survives a HA restart
