#!/usr/bin/env python3
import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

PORT = 8000

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Thêm CORS headers để tránh lỗi khi load local files
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def open_browser():
    """Mở trình duyệt sau 1 giây"""
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}')

def main():
    print("=" * 40)
    print("   Russian Vocabulary Quiz")
    print("   Starting HTTP Server...")
    print("=" * 40)
    print()
    
    # Kiểm tra nếu đang ở đúng thư mục
    if not os.path.exists('index.html'):
        print("❌ Error: index.html not found!")
        print("Please run this script from the project directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Kiểm tra thư mục data
    if not os.path.exists('data'):
        print("⚠️  Warning: 'data' folder not found!")
        print("Creating 'data' folder...")
        os.makedirs('data')
        print("Please add your .txt files to the 'data' folder.")
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Server running at: http://localhost:{PORT}")
            print("📂 Serving files from current directory")
            print("🌐 Opening browser...")
            print("⏹️  Press Ctrl+C to stop the server")
            print()
            
            # Mở trình duyệt trong thread riêng
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Chạy server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("Try closing other applications or use a different port.")
        else:
            print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()