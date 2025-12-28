# file: encode_cayennelpp_test.py
# https://github.com/smlng/pycayennelpp
# pip install pycayennelpp
# Cayenne LPP Documentation: https://github.com/myDevicesIoT/cayenne-docs/blob/master/docs/LORA.md

import binascii
from cayennelpp import LppFrame

# Create an empty Cayenne LPP frame
frame = LppFrame()

# Add sensor data to the frame
frame.add_temperature(1, 27.2)  # Channel 1: Temperature
frame.add_humidity(2, 64.5)     # Channel 2: Humidity
frame.add_analog_output(3, 0.4) # Channel 3: Analog Output
frame.add_gps(4, 60.48726, 15.40954, 150)  # Channel 4: GPS (latitude, longitude, altitude)

# Encode the frame into a binary payload
buffer = bytes(frame)

# Print the encoded binary payload
print("Cayenne LPP Frame as Bytes:")
print(buffer)

# Print the payload in hexadecimal format (useful for C/C++/C#/embedded systems)
hex_payload = binascii.hexlify(buffer)
print("Payload for C/C++/C#/Embedded:")
print(f'uint8_t tx_buffer[] = {{ {", ".join("0x" + hex_payload[i:i+2].decode() for i in range(0, len(hex_payload), 2))} }};')

# Print the total size of the payload
print(f"Buffer Length: {len(buffer)} bytes")
