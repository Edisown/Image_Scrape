import time
import os
import requests
import io
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # Importing ActionChains
from PIL import Image

# Specify the path to your ChromeDriver
PATH = "C:/Users/ediso/Desktop/Image_Scrape/chromedriver.exe"

# Create a Service object and initialize the WebDriver
service = Service(PATH)
wd = webdriver.Chrome(service=service)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?sca_esv=afaa2ac8252b60e9&rlz=1C1JJTC_enPH1081PH1081&q=orange+fruit&udm=2&fbs=AEQNm0BglSNKPbDQcL4Et01QEIYvg5bRO_M3ywqCa9xtNRWwAm_qOe_c9lI78Uqe-Ht_ugkYVWG4KbuNih5Uc00qY9UsbxF5VDU6oWu6wKyMxQ4JqagJJK-QQoCSu8w72odwBSkF0Dty4JiRehICCf1FuOKpbUcU7LBCFyYaFzUs-fthpG_D_JAWOEC_Si5U8dtbrZHBJo9rnWf7VYPPoxisFPWFcZbF-w&sa=X&ved=2ahUKEwjU38rUgaSKAxVvr1YBHXm4Kw8QtKgLegQIFhAB&biw=1920&bih=945&dpr=1"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        # Use XPath to select img elements
        thumbnails = wd.find_elements(By.XPATH, "//img[contains(@src, 'https')]")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                # Use ActionChains to click on the image thumbnail more reliably
                actions = ActionChains(wd)
                actions.move_to_element(img).click().perform()  # Perform the click action
                time.sleep(delay)  # Wait for the full-size image to load
            except Exception as e:
                print(f"Error clicking image: {e}")
                continue

            # Find the full-size image
            images = wd.find_elements(By.XPATH, "//img[contains(@class, 't0fcAb')]")  # Full image class
            for image in images:
                image_url = image.get_attribute('src')
                if image_url and 'http' in image_url:
                    if image_url not in image_urls:
                        image_urls.add(image_url)
                        print(f"Found {len(image_urls)} images.")
            if len(image_urls) >= max_images:
                break

        # If we've reached the desired number of images, stop scrolling
        if len(image_urls) >= max_images:
            break

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
        print(f"Downloaded {file_name}")
    except Exception as e:
        print('FAILED -', e)

# Ensure the folder exists
if not os.path.exists("images/orange/"):
    os.makedirs("images/orange/")

# Get image URLs
urls = get_images_from_google(wd, 1, 6)

# Download images
for i, url in enumerate(urls):
    download_image("images/orange/", url, str(i) + ".jpg")

wd.quit()
