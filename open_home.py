import subprocess


def open_home():
    with open('main.py') as f:
        exec(f.read(), globals())
        
if __name__ == '__main__':
    open_home()
