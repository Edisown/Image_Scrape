import requests
import os

# unsplash api key
access_key = 'QceyE7XHmQvmbqbj0EdFaP7xv1yoeak7uEkDTbZSTAA'


save_path = "C:/Users/ediso/Desktop/Image_Scrape/images/lemon"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# set maximum number of downloads
max_images = 500
batch_size = 30  # max number of images per request

# needed batches
total_batches = (max_images // batch_size) + (1 if max_images % batch_size else 0)

# counter
image_count = 0

# fetch images per batches
for batch in range(total_batches):
    page_number = batch + 1
    url = f'https://api.unsplash.com/search/photos?query=lemon&per_page={batch_size}&page={page_number}&client_id={access_key}' # depends on what dataset you are gathering
    response = requests.get(url)

    if response.status_code == 200:
        images = response.json()['results']

        # download the image in current batch
        for index, image in enumerate(images):
            if image_count >= max_images:
                break  # stop once it reaches the max images

            try:
                img_url = image['urls']['regular']

                # send a get requests
                img_data = requests.get(img_url).content

                # save image to the directory
                with open(f"{save_path}/lemon_{image_count + 1}.jpg", "wb") as file:
                    file.write(img_data)
                print(f"Downloaded image_{image_count + 1}.jpg")
                image_count += 1
            except Exception as e:
                print(f"Could not download image {image_count + 1}: {e}")
    else:
        print(f"Failed to fetch batch {batch + 1}. Status code: {response.status_code}")

print(f"Total images downloaded: {image_count}")
