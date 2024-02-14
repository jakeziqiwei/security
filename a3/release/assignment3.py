import urllib.request
import base64
import binascii
from pymd5 import md5, padding

from problem1 import ctxts_hex, ctxts_bin
from problem2 import KEY, get_user_url, query_url

################################################################################
#
# Starter file for UChicago CMSC 23200 Assignment 3, Winter 2024
#
################################################################################


################################################################################
# PROBLEM 1 SOLUTION
################################################################################

# Add your helper code for solving Problem 1 here.

# Submission function for grading


def xor(c1, c2):
    # general xor function that xor two bytearray together
    return bytes(x ^ y for x, y in zip(c1, c2))


def createXorList(ctxts_bin):
    # Loop through the 4 cipher texts and take the xor combination of each other. This gives us 6 p ⊕ p
    xor_list = []
    for i in range(len(ctxts_bin)):
        for j in range(i+1, len(ctxts_bin)):
            xor_list.append(xor(ctxts_bin[i], ctxts_bin[j]))
    return xor_list


def cribAttack(guess, xor_list, i):
    # given a guess, I print the xor of it at each location of 1 p ⊕ p in the xor_list.
    # I also modified this function to do it one at a time.
    # I used this to see if there are english words that I can update the guess and keep going
    # ie, I used "The " for the combination of ctext1 and ctext2 by using cribAttack("The ", xor_list, 0)
    # and found that the word "The " appears in one of the string and it translates to "Libr"
    # I now go backwards with guess "Libr" and found the next parts the "The "
    # I used a physical notebook to keep track of my guesses and positions.
    # Repeat this till I get something that seems like English
    l = 0
    r = len(guess)
    while r < len(xor_list[i]):
        print("xor" + str(i) + "from " + str(l) + " to " + str(r))
        print(xor(xor_list[i][l:r+1]))
        l += 1
        r += 1


def findKey(p, c):
    # I was able to semi guess one of the plain text
    # and I used this function to create the key
    return xor(p, c)


def decryptAll(key, ctxts_bin):
    # I used the key from the last function to decrpyt all
    for i in ctxts_bin:
        print(xor(ctxts_bin[i], key))


# Overall Process
# 1) create all combination of cipher text with createXorList()
# 2) use cribAttack() with english word guess like [the, and, of, with, like] and repeatly update the guess and narrowed down the plain text
# 3) Used one of the cipher to xor one of my plain text guesses that is close enough to create the key
# 4) decript all and use logic to fill in the English and Grant's post on ed.

def problem1():
    # Fill in this array with the four decoded plaintexts *in order*
    # no further implementation required in this function
    ptxts = ["Libraries pulled through, of course, but then the rise of the internet renewed fears of obsolescence. So far, the internet has not killed libraries either. But the percentage of higher-education budgets dedicated to libraries has been dwindling since the 1980s, and at many institutions there's been a corresponding drop in reported spending on print materials.",
             "The game is most gratifying when players devise the canniest, most unexpected, and most unnecessary ways to trick the poor villagers whose unfortunate assignment it is to share a world with this wicked waterfowl. Sneaking and cheating are game-play elements that get rewarded; being a bad goose is what it must feel like to be a card sharp.\n"
             "PhD student Shawn Shan and alumni Emily Wenger and Jenna Cryan were named to the Forbes 30 Under 30 list for 202s. Forbes editors reached out to the team for their work on Glaze, a tool for artists to protect their creative property against AI models. This is the first time the Department of Computer Science has had students make the list.\n",
             "He injected a piece of lasagna with heroin for a work titled lasagna on heroin, and he drove his aunts car from her house outside Miami and park.d it in front of the Bass Museum of Art for a piece called my aunts car. There is a bit of Well, what happens if to his work. Happily ever after.\n",
             ]
    return ptxts

################################################################################
# PROBLEM 2 SOLUTION
################################################################################


def problem2(cnet):
    url = get_user_url(cnet)
    params_strs = url.lstrip(b'http://www.flickur.com/?')
    ps = list(map(lambda x: x.split(b'='), params_strs.split(b'&')))
    params = {p[0]: p[1] for p in ps if len(p) >= 2}
    amp_index = params_strs.find(b'&')
    print(params)
    # everything after the first &
    # uname=<your-cnet>&role=user
    input_len = 8 * (sum(len(i) for i in list(params.keys())[
        1:]) + sum(len(i) for i in list(params.values())[1:]) + 3)
    # Fill in your solution to Problem 2 here
    # goal: return a new URL causes query_url(...) to return success for an admin login
    for key in range(128, 512+1, 8):
        # need to figure out old message    
        new_input = key + input_len
        blocks = new_input + 65
        h = md5(state=(bytes.fromhex(params[b'api_tag'].decode('utf-8'))),
                count=((blocks // 512+1) * 512))
        h.update(b'&role=admin')
        new_tag = h.hexdigest()
        new_url = (b"http://www.flickur.com/?api_tag=") + new_tag.encode('utf-8') + \
            b"&uname=ziqiwei&role=user" + \
            padding(new_input) + b'&role=admin'
        if query_url(new_url) == b"Admin Login Success":
            return new_url

    return "oh no"


################################################################################

# Code below here will be run if you execute 'python4 assignment3.py'.
# This code here won't be graded, and your code above shouldn't depend on it.
if __name__ == "__main__":
    print(problem2(b"ziqiwei"))
    # optional driver code here, e.g., to help test your solution to Problem 2
    exit()
