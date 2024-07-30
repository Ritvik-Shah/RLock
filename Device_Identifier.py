import uuid
import platform
import hashlib
import psutil
import win32file

def get_disk_serial_numbers():
    serial_numbers = []
    if platform.system() == 'Windows':
        for partition in psutil.disk_partitions():
            try:
                drive_letter = partition.mountpoint[:2]
                volume_name = win32file.GetVolumeNameForVolumeMountPoint(drive_letter)
                serial_number = win32file.GetVolumeInformation(volume_name)[1]
                serial_numbers.append(str(serial_number))
            except Exception as e:
                print(f"Error: {e}")
    elif platform.system() == 'Linux':
        # You may need to customize this part for Linux systems
        pass
    return serial_numbers

def get_unique_identifier():
    # Generate a UUID
    device_uuid = uuid.uuid4()

    # Get system information
    system_info = platform.uname()

    # Get hardware serial numbers
    serial_numbers = get_disk_serial_numbers()

    # Combine system information and serial numbers
    combined_info = f"{system_info.node}-{system_info.processor}-{system_info.system}-{'-'.join(serial_numbers)}"

    # Generate a hash of the combined information
    unique_hash = hashlib.sha256(combined_info.encode()).hexdigest()

    return unique_hash


