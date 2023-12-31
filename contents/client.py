# This is the client

import socket as s
from sys import argv, path
from os import getcwd

path.insert(0, f"{getcwd()}/utils")
from helpers import validateIP, validatePORT  # noqa E402
from errors import IPInvalid, PORTInvalid  # noqa E402

ip = ""
port = 0


def validateSocket():
    if len(argv) < 3:
        raise IndexError

    if validateIP(argv[1]):
        print("[+] IP validated")
    if validatePORT(argv[2]):
        print("[+] Port validated")


def main():
    with s.socket(s.AF_INET, s.SOCK_STREAM) as target:
        try:
            validateSocket()
            ip = argv[1]
            port = int(argv[2])

            print(f"Attempting connection to {ip}:{port}")
            target.connect((ip, port))
            print(f"Connected to {ip}:{port}.")

            response = b""
            while True:
                response = target.recv(4096)
                print(response.decode(), end="")

                buffer = input("")
                target.send(buffer.encode())

        except IPInvalid:
            print("[FATAL] IP address invalid. Example: 0.0.0.0")
        except PORTInvalid:
            print("[FATAL] IP address invalid. Example: 1234")
        except ConnectionRefusedError:
            print("[FATAL] Sorry, connection refused.")
        except OverflowError:
            print("[FATAL] Port must be 0-65535.")
        except IndexError:
            print("Usage: python(3) [IP] [PORT]")
        except (KeyboardInterrupt, EOFError):
            print("Exiting due to keyboard interrupt.")
            target.send(b"END")
            _ = target.recv(4096)
            target.close()


if __name__ == "__main__":
    main()
