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
from selenium.common.exceptions import NoSuchElementException, WebDriverException


def tap(driver, x, y, pause_sec: float = 0.02):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(
        driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
    )
    a = actions.w3c_actions.pointer_action
    a.move_to_location(x, y)
    a.pointer_down()
    a.pause(pause_sec)
    a.pointer_up()
    actions.perform()


def swipe(driver, x1, y1, x2, y2, pause_sec: float = 0.0):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(
        driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
    )
    a = actions.w3c_actions.pointer_action
    a.move_to_location(x1, y1)
    a.pointer_down()
    a.pause(pause_sec)
    a.move_to_location(x2, y2)
    a.pointer_up()
    actions.perform()
def click_until_element_appears(driver, button_selector, target_selector, timeout=15, retry_interval=0.2):
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Check nếu phần tử đích đã xuất hiện → kết thúc
            driver.find_element(*target_selector)
            print("🎯 Found target element!")
            return

        except NoSuchElementException:
            # Chưa thấy phần tử đích, tiếp tục click
            try:
                btn = driver.find_element(*button_selector)
                if btn.is_enabled() and btn.is_displayed():
                    btn.click()
                    print("🖱 Clicked 'Next'")
                else:
                    print("⏳ Button not clickable yet")
            except WebDriverException:
                print("⚠️ Button not ready or not found")
            time.sleep(retry_interval)

    raise TimeoutError("❌ Timed out: Target element never appeared.")

def login_to_zalo(index, instance_port, udid):
    service = None
    driver = None
    try:
        subprocess.run(["adb", "connect", udid], check=True)

        service = AppiumService()
        service.start(args=[
            "--address", "127.0.0.1",
            "--port", str(instance_port),
            "-pa", "/wd/hub"
        ])
        print(f"[{udid}] Appium server started at {instance_port}")

        options = UiAutomator2Options()
        options.set_capability("platformName", "Android")
        options.set_capability("platformVersion", "9")
        options.set_capability("automationName", "UiAutomator2")
        options.set_capability("udid", udid)
        options.set_capability("appPackage", "com.zing.zalo")
        options.set_capability("appActivity", "com.zing.zalo.ui.ZaloLauncherActivity")
        options.set_capability("noReset", True)
        options.set_capability("systemPort", random.randint(8201, 8299))

        driver = webdriver.Remote(f"http://127.0.0.1:{instance_port}/wd/hub", options=options)
        driver.implicitly_wait(7)

        # ============ BẮT ĐẦU CHUỖI ACTION ============

        wait = WebDriverWait(driver, 100)

        # ViewGroup đầu tiên – CHỈNH THÀNH WAIT
        el5 = wait.until(
            EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.view.ViewGroup"))
        )
        el5.click()

        try:
            el5 = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.view.View").instance(8)'
                ))
            )

            # 👉 Swipe 2
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(756, 763)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(979, 35)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        except:
            print("Không tìm thấy el5 sau 20 giây.")
        
        
        # Đợi đủ 2 ô EditText
        name_box = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(0)'
            ))
        )
        wait.until(
            EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(2)'
            ))
        )

        # Điền form
        name_box.send_keys("Huỳnh Trần Đông")

        email_box = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(2)'
        )
        email_box.send_keys("a@a.com")

        swipe(driver, 702, 654, 819, 321)

        phone_box = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.EditText").instance(3)'
        )
        phone_box.send_keys("079099000625")

        agree_chk = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("đồng ý")'
        )
        agree_chk.click()

        click_until_element_appears(
    driver,
    button_selector=(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Tiếp tục (Next)")'),
    target_selector=(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Tỉnh thành")'),
    timeout=40,
    retry_interval=0.3
)

        el5 = wait.until(
            EC.presence_of_element_located((
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Tỉnh thành")'
            ))
        )
        el5.click()
        print("Tiền hành tỉnh thành")
        time.sleep(0.2)
        el6 = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Vui lòng chọn địa điểm, cửa hàng để hiển thị các khung giờ đăng ký.")'
        )
        el6.click()
        time.sleep(0.2)
        
        el7 = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Cửa hàng")'
        )
        el7.click()
        time.sleep(0.2)
        el8 = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().text("Please select a location & store to display the available registration time slots.")'
        )
        el8.click()

        el9 = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("19/07/202508:15 - 11:45")'
        )
        el9.click()

        el10 = driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.TextView").instance(13)'
        )
        el10.click()

        print(f"[{udid}] Scenario completed.")
        time.sleep(5)

    except Exception as e:
        print(f"[{udid}] Error: {e}")
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass
        if service:
            service.stop()
            print(f"[{udid}] Appium server stopped.")


# === Multi-thread ===
number_of_instances = 1
threads = []

for i in range(number_of_instances):
    instance_port = 4723 + i
    udid = f"127.0.0.1:{5555 + (i * 10)}"
    t = Thread(target=login_to_zalo, args=(i, instance_port, udid))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
