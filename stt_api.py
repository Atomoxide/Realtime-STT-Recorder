import aiohttp
import asyncio
import os

async def upload_file_async(file_path):
    stt_url = "http://127.0.0.1:9977/api"
    namazu_url = "http://127.0.0.1:2019/command"
    
    # Prepare the file and data for the request
    # file_path = './outputs/test.wav'
    data = {"language": "zh", "model": "small", "response_format": "json"}

    async with aiohttp.ClientSession() as session:
        with open(file_path, 'rb') as file:
            form_data = aiohttp.FormData()
            form_data.add_field('file', file, filename=os.path.basename(file_path), content_type='audio/wav')
            
            for key, value in data.items():
                form_data.add_field(key, value)
            
            # os.remove(file_path)
            # Perform the POST request asynchronously
            # print("invoking")
            async with session.post(stt_url, data=form_data, timeout=aiohttp.ClientTimeout(total=30)) as response:
                try:
                    # Handle the response
                    if response.status == 200:
                        result = await response.json()
                        # print("Upload successful.")
                        # text = result.get("data")[0].get("text")
                        text = result.get("data")
                        if text != "请转录为中文简体 " and text:
                            command = f"/p {text}"
                            print(command)
                            async with session.post(namazu_url, data=command, timeout=aiohttp.ClientTimeout(total=10)) as namazu_response:
                                if namazu_response.status != 200:
                                    print(f"Failed to post to Namazu. Status code: {response.status}")
                        else:
                            print("Null Text")
                    else:
                        print(f"Failed to upload. Status code: {response.status}")
                except asyncio.TimeoutError:
                    print("Time out!")
                finally:
                    os.remove(file_path)
