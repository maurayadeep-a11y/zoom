#!/usr/bin/env python3
# Zoom Bot for GitHub Actions
# Made by Dept of PUBLIC RELATIONS

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import os
import sys
import psutil
import threading
from datetime import datetime

# Get configuration from environment variables
START_RANGE = int(os.environ.get('START_RANGE', '1'))
END_RANGE = int(os.environ.get('END_RANGE', '30'))
NUMBER_OF_BOTS = int(os.environ.get('NUMBER_OF_BOTS', '10'))
MEETING_ID = os.environ.get('MEETING_ID', '')
MEETING_PASSCODE = os.environ.get('MEETING_PASSCODE', '')
CUSTOM_NAME = os.environ.get('CUSTOM_NAME', '')
RUN_DURATION = int(os.environ.get('RUN_DURATION', '60'))  # minutes

# Setup logging
log_file = open('bot_logs.txt', 'w')
resource_log = open('resource_usage.csv', 'w')
resource_log.write('TIME,CPU(%),MEM(%),MEM(MB),BOTS_ACTIVE\n')
resource_log.flush()

active_bot_count = 0
monitoring = True

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    log_file.write(log_message + '\n')
    log_file.flush()

def monitor_resources():
    """Monitor and log system resources every 60 seconds"""
    global monitoring, active_bot_count
    
    process = psutil.Process()
    
    while monitoring:
        try:
            cpu_percent = process.cpu_percent(interval=1)
            mem_info = process.memory_info()
            mem_percent = process.memory_percent()
            mem_mb = mem_info.rss / 1024 / 1024  # Convert to MB
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            resource_log.write(f'{timestamp},{cpu_percent:.1f},{mem_percent:.1f},{mem_mb:.1f},{active_bot_count}\n')
            resource_log.flush()
            
            # Log significant changes
            if cpu_percent > 50:
                log(f"⚠️  High CPU usage: {cpu_percent:.1f}%")
            if mem_percent > 70:
                log(f"⚠️  High memory usage: {mem_percent:.1f}%")
            
            time.sleep(60)  # Monitor every 60 seconds
            
        except Exception as e:
            log(f"Resource monitor error: {e}")
            time.sleep(60)

# Start resource monitoring in background
monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
monitor_thread.start()

log("=" * 60)
log("FUNDS BOT - GITHUB ACTIONS EDITION".center(60))
log("Made by Dept of PUBLIC RELATIONS".center(60))
log("=" * 60)
log("")

# Log system info
try:
    cpu_count = psutil.cpu_count()
    total_mem = psutil.virtual_memory().total / 1024 / 1024 / 1024  # GB
    log(f"System Info: {cpu_count} CPU cores, {total_mem:.1f} GB RAM")
except:
    pass

# Load names
try:
    with open('names.txt', 'r', encoding='utf-8') as f:
        all_names = [name.strip() for name in f.read().split('\n') if name.strip()]
    log(f"✓ Loaded {len(all_names)} names from names.txt")
except FileNotFoundError:
    log("❌ ERROR: names.txt not found!")
    sys.exit(1)

# Validate range
if START_RANGE < 1 or END_RANGE > len(all_names) or START_RANGE > END_RANGE:
    log(f"❌ Invalid range: {START_RANGE}-{END_RANGE}")
    sys.exit(1)#!/usr/bin/env python3
# Zoom Bot for GitHub Actions
# Made by Dept of PUBLIC RELATIONS

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import random
import time
import os
import sys
from datetime import datetime

# Get configuration from environment variables
START_RANGE = int(os.environ.get('START_RANGE', '1'))
END_RANGE = int(os.environ.get('END_RANGE', '30'))
NUMBER_OF_BOTS = int(os.environ.get('NUMBER_OF_BOTS', '10'))
MEETING_ID = os.environ.get('MEETING_ID', '')
MEETING_PASSCODE = os.environ.get('MEETING_PASSCODE', '')
CUSTOM_NAME = os.environ.get('CUSTOM_NAME', '')
RUN_DURATION = int(os.environ.get('RUN_DURATION', '60'))  # minutes

# Setup logging
log_file = open('bot_logs.txt', 'w')

def log(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    print(log_message)
    log_file.write(log_message + '\n')
    log_file.flush()

log("=" * 60)
log("FUNDS BOT - GITHUB ACTIONS EDITION".center(60))
log("Made by Dept of PUBLIC RELATIONS".center(60))
log("=" * 60)
log("")

# Load names
try:
    with open('names.txt', 'r', encoding='utf-8') as f:
        all_names = [name.strip() for name in f.read().split('\n') if name.strip()]
    log(f"✓ Loaded {len(all_names)} names from names.txt")
except FileNotFoundError:
    log("❌ ERROR: names.txt not found!")
    sys.exit(1)

# Validate range
if START_RANGE < 1 or END_RANGE > len(all_names) or START_RANGE > END_RANGE:
    log(f"❌ Invalid range: {START_RANGE}-{END_RANGE}")
    sys.exit(1)

selected_names = all_names[START_RANGE-1:END_RANGE]
log(f"✓ Selected {len(selected_names)} names (range {START_RANGE}-{END_RANGE})")
log(f"✓ Configuration:")
log(f"  - Bots: {NUMBER_OF_BOTS}")
log(f"  - Meeting ID: {MEETING_ID}")
log(f"  - Duration: {RUN_DURATION} minutes")
log("")

# Chrome options
def get_chrome_options():
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--mute-audio')
    options.add_argument('--disable-extensions')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-webrtc')
    options.add_argument('--disable-webrtc-hw-encoding')
    options.add_argument('--disable-webrtc-hw-decoding')
    
    prefs = {
        'profile.default_content_setting_values.media_stream_mic': 2,
        'profile.default_content_setting_values.media_stream_camera': 2,
        'profile.default_content_setting_values.notifications': 2,
        'profile.managed_default_content_settings.images': 2,
    }
    options.add_experimental_option('prefs', prefs)
    
    return options

# Media blocking
MEDIA_BLOCKER = """
(function() {
    window.RTCPeerConnection = function() {
        return {
            createOffer: () => Promise.reject(new Error('Disabled')),
            createAnswer: () => Promise.reject(new Error('Disabled')),
            setLocalDescription: () => Promise.reject(new Error('Disabled')),
            setRemoteDescription: () => Promise.reject(new Error('Disabled')),
            addIceCandidate: () => Promise.reject(new Error('Disabled')),
            addStream: () => {}, addTrack: () => {}, close: () => {},
            getSenders: () => [], getReceivers: () => [], getTransceivers: () => []
        };
    };
    HTMLMediaElement.prototype.play = function() { this.pause(); return false; };
})();
"""

def inject_media_blocker(driver):
    try:
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': MEDIA_BLOCKER})
    except:
        pass

def kill_media_elements(driver):
    try:
        driver.execute_script("""
            setInterval(() => {
                document.querySelectorAll('video, audio').forEach(e => {
                    if(e.srcObject) e.srcObject.getTracks().forEach(t => t.stop());
                    e.pause(); e.remove();
                });
            }, 1000);
        """)
    except:
        pass

# Launch bot
def launch_bot(bot_id):
    driver = None
    try:
        time.sleep(random.uniform(2, 4))
        
        options = get_chrome_options()
        
        # Try undetected-chromedriver first (auto-handles version)
        try:
            log(f"Bot {bot_id+1}: Using undetected-chromedriver...")
            driver = uc.Chrome(options=options, use_subprocess=False, version_main=None)
        except Exception as uc_error:
            # Fallback to regular Chrome with ChromeDriverManager
            log(f"Bot {bot_id+1}: Falling back to ChromeDriverManager...")
            try:
                service = Service(ChromeDriverManager().install())
                from selenium.webdriver.chrome.options import Options as RegularOptions
                regular_opts = RegularOptions()
                for arg in ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', 
                           '--mute-audio', '--disable-extensions', '--blink-settings=imagesEnabled=false',
                           '--disable-webrtc', '--disable-webrtc-hw-encoding', '--disable-webrtc-hw-decoding']:
                    regular_opts.add_argument(arg)
                
                prefs = {
                    'profile.default_content_setting_values.media_stream_mic': 2,
                    'profile.default_content_setting_values.media_stream_camera': 2,
                    'profile.default_content_setting_values.notifications': 2,
                    'profile.managed_default_content_settings.images': 2,
                }
                regular_opts.add_experimental_option('prefs', prefs)
                
                driver = webdriver.Chrome(service=service, options=regular_opts)
            except Exception as fallback_error:
                log(f"Bot {bot_id+1}: Both methods failed - UC: {uc_error}, Regular: {fallback_error}")
                raise fallback_error
        
        inject_media_blocker(driver)
        
        driver.set_page_load_timeout(30)
        driver.get(f'https://zoom.us/wc/join/{MEETING_ID}')
        
        time.sleep(random.uniform(2, 3))
        
        wait = WebDriverWait(driver, 20)
        
        # Get bot name
        if CUSTOM_NAME:
            bot_name = CUSTOM_NAME
        else:
            bot_name = selected_names[bot_id % len(selected_names)]
        
        # Handle continue button
        try:
            continue_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'continue')))
            continue_btn.click()
            time.sleep(1)
        except:
            pass
        
        # Find name input
        name_input = None
        for selector in ['input-for-name', 'inputname', 'join-dialog-name']:
            try:
                name_input = wait.until(EC.visibility_of_element_located((By.ID, selector)))
                break
            except:
                continue
        
        if not name_input:
            name_input = wait.until(EC.visibility_of_element_located((By.NAME, 'name')))
        
        # Find password input
        pwd_input = None
        if MEETING_PASSCODE:
            for selector in ['input-for-pwd', 'inputpasscode', 'join-dialog-passcode']:
                try:
                    pwd_input = driver.find_element(By.ID, selector)
                    break
                except:
                    continue
        
        # Enter credentials
        name_input.clear()
        name_input.send_keys(bot_name)
        time.sleep(0.5)
        
        if pwd_input and MEETING_PASSCODE:
            pwd_input.clear()
            pwd_input.send_keys(MEETING_PASSCODE)
            time.sleep(0.5)
        
        # Click join button
        join_btn = None
        join_selectors = [
            "//button[contains(@class, 'preview-join-button')]",
            "//button[contains(text(), 'Join')]",
            "//button[@type='submit']"
        ]
        
        for selector in join_selectors:
            try:
                join_btn = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                break
            except:
                continue
        
        if join_btn:
            driver.execute_script("arguments[0].click();", join_btn)
        
        time.sleep(4)
        kill_media_elements(driver)
        
        log(f"✓ Bot {bot_id+1} joined as '{bot_name}'")
        return (driver, bot_name)
        
    except Exception as e:
        log(f"✗ Bot {bot_id+1} failed: {str(e)}")
        if driver:
            try:
                driver.quit()
            except:
                pass
        return None

# Main execution
log("=" * 60)
log(f"LAUNCHING {NUMBER_OF_BOTS} BOTS")
log("=" * 60)
log("")

active_drivers = []

for i in range(NUMBER_OF_BOTS):
    log(f"Launching bot {i+1}/{NUMBER_OF_BOTS}...")
    
    result = launch_bot(i)
    
    if result:
        driver, bot_name = result
        active_drivers.append((i+1, driver, bot_name))
    
    if i < NUMBER_OF_BOTS - 1:
        time.sleep(random.uniform(2, 4))

log("")
log("=" * 60)
log("DEPLOYMENT COMPLETE")
log("=" * 60)
log(f"✓ Successfully launched: {len(active_drivers)}/{NUMBER_OF_BOTS} bots")
log(f"✓ Name range used: {START_RANGE}-{END_RANGE}")

if active_drivers:
    log("\n👥 Deployed bots:")
    for bot_id, driver, name in active_drivers:
        log(f"   Bot {bot_id}: {name}")

log("")
log(f"⏱️  Bots will run for {RUN_DURATION} minutes...")
log("=" * 60)
log("")

# Keep bots alive for specified duration
start_time = time.time()
end_time = start_time + (RUN_DURATION * 60)

try:
    while time.time() < end_time:
        remaining = int((end_time - time.time()) / 60)
        if remaining % 5 == 0:  # Log every 5 minutes
            log(f"⏱️  {remaining} minutes remaining...")
        time.sleep(60)  # Check every minute
except KeyboardInterrupt:
    log("\n⚠️  Interrupted by user")

# Cleanup
log("\n🛑 Stopping all bots...")
for bot_id, driver, name in active_drivers:
    try:
        driver.quit()
        log(f"✓ Stopped bot {bot_id}")
    except:
        pass

log(f"\n✓ All {len(active_drivers)} bots stopped successfully!")
log("\nDon't be jealous now Golu's! 😄")
log_file.close()
