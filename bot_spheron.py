import requests
import random
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# === KONFIGURASI ===
REFERRAL_LINK = "https://tge.spheron.network/signup?ref=666985CE"  # Ganti dengan referralmu
USERNAME_PREFIX = "refbot"
PASSWORD = "BotPass123!"
CHROME_DRIVER_PATH = "/usr/local/bin/chromedriver"
CSV_FILE = "akun_terdaftar.csv"

def get_temp_email():
    domain_data = requests.get("https://api.mail.tm/domains").json()
    domain = domain_data["hydra:member"][0]["domain"]
    username = f"{USERNAME_PREFIX}{random.randint(1000,9999)}"
    email = f"{username}@{domain}"
    password = "tempmail123"

    r = requests.post("https://api.mail.tm/accounts", json={
        "address": email,
        "password": password
    })

    if r.status_code != 201:
        raise Exception("Gagal membuat email sementara")

    print(f"[📧] Email dibuat: {email}")
    return email, username

def daftar_ke_spheron(email, username):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)
    driver.get(REFERRAL_LINK)
    time.sleep(3)

    try:
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        tombol = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign up')]")
        tombol.click()

        time.sleep(5)
        print(f"[✅] Akun berhasil join: {email}")
        return True
    except Exception as e:
        print("[❌] Gagal daftar:", e)
        return False
    finally:
        driver.quit()

def simpan_ke_csv(email, username, password):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([email, username, password])
    print(f"[💾] Disimpan ke CSV: {email}")

def main_loop():
    while True:
        try:
            email, username = get_temp_email()
            berhasil = daftar_ke_spheron(email, username)
            if berhasil:
                simpan_ke_csv(email, username, PASSWORD)
        except Exception as e:
            print(f"[⚠️] Error: {e}")
        delay = random.randint(30, 60)
        print(f"[⏱️] Delay {delay} detik sebelum lanjut...\n")
        time.sleep(delay)

if name == "__main__":
    main_loop()
