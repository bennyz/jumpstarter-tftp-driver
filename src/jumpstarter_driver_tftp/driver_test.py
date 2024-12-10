import os
import tempfile
import time
import tftpy
from jumpstarter.common.utils import serve
from jumpstarter_driver_tftp.driver import TftpServer

def test_tftp_server():
    # Create temporary directory for TFTP root
    with tempfile.TemporaryDirectory() as tftp_root:
        # Create test file
        test_file = os.path.join(tftp_root, "test.txt")
        with open(test_file, "w") as f:
            f.write("Test content")

        # Create and start server
        server = TftpServer(root_dir=tftp_root, port=6969)  # Using non-privileged port for testing

        with serve(server) as client:
            # Start server
            assert client.start() == "Server started"

            # Give server time to start
            time.sleep(1)

            # List files
            files = client.list_files()
            assert "test.txt" in files

            # Create TFTP client and download file
            tftp_client = tftpy.TftpClient('localhost', 6969)

            # Create temp dir for downloaded files
            with tempfile.TemporaryDirectory() as download_dir:
                download_path = os.path.join(download_dir, "downloaded.txt")

                # Download file
                tftp_client.download("test.txt", download_path)

                # Verify content
                with open(download_path, "r") as f:
                    assert f.read() == "Test content"

                # Upload new file
                upload_file = os.path.join(download_dir, "upload.txt")
                with open(upload_file, "w") as f:
                    f.write("Uploaded content")

                tftp_client.upload("upload.txt", upload_file)

                # Verify upload
                assert "upload.txt" in client.list_files()

                # Delete file
                assert "Deleted upload.txt" in client.delete_file("upload.txt")
                assert "upload.txt" not in client.list_files()

            # Stop server
            assert client.stop() == "Server stopped"
