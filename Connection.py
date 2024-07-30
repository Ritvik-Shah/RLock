import bluetooth
import Vars
import socket

def send_file(file_path, target_mac_address):
    try:
        # Create a Bluetooth RFCOMM socket
        client_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

        # Connect to the target device
        client_socket.connect((target_mac_address, 1))  # Assuming RFCOMM channel 1 for simplicity

        # Open the file for reading
        with open(file_path, 'rb') as file:
            # Send the file data
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.send(data)

        print("File sent successfully.")

    except Exception as e:
        print("Error:", e)

    finally:
        # Close the socket
        client_socket.close()

# Example usage:
if __name__ == "__main__":
    file_path = Vars.unlock_file
    target_mac_address = '1C:F8:D0:34:3A:82'
    send_file(file_path, target_mac_address)
