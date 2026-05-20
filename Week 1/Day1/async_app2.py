import asyncio
import aiohttp
import time

urls = [
    "https://images.pexels.com/photos/1540258/pexels-photo-1540258.jpeg",        # pexels
    "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg",  # wikimedia
    "https://images.unsplash.com/photo-1501854140801-50d01698950b",               # unsplash
    "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_demonstration_1.png", # wikimedia
    "https://www.w3schools.com/css/img_5terre.jpg",                                # w3schools
    "https://picsum.photos/seed/picsum/800/600",                                   # picsum
    "https://images.pexels.com/photos/2662116/pexels-photo-2662116.jpeg",         # pexels
]

filename=[]
for i in range(7):
    filename.append(f"image{i}")

# Complete Asyncrounus approach

start = time.time()

def get_tasks(session):
    tasks=[]
    for url in urls:
        tasks.append(session.get(url,ssl=False))
    return tasks


async def down():
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session)
        responses = await asyncio.gather(*tasks)

        print(len(tasks))

        for i,response in enumerate(responses):
            
            import os

            BASE_DIR = os.path.dirname(__file__)

            SAVE_FOLDER = os.path.join(BASE_DIR, "Saved_files")

            os.makedirs(SAVE_FOLDER, exist_ok=True)

            path = os.path.join(SAVE_FOLDER, filename[i])

            with open(path, "wb") as f:
                f.write(await response.read())

            print(f"Downloaded {filename[i]}")
    

asyncio.run(down())

print("Time:", time.time() - start)