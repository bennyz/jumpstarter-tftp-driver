from jumpstarter.common.utils import env

with env() as client:
    client.tftp.start()

    test_content = b"TFTP test!"
    result = client.tftp.put_file("test.txt", test_content)
    print(f"Put file result: {result}")

    files = client.tftp.list_files()
    print(f"Files in TFTP root: {files}")

    print("Cleaning up")
    client.tftp.delete_file("test.txt")
    print("Cleanup complete")

    print(client.tftp.stop())
