import requests
import re
from os import getenv


CHANNEL_ID = getenv("CHANNEL_ID")
BOT_TOKEN = getenv("BOT_TOKEN")


async def Retrieve_Messages(trigger_id: str) :
    
    headers = {
        'authorization': f'Bot {BOT_TOKEN}'  # Include 'Bot' before the token
    }

    # Use the channel ID and message ID in the URL to retrieve a specific message
    url = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)

        # Check if the response indicates success
        if r.status_code == 200:
            json_data = r.json()  # Use the json() method directly on the response object
        else:
            print(f"Unexpected status code: {r.status_code}")

        for message in json_data:
            match = re.search(r'<#(.*?)#>', message['content'])
            if match :
                trig_val = match.group(1)
                if trig_val == trigger_id and "attachments" in message and len(message["attachments"]) > 0:
                    pattern = r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})\.png'
                    message_filename = str(message["attachments"][0]["filename"])
                    message_hash_match = re.search(pattern, message_filename)
                    
                    if message_hash_match:
                        message_hash = message_hash_match.group(1)
                        info = {
                            "message_id": message["id"],
                            "content" : message["content"],
                            "message_hash": message_hash,
                            "url" : message["attachments"][0]["url"],
                            "proxy_url" : message["attachments"][0]["proxy_url"],

                        }
                        return info
                    
        return {"error" : "No match has been found for the given trigger_id"}
        
        

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}") 
        raise e


    