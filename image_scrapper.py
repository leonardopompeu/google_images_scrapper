from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

#image_url = 'https://www.petz.com.br/blog/wp-content/uploads/2020/08/cat-cafe-pet.jpg'

#driver.get(image_url)


def get_images_url(driver, delay, max_images):
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    
    url = 'https://www.google.com/search?q=dogs&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiPmY3cwav8AhWpq5UCHSvIAMIQ_AUoAXoECAEQAw&biw=1366&bih=664'

    driver.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CLASS_NAME, 'Q4LuWd')

        for img in thumbnails[len(image_urls)+skips: max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            images = driver.find_elements(By.CLASS_NAME, 'n3VNCb')

            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
    return image_urls


def download_image(download_path, url, filename):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        image = image.convert('RGB')
        filepath = download_path + filename

        with open(filepath, 'wb') as f:
            image.save(f, 'JPEG')
    except Exception as e:
        print('Failed - ', e)

#download_image('', image_url, 'test.jpg')

urls = get_images_url(driver, 1, 3)
driver.quit()
print(urls)
print(len(urls))

for i, url in enumerate(urls):
    download_image('imgs/', url, str(i)+'.jpg')

