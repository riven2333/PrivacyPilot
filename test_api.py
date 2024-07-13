import requests
import json

BASE_URL = "http://localhost:8000"

def test_cpu_endpoint():
    response = requests.get(f"{BASE_URL}/cpu")
    if response.status_code == 200:
        data = response.json()
        print("CPU Usage:", data)
    else:
        print("Failed to get CPU info. Status code:", response.status_code)

def test_disk_endpoint():
    response = requests.get(f"{BASE_URL}/disk")
    if response.status_code == 200:
        data = response.json()
        print("Disk Usage:", data)
    else:
        print("Failed to get disk info. Status code:", response.status_code)

def test_manifest_endpoint():
    response = requests.get(f"{BASE_URL}/manifest.json")
    if response.status_code == 200:
        data = response.json()
        print("API Manifest:")
        print(data["name"])
    else:
        print("Failed to get manifest. Status code:", response.status_code)

def main():
    print("Testing CPU endpoint:")
    test_cpu_endpoint()
    print("\nTesting Disk endpoint:")
    test_disk_endpoint()
    print("\nTesting Manifest endpoint:")
    test_manifest_endpoint()

if __name__ == "__main__":
    main()