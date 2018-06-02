import os


def test_proxy(proxy):
    try:
        a = os.popen("ping " + proxy).read(100)
        # a.close()
        print(a)
        return a.split("\n")[1].split(" ")[-1].split("=")[1]
    except IndexError:
        return 0

print(test_proxy("192.168.1.10"))