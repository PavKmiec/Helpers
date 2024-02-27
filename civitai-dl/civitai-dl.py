import requests
import json
import time
from urllib.parse import quote
from pathlib import Path
from tqdm import tqdm

# Function to read the Secure-civitai-token from a file
def read_token_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()  # Remove any potential whitespace
    except FileNotFoundError:
        print("Token file not found.")
        return None

# Define the headers for the request
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://civitai.com",
    "Content-Type": "application/json",
    "DNT": "1",
    "Alt-Used": "civitai.com",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers"
}

def download_image_and_metadata(item, username):
    image_is_new = False
    base_image_url = "https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/" # TODO: get this automatically 
    image_url = f"{base_image_url}{item['url']}/original=true/"

    user_dir = Path(f"users/{username}")
    user_dir.mkdir(parents=True, exist_ok=True)

    image_path = user_dir / f"{item['url']}.png"
    metadata_path = user_dir / f"{item['url']}.json"

    if image_path.exists() and metadata_path.exists():
        print(f"Both image and metadata exist for {item['url']}, skipping.")
    else:
        image_is_new = True
        if not image_path.exists():
            response = requests.get(image_url, stream=True)
            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024
            
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(image_path, 'wb') as f:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    f.write(data)
            progress_bar.close()
            
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print(f"ERROR, something went wrong downloading {image_url}")

        if not metadata_path.exists():
            with open(metadata_path, 'w') as f:
                json.dump(item, f, indent=4)

    return image_url, image_is_new

def fetch_images(username, cursor=None):
    # Base URL and endpoint
    base_url = "https://civitai.com"
    endpoint = "/api/trpc/image.getInfinite"

    # For the initial request, include 'meta'; for subsequent requests, exclude 'meta'
    if cursor is None:  # Initial request
        payload = {
            "json": {
                "period": "AllTime",
                "sort": "Newest",
                "view": "feed",
                "types": ["image"],
                "username": username,
                "withMeta": False,
                "cursor": cursor,  # This will be None for the initial request
                "authed": True
            },
            "meta": {
                "values": {
                    "cursor": ["undefined"]
                }
            }
        }
    else:  # Subsequent requests
        payload = {
            "json": {
                "period": "AllTime",
                "sort": "Newest",
                "view": "feed",
                "types": ["image"],
                "username": username,
                "withMeta": False,
                "cursor": cursor,  # This will have the nextCursor value for subsequent requests
                "authed": True
            }
        }

    # Encode the payload as a URL parameter
    encoded_input = 'input=' + quote(json.dumps(payload))
    url = f"{base_url}{endpoint}?{encoded_input}"

    response = requests.get(url, headers=headers, cookies={"__Secure-civitai-token": secure_civitai_token})

    return response


# Main script starts here
username = input("Enter the username: ")
token_file_path = 'token.txt'
secure_civitai_token = read_token_from_file(token_file_path)

if secure_civitai_token:
    cookies = {"__Secure-civitai-token": secure_civitai_token}
    cursor = None
    file_path = f"{username}_image_urls.txt"


    while True:
        response = fetch_images(username, cursor)
        if response.status_code == 200:
            data = response.json()
            cursor = data["result"]["data"]["json"].get("nextCursor")
            print(f"Next cursor: {cursor}")

            with open(file_path, 'a') as url_file:
                for item in data["result"]["data"]["json"]["items"]:
                    image_url, image_is_new = download_image_and_metadata(item, username)
                    # Only save URL if the image is new
                    if image_is_new:
                        url_file.write(image_url + "\n")

            print(f"Processed items for cursor: {cursor}")

            if not cursor:  # If there is no next cursor, break the loop
                print("No more items to process.")
                break
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            break
        print("Waiting for 2 seconds...")
        time.sleep(2)
else:
    print("Secure-civitai-token not available. Exiting...")