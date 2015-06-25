from hashlib import md5

key = 'guoku'
chars = [
		"a" , "b" , "c" , "d" , "e" , "f" , "g" , "h" ,
        "i" , "j" , "k" , "l" , "m" , "n" , "o" , "p" ,
        "q" , "r" , "s" , "t" , "u" , "v" , "w" , "x" ,
        "y" , "z" , "0" , "1" , "2" , "3" , "4" , "5" ,
        "6" , "7" , "8" , "9" , "A" , "B" , "C" , "D" ,
        "E" , "F" , "G" , "H" , "I" , "J" , "K" , "L" ,
        "M" , "N" , "O" , "P" , "Q" , "R" , "S" , "T" ,
        "U" , "V" , "W" , "X" , "Y" , "Z"
		]


def shortURL(string):

    res = list()
    s = md5(key + string).hexdigest()
    for i in range(0, 4):
        hexint = int(s[i * 8:(i+1) * 8], 16) & 0x3fffffff
        outChars = ""
        for j in range(0, 6):
            index = hexint & 0x0000003D
            outChars += chars[index]
            hexint = hexint >> 5
        res.append(outChars)

    return res

if __name__ == '__main__':
    print shortURL('fdsafdsa')


__author__ = 'xiejiaxin'
