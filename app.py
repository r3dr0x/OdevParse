from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Chrome sürücüsünün hizmetini başlat
driver = webdriver.Chrome('chromedriver.exe')

# Akakoleji sitesine git
driver.get("https://akakoleji.net/")

try:
    # Kullanıcı adı ve şifre giriş alanlarını bulmak için id'leri kullan
    username_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    password_box = driver.find_element(By.ID, 'password')

    # Kullanıcı adı ve şifre giriş alanlarının mevcut içeriğini sil
    username_box.clear()
    password_box.clear()

    # Kullanıcı adı ve şifre alanlarına veri girişi
    username_box.send_keys('XXXXX')
    password_box.send_keys('XXXXX')

    print("Username and password entered into the fields")

    # Giriş butonunu XPath kullanarak bul
    login_button = driver.find_element(By.XPATH, '//*[@id="login-screen-container"]/div[2]/div/div[1]/div[2]/form/div[4]/button')

    # giriş butonuna tıkla
    login_button.click() 

    print("Clicked on login button")

    # login_button.click() işlemi gerçekleştirdikten sonra 3 saniye bekleyin
    time.sleep(7)

    # //[@id="main-menu"]/li[12]/a/span bu xpath a click işlemi yapın
    first_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[12]/a/span'))
    )
    # Scroll to the element and click if element is not visible
    driver.execute_script("arguments[0].scrollIntoView();", first_click)
    first_click.click()

    second_click = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[12]/ul/li[1]/a/span'))
    )
    # Scroll to the element and click if element is not visible
    driver.execute_script("arguments[0].scrollIntoView();", second_click)
    second_click.click()

    time.sleep(1)

    try:
        # Belirtilen buton tipine tıklama işlemi için WebDriverWait ve expected_conditions kullanmak
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((
                By.XPATH, 
                '//button[@data-toggle="tooltip" and @data-placement="left" and @data-original-title="Detay"]'
            ))
        )
        
        for i, button in enumerate(buttons, start=1):
            driver.execute_script("arguments[0].scrollIntoView();", button)

            try:  
                # Get html content and write to a file
                td_tag_content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'(//td[@tabindex="0"])[{i}]'))).text
                

            except Exception as ex:
                print(f"An error occurred while getting the td tag content: {str(ex)}")
                
            # Button'a tıkla ve 1 saniye bekle
            time.sleep(1) 
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)

            # Beliren butonu bul ve tıkla
            popup_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="modalstrap-button-0"]')))
            popup_button.click()
            extra_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/section/div/div/div[2]/section/div[2]/div[2]/div/div[2]/div[2]/div[3]')))
            extra_text = extra_element.text
            # 'description' id'li öğenin yüklenmesini bekle
            description_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'description')))
            
            # öğenin metnini elde et
            description_text = description_element.text
            # Metni dosyaya yazdır
            with open('odevler.txt', 'a') as f:
                f.write(f"Ders Adı: {extra_text}\n")
                f.write(f"Kitap Adı: {td_tag_content}\n")
                f.write(f"Açıklama: {description_text}")
                f.write('\n\n')
    except Exception as ex:
        print(f"An error occurred while clicking on the buttons: {str(ex)}")

except Exception as ex:
    print(f"An error occurred: {str(ex)}")
finally:
    # 5 saniye bekle
    time.sleep(5)
    
    # Tarayıcıyı kapat
    driver.quit()
