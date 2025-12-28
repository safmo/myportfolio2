# file: decode_cayennelpp_test.py
# https://github.com/smlng/pycayennelpp
# pip install pycayennelpp
# Cayenne LPP Documentation: https://github.com/myDevicesIoT/cayenne-docs/blob/master/docs/LORA.md

from cayennelpp import LppFrame

# Example Cayenne LPP payload as a byte buffer
# Contains temperature, humidity, analog output, and GPS data
buffer = bytearray(b'\x01\x67\x01\x10\x02\x68\x81\x03\x03\x00\x28\x04\x88\x09\x3a\xc8\x02\x59\xef\x00\x3a\x98')

# Decode the payload
frame = LppFrame().from_bytes(buffer)

# Print the decoded data
print("Decoded Cayenne LPP Payload:")
print(frame)