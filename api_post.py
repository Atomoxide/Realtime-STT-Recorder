import aiohttp
import asyncio
import os

async def upload_file_async(file_path):
    url = "http://127.0.0.1:9977/api"
    
    # Prepare the file and data for the request
    # file_path = './outputs/test.wav'
    data = {"language": "zh", "model": "base", "response_format": "json"}

    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=os.path.basename(file_path), content_type='audio/wav')
            
            for key, value in data.items():
                form_data.add_field(key, value)
            
            # os.remove(file_path)
            # Perform the POST request asynchronously
            async with session.post(url, data=form_data, timeout=aiohttp.ClientTimeout(total=600)) as response:
                # Handle the response
                if response.status == 200:
                    result = await response.json()
                    print("Upload successful:", result)
                    return result, file_path
                else:
                    print(f"Failed to upload. Status code: {response.status}")
                    return None, file_path
