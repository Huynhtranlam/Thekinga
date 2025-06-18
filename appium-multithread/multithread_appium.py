from threading import Thread
from appium import webdriver
import time
import subprocess
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from appium.webdriver.appium_service import AppiumService
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.android import UiAutomator2Options

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction


def login_to_zalo(index, instance_port, udid):
    service = None
    driver = None
    try:
        # ADB connect
        subprocess.run(["adb", "connect", udid], check=True)

        # Start Appium server
        service = AppiumService()
        service.start(args=[
            "--address", "127.0.0.1",
            "--port", str(instance_port),
            "-pa", "/wd/hub"
        ])
        print(f"[{udid}] Appium server started at {instance_port}")

        # Setup options
        options = UiAutomator2Options()
        options.set_capability("platformName", "Android")
        options.set_capability("platformVersion", "9")
        options.set_capability("automationName", "UiAutomator2")
        options.set_capability("udid", udid)

        options.set_capability("appPackage", "com.zing.zalo")
        options.set_capability("appActivity", "com.zing.zalo.ui.ZaloLauncherActivity")
        options.set_capability("noReset", True)
        options.set_capability("systemPort", random.randint(8201, 8299))

        # Start driver
        driver = webdriver.Remote(f"http://127.0.0.1:{instance_port}/wd/hub", options=options)
        wait = WebDriverWait(driver, 30)
        print(f"[{udid}] Connected to Appium server at {instance_port}")

        zalo_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Zalo")'))
        )
        zalo_icon.click()

        # 👉 Thực hiện các thao tác touch
        def tap(x, y):
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(x, y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        tap(652, 192)
        tap(227, 644)
        tap(488, 283)
        tap(840, 552)
        tap(1167, 646)

        time.sleep(10)
        driver.quit()

    except Exception as e:
        print(f"[{udid}] Error: {e}")
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
    finally:
        if service:
            service.stop()
            print(f"[{udid}] Appium server stopped.")


# === Multi-thread section ===

number_of_instances = 1
threads = []

for i in range(number_of_instances):
    instance_port = 4723 + i
    udid = f"127.0.0.1:{5555 + (i * 10)}"
    thread = Thread(target=login_to_zalo, args=(i, instance_port, udid))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
