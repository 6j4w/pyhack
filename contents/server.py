# This is the server

import socket as s
from sys import argv, path
from os import getcwd
from threading import Thread

path.insert(0, f"{getcwd()}/utils")
from helpers import validateIP, validatePORT, onemessage, cmdshell  # noqa E402
from errors import IPInvalid, PORTInvalid  # noqa E402


ip = ""
port = 0


def validateSocket():
    if len(argv) < 3:
        raise IndexError
    if validateIP(argv[2]):
        print("[+] IP validated")
    if validatePORT(argv[1]):
        print("[+] Port validated")


def handle_client(target, initationmess):
    print(f"Function: {initationmess}")
    if initationmess == "ONEMESSAGE":
        onemessage(target)
    elif initationmess == "SHELL":
        print("shelly")
        cmdshell(target)

    target.close()
    print("Connection ended.")


def main():
    with s.socket(s.AF_INET, s.SOCK_STREAM) as server:
        client = None
        try:
            validateSocket()
            ip = argv[2]
            port = int(argv[1])

            print(f"Listening on {ip}:{port}")
            server.bind((ip, port))
            server.listen(5)
            server.settimeout(5)
            while True:
                client, addr = server.accept()
                print("Connected")

                client_thread = Thread(
                    target=(handle_client),
                    args=(
                        client,
                        "SHELL",
                    ),
                )
                client_thread.start()

        except IPInvalid:
            print("[FATAL] IP address invalid. Example: 0.0.0.0")
        except PORTInvalid:
            print("[FATAL] IP address invalid. Example: 1234")
        except ConnectionRefusedError:
            print("[FATAL] Sorry, connection refused.")
        except OverflowError:
            print("[FATAL] Port must be 0-65535.")
        except IndexError:
            print("Usage: python(3) [PORT] [IP]")
        except ConnectionResetError:
            print("Connection ended in unusual circumstances")
        except (s.error, BrokenPipeError):
            print("Client disconnected.")
            if client:
                client.close
        except (KeyboardInterrupt, EOFError):
            print("Exiting due to keyboard interrupt.")
            client.send(b"END")
            if client:
                client.close()


if __name__ == "__main__":
    main()
