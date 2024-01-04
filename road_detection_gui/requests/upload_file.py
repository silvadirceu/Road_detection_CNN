import requests

def upload_file(chunk):
    api_endpoint = 'http://example.com/upload'
    # Prepare the file for sending
    files = {'file': ('file', uploaded_file, 'multipart/form-data')
    # Send the request to the API
    response = requests.post(api_endpoint, files=files
    # Check the response from the API
    if response.status_code == 200:
        st.write("API request successful")
        st.write(response.json())  # Assuming the API returns JSON data
    else:
        st.write(f"API request failed with status code: {response.status_code}")
        st.write(response.text)  # Display the response text for debugging