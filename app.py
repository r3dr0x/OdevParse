from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

# Go to the website of Akakoleji
driver.get("https://akakoleji.net/")

try:
    # Locating the username and password input fields by their ids
    username_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    password_box = driver.find_element(By.ID, 'password')

    # Clearing the current content of the username and password input fields 
    username_box.clear()
    password_box.clear()

    # Entering data into the username and password fields
    username_box.send_keys('')
    password_box.send_keys('')

    # Locating the submit button by XPath and clicking it
    login_button = driver.find_element(By.XPATH, '//*[@id="login-screen-container"]/div[2]/div/div[1]/div[2]/form/div[4]/button')
    login_button.click()

    # Allow some delay after the button click for potential redirects (3 seconds as an example)
    time.sleep(7)

    # Finding a specific element using an XPath and clicking it
    first_click_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[12]/a/span'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", first_click_element)
    first_click_element.click()

    second_click_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[12]/ul/li[1]/a/span'))
    )
    driver.execute_script("arguments[0].scrollIntoView();", second_click_element)
    second_click_element.click()

    # Allow a delay of 1 second
    time.sleep(1)

    # To click on a button given its specific type using WebDriverWait and expected_conditions 
    buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((
            By.XPATH, 
            '//button[@data-toggle="tooltip" and @data-placement="left" and @data-original-title="Detay"]'
        ))
    )

    for i, button in enumerate(buttons, start=1):
        driver.execute_script("arguments[0].scrollIntoView();", button)
        try:  
            td_tag_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'(//td[@tabindex="0"])[{i}]'))).text
        except Exception as ex:
            print(f"An error occurred while getting the td tag content: {str(ex)}")

        time.sleep(1)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)

        # Find and click the revealed button
        popup_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalstrap-button-0"]')))
        popup_button.click()
        
        extra_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/section/div/div/div[2]/section/div[2]/div[2]/div/div[2]/div[2]/div[3]')))
        extra_text = extra_element.text

        # Checking the status
        status_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="status"]')))
        status_text = status_element.text

        if status_text.strip() == "Değerlendirilmedi":
            description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'description')))
            description_text = description_element.text
            # Print into the file only when status_text == "Değerlendirilmedi"
            with open('odevler.txt', 'a', encoding='utf-8') as f:
                f.write(f"Ders Adı: {extra_text}\n")
                f.write(f"Kitap Adı: {td_tag_content}\n")
                f.write(f"Açıklama: {description_text}")
                f.write('\n\n')

except Exception as ex:
    print(f"An error occurred: {str(ex)}")
finally:
    # Allow a delay of 5 seconds
    time.sleep(5)

    # Close the browser
    driver.quit()
