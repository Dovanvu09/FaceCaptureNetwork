#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <vector>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

using namespace std;
using namespace cv;

extern "C" {

    // Class client được cập nhật để sử dụng chung với ctypes
    class client {
    private:
        int sock;
        struct sockaddr_in server_addr;

    public:
        // Constructor mở kết nối socket đến server
        client(const char* server_ip, int server_port) {
            sock = socket(AF_INET, SOCK_STREAM, 0);
            if (sock < 0) {
                cerr << "Error: Unable to create socket" << endl;
                exit(1);
            }

            // Cấu hình địa chỉ server
            server_addr.sin_family = AF_INET;
            server_addr.sin_port = htons(server_port);  // Cổng server (chuyển đổi theo chuẩn mạng)
            server_addr.sin_addr.s_addr = inet_addr(server_ip);  // Địa chỉ IP của server (chuyển đổi từ string)

            if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
                cerr << "Error: Unable to connect to server" << endl;
                exit(1);  // thoát ra nếu không thể kết nối tới server
            }
            cout << "Connected to server successfully" << endl;
        }

        ~client() {
            close(sock);
        }

        // Phương thức gửi ảnh nén qua socket
        void send_image(const char* image_path) {
            // Đọc ảnh vào bộ nhớ bằng OpenCV
            Mat image = imread(image_path, IMREAD_COLOR);
            if (image.empty()) {
                cerr << "Error: Unable to open image file." << endl;
                return;
            }

            // Nén ảnh thành chuỗi byte (JPEG hoặc PNG)
            vector<uchar> buf;
            bool result = imencode(".jpg", image, buf);  // Nén ảnh dưới dạng JPEG
            if (!result) {
                cerr << "Error: Failed to encode image." << endl;
                return;
            }

            // Gửi dữ liệu ảnh nén qua socket
            send(sock, buf.data(), buf.size(), 0);
            cout << "Image sent successfully." << endl;
        }

        // Phương thức nhận ảnh từ server và giải nén
        void receive_image_and_decompress(const char* output_image_path) {
            const int buffer_size = 4096;
            char buffer[buffer_size];
            vector<char> image_data;  // Dùng vector để lưu trữ dữ liệu nhận được từ server

            int bytes_received = 0;
            while ((bytes_received = recv(sock, buffer, buffer_size, 0)) > 0) {
                image_data.insert(image_data.end(), buffer, buffer + bytes_received);
            }

            if (bytes_received < 0) {
                cerr << "Error: Failed to receive data from server." << endl;
                return;
            }

            // Giải mã ảnh từ chuỗi byte nhận được
            vector<uchar> data(image_data.begin(), image_data.end());
            Mat received_image = imdecode(data, IMREAD_COLOR);  // Giải mã ảnh từ byte array

            if (received_image.empty()) {
                cerr << "Error: Failed to decode image." << endl;
                return;
            }

            // Lưu ảnh vào tệp
            imwrite(output_image_path, received_image);
            cout << "Image saved successfully to " << output_image_path << endl;
        }

        // Phương thức gửi yêu cầu xem lại ảnh hoặc phiên làm việc
        void send_request_to_view_images(const char* session_id) {
            // Tạo thông điệp yêu cầu: yêu cầu luôn là "view_image" và kèm theo session_id
            string request_message = string("view_image") + ":" + string(session_id);

            // Gửi yêu cầu qua socket
            send(sock, request_message.c_str(), request_message.size(), 0);
            cout << "Request sent: " << request_message << endl;
    }

    };

    // Export các phương thức để Python có thể gọi
    client* client_new(const char* server_ip, int server_port) {
        return new client(server_ip, server_port);
    }

    void client_delete(client* c) {
        delete c;
    }

    void client_send_image(client* c, const char* image_path) {
        c->send_image(image_path);
    }

    void client_receive_image_and_decompress(client* c, const char* output_image_path) {
        c->receive_image_and_decompress(output_image_path);
    }

    void client_send_request_to_view_images(client* c, const char* session_id) {
        c->send_request_to_view_images(session_id);
    }

}
