from playwright.sync_api import sync_playwright
import pyautogui
import json
import time

with open("robot/calibration.json", "r") as f:
    pos = json.load(f)

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        slow_mo=300
    )

    page = browser.new_page(
        viewport={"width": 1400, "height": 900}
    )

    page.goto("https://cadastre.com")

    print("Connecte-toi puis arrive sur la page avec les tuiles.")
    input("Quand tu vois la tuile DPE, appuie sur Entrée...")

    page.bring_to_front()
    time.sleep(1)

    print("Je clique sur DPE...")

    pyautogui.moveTo(
        pos["DPE"]["x"],
        pos["DPE"]["y"],
        duration=1
    )

    pyautogui.click()

    input("DPE cliqué. Appuie sur Entrée pour fermer...")

    browser.close()