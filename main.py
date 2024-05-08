from banking.script import signing_in
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def main():
    install('plyer')
    install('pyobjus')
    signing_in()


if __name__ == '__main__':
    main()
