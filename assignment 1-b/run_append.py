import os

text = "bloom"  # modify this variable
filename = "/home/ziqiwei/random"  # modify this variable; give the full path

for _ in range(3000):
    os.system("/home/grant/append " + text + " " + filename)
