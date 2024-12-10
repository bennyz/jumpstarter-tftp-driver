from dataclasses import dataclass

from jumpstarter.client import DriverClient


@dataclass(kw_only=True)
class TftpServerClient(DriverClient):
    """Client interface for TFTP Server driver"""

    def start(self) -> str:
        """Start the TFTP server"""
        return self.call("start")

    def stop(self) -> str:
        """Stop the TFTP server"""
        return self.call("stop")

    def list_files(self) -> list[str]:
        """List files in TFTP root directory"""
        return self.call("list_files")

    def put_file(self, filename: str, content: bytes) -> str:
        """Put a file directly into the TFTP root directory"""
        return self.call("put_file", filename, content)

    def delete_file(self, filename: str) -> str:
        """Delete a file from TFTP root directory"""
        return self.call("delete_file", filename)
