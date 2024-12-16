import ctypes

# Load thư viện động
client_lib = ctypes.CDLL("./libclient.so")

# Khởi tạo client
client_new = client_lib.client_new
client_new.argtypes = [ctypes.c_char_p, ctypes.c_int]
client_new.restype = ctypes.c_void_p

client_delete = client_lib.client_delete
client_send_image = client_lib.client_send_image
client_receive_image = client_lib.client_receive_image_and_decompress

# Tạo đối tượng client
server_ip = b"127.0.0.1"
server_port = 8080
client = client_new(server_ip, server_port)

# Gửi ảnh
client_send_image(client, b"input_image.jpg")

# Nhận và lưu ảnh
client_receive_image(client, b"output_image.jpg")

# Xóa client
client_delete(client)
