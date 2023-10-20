from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
chrome_options = Options()
chrome_options.add_argument("--headless")
webdriver_service = Service()
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
driver.get("https://akakoleji.net/")

try:
    username_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    password_box = driver.find_element(By.ID, 'password')
    username_box.clear()
    password_box.clear()
    username_box.send_keys('XXXX')
    password_box.send_keys('XXXX')

    login_button = driver.find_element(By.XPATH, '//*[@id="login-screen-container"]/div[2]/div/div[1]/div[2]/form/div[4]/button')
    login_button.click() 
    time.sleep(7)

    first_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[12]/a/span'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", first_click)
    first_click.click()

    second_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[12]/ul/li[1]/a/span'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", second_click)
    second_click.click()

    time.sleep(1)

    buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.XPATH, 
            '//button[@data-toggle="tooltip" and @data-placement="left" and @data-original-title="Detay"]'
        ))
    )

    for i, button in enumerate(buttons, start=1):
        driver.execute_script("arguments[0].scrollIntoView();", button)
        td_tag_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'(//td[@tabindex="0"])[{i}]'))).text
        
        time.sleep(1) 
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        # Beliren butonu bul ve tıkla
        popup_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalstrap-button-0"]')))
        popup_button.click()
        extra_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/section/div/div/div[2]/section/div[2]/div[2]/div/div[2]/div[2]/div[3]')))
        extra_text = extra_element.text
        # Check the status
        status_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="status"]')))
        status_text = status_element.text

        if status_text == "Değerlendirilmedi":
            description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'description')))
            description_text = description_element.text
            with open('odevler.txt', 'a') as f:
                f.write(f"Ders Adı: {extra_text}\n")
                f.write(f"Kitap Adı: {td_tag_content}\n")
                f.write(f"Açıklama: {description_text}")
                f.write('\n\n')
                
except Exception as ex:
    print(f"An error occurred: {str(ex)}")
finally:
    time.sleep(5)
    driver.quit()
