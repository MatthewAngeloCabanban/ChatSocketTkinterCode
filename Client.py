import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

# Client configuration
HOST = '127.0.0.1'
PORT = 55555

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Tkinter setup
window = tk.Tk()
window.title("Chat App")

# Message display area
chat_display = scrolledtext.ScrolledText(window, width=40, height=10)
chat_display.pack(padx=10, pady=10)

# Message input field
message_entry = Entry(window, width=30)
message_entry.pack(padx=10, pady=10)


# Send button
def send_message():
    message = message_entry.get()
    client_socket.send(message.encode())
    message_entry.delete(0, tk.END)


send_button = Button(window, text="Send", command=send_message)
send_button.pack(padx=10, pady=10)


# Receive messages from the server
def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            chat_display.insert(tk.END, message + '\n')
        except:
            # Handle disconnection
            break


# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# Run the Tkinter main loop
window.mainloop()
