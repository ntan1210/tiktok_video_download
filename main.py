import requests
from credentials import *

def find_download_url(video_html, id):
    import json

    start = video_html.find('<script id="SIGI_STATE" type="application/json">')
    if start == -1:
        print("Error Finding START")

    start += len('<script id="SIGI_STATE" type="application/json">')
    end = video_html.find("</script>", start)

    if end == -1:
        print("Error Finding END")

    data = json.loads(video_html[start:end])

    # Use playAddr instead of downloadAddr to remove watermark
    download_add = data["ItemModule"][id]["video"]["playAddr"]
    return download_add

def download_tiktok_video(url):
    print("=> Start downloading video: ", url)
    id = url.split("/")[-1]
    
    video_html = requests.get(url, headers=headers, cookies=cookies).text
    download_url = find_download_url(video_html, id)
    print("=> Done getting download url: ", download_url)

    response = requests.get(
        download_url,
        cookies=cookies,
        headers=headers,
    )

    video_path = f"videos/video_{id}.mp4"
    print("=> Saving video to: ", video_path)
    with open(video_path, 'wb') as fn:
        fn.write(response.content)
    print("DONE")

if __name__ == "__main__":
    urls = ["https://www.tiktok.com/@smidigital6/video/7247482014075456773", "https://www.tiktok.com/@pobimatacc/video/7251555898991168774", "https://www.tiktok.com/@chulamtamdaoquan/video/7277801791616503042"]
    for url in urls:
        download_tiktok_video(url)
    