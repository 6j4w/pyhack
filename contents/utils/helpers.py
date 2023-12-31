from errors import IPInvalid, PORTInvalid
from subprocess import check_output, STDOUT, CalledProcessError


def exec(cmd):
    cmd = cmd.rstrip()
    try:
        output = check_output(cmd, stderr=STDOUT, shell=True)
    except CalledProcessError as e:
        output = e.output

    return output


def validateIP(ip):
    splitip = ip.split(".")

    if len(splitip) != 4:
        raise IPInvalid

    for i in splitip:
        if not i.isdigit():
            raise IPInvalid
    return True


def validatePORT(port):
    if not port.isdigit():
        return PORTInvalid

    if not port.isnumeric():
        return PORTInvalid
    """
    #! I don't know why, but these
    #! if statements don't catch anything
    if int(port) <= 0:
        return PORTInvalid

    if int(port) > 65535:
        return PORTInvalid
    """
    return True


def onemessage(target):
    buffer = input("> ")
    target.send(buffer.encode())

    target.send(b"\n> ")

    response = target.recv(4096)
    print(response.decode())


def cmdshell(target):
    buffer = b""

    while True:
        target.send(b"$ ")

        buffer = target.recv(4096)
        if buffer == b"END":
            print("ending")
            break

        target.send(exec(buffer))
