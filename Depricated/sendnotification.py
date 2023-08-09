import base64
import requests
import sqlite3

# Function to send a notification with image from a URL to the server
def send_notification(image_url):
    conn = sqlite3.connect('notifications.db')
    c = conn.cursor()
    c.execute('INSERT INTO notifications (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()
    server_url = "http://localhost:8000"
    headers = {'Content-Type': 'application/json'}

    # Send an HTTP GET request to fetch the image data from the URL
    response = requests.get(image_url)
    image_data = response.content

    image_base64 = base64.b64encode(image_data).decode("utf-8")

    notification_data = {
        "message": "Inappropriate image detected.",
        "image_base64": image_base64
    }

    response = requests.post(server_url, json=notification_data, headers=headers)

    if response.status_code == 200:
        print("Notification sent successfully.")
    else:
        print("Failed to send notification.")

def main():
    # Example image URL for demonstration purposes
    image_url = "https://www.google.com/imgres?imgurl=https%3A%2F%2Fe1.pxfuel.com%2Fdesktop-wallpaper%2F238%2F852%2Fdesktop-wallpaper-masque-luffy-smiling-luffy-smile-thumbnail.jpg&tbnid=VMEXAzZEKs9eSM&vet=12ahUKEwj2sa_3iMqAAxXY6DgGHR1ECqAQMygEegUIARD9AQ..i&imgrefurl=https%3A%2F%2Fwww.pxfuel.com%2Fen%2Fquery%3Fq%3Dluffy%2Bsmile&docid=n98JCM-J_BCkTM&w=350&h=597&q=luffy&ved=2ahUKEwj2sa_3iMqAAxXY6DgGHR1ECqAQMygEegUIARD9AQ"

    send_notification(image_url)

if __name__ == "__main__":
    main()
