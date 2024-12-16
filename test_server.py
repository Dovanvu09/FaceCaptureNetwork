import ctypes

# Load thư viện động
server_lib = ctypes.CDLL("./libserver.so")

# Định nghĩa các phương thức
server_new = server_lib.server_new
server_new.restype = ctypes.c_void_p

server_delete = server_lib.server_delete
server_delete.argtypes = [ctypes.c_void_p]

server_accept = server_lib.server_accept_connection
server_accept.argtypes = [ctypes.c_void_p]

server_receive = server_lib.server_receive_image
server_receive.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

server_send = server_lib.server_send_image
server_send.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

server_handle = server_lib.server_handle_request
server_handle.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

# Khởi tạo server
server = server_new()

# Chấp nhận kết nối
server_accept(server)

# Nhận ảnh từ client
server_receive(server, b"received_image.jpg")

# Gửi ảnh đến client
server_send(server, b"response_image.jpg")

# Gửi ảnh dựa trên session ID
server_handle(server, b"123")

# Xóa server
server_delete(server)
