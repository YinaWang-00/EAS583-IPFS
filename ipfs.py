import requests
import json
import os

def pin_to_ipfs(data):
    assert isinstance(data,dict), f"Error pin_to_ipfs expects a dictionary"
    #YOUR CODE HERE
    url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

    headers = {
        "Authorization": f"Bearer {os.environ['PINATA_JWT']}",
        "Content-Type": "application/json"
    }

    payload = {
        "pinataContent": data
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )
    response.raise_for_status()

    cid = response.json()["IpfsHash"]

    return cid

def get_from_ipfs(cid,content_type="json"):
    assert isinstance(cid,str), f"get_from_ipfs accepts a cid in the form of a string"
    #YOUR CODE HERE
    gateways = [
        "https://ipfs.io/ipfs/",
        "https://gateway.pinata.cloud/ipfs/"
    ]

    for gateway in gateways:
        try:
            response = requests.get(
                gateway + cid,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()
            if isinstance(data, dict):
                break
        except (requests.RequestException, ValueError):
            continue
    else:
        raise RuntimeError(f"Failed to retrieve JSON from IPFS: {cid}")

    assert isinstance(data,dict), f"get_from_ipfs should return a dict"
    return data
