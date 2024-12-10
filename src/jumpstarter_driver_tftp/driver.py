from dataclasses import dataclass, field
import os
import tftpy
import threading
from typing import Optional, Union
from jumpstarter.driver import Driver, export

@dataclass(kw_only=True)
class TftpServer(Driver):
    """TFTP Server driver for Jumpstarter"""

    root_dir: str
    host: str = "0.0.0.0"
    port: int = 6969
    server: Optional[tftpy.TftpServer] = field(init=False, default=None)
    server_thread: Optional[threading.Thread] = field(init=False, default=None)

    @classmethod
    def client(cls) -> str:
        return "jumpstarter_driver_tftp.client.TftpServerClient"

    def __post_init__(self):
        super().__post_init__()
        # Ensure root directory exists
        os.makedirs(self.root_dir, exist_ok=True)
        # Create server instance
        self.server = tftpy.TftpServer(self.root_dir)

    def __start_server(self):
        """Helper method to run server in thread"""
        self.server.listen(self.host, self.port)

    @export
    def start(self) -> str:
        """Start the TFTP server"""
        if self.server_thread is not None:
            return "Server already running"

        self.server_thread = threading.Thread(
            target=self.__start_server,
            daemon=True
        )
        self.server_thread.start()
        return "Server started"

    @export
    def stop(self) -> str:
        """Stop the TFTP server"""
        if self.server_thread is None:
            return "Server not running"

        if self.server:
            self.server.stop()
            self.server_thread.join()
            self.server_thread = None
        return "Server stopped"

    @export
    def list_files(self) -> list[str]:
        """List files in TFTP root directory"""
        return os.listdir(self.root_dir)

    @export
    def put_file(self, filename: str, content: Union[str, bytes]) -> str:
        """Put a file directly into the TFTP root directory"""
        try:
            file_path = os.path.join(self.root_dir, filename)
            file_content = content if isinstance(content, bytes) else content.encode('utf-8')
            with open(file_path, 'wb') as f:
                f.write(file_content)
            return f"Created {filename}"
        except Exception as e:
            return f"Error creating {filename}: {str(e)}"

    @export
    def delete_file(self, filename: str) -> str:
        """Delete a file from TFTP root directory"""
        try:
            os.remove(os.path.join(self.root_dir, filename))
            return f"Deleted {filename}"
        except FileNotFoundError:
            return f"File {filename} not found"
        except Exception as e:
            return f"Error deleting {filename}: {str(e)}"

    def close(self):
        """Clean up when driver is closed"""
        self.stop()
        super().close()
