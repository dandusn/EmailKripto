class Fiestel:
    left = ''
    right = ''
    rowtrp = [3, 1, 0, 2]
    coltrp = [2, 0, 3, 1]
    sboxkey = [[]]
    sbox1 = [[]]

    def __init__(self, isdekrip):
        self.sboxkey = [[183, 59, 68, 98, 83, 6, 214, 23, 10, 157, 174, 173, 202, 166, 70, 85],
                   [7, 137, 163, 69, 221, 63, 177, 210, 132, 178, 244, 18, 242, 237, 100, 228],
                   [95, 80, 58, 43, 161, 99, 187, 64, 61, 110, 117, 33, 22, 1, 19, 66],
                   [220, 230, 209, 30, 118, 184, 175, 205, 109, 196, 113, 169, 129, 253, 65, 55],
                   [128, 49, 238, 182, 48, 193, 243, 146, 152, 81, 96, 247, 190, 153, 232, 188],
                   [131, 160, 208, 147, 36, 212, 107, 46, 37, 3, 56, 151, 240, 162, 9, 97],
                   [168, 254, 122, 201, 142, 20, 180, 211, 86, 34, 171, 165, 179, 75, 215, 133],
                   [140, 150, 8, 130, 74, 41, 218, 194, 185, 106, 21, 25, 0, 62, 90, 108],
                   [144, 156, 54, 28, 200, 60, 235, 155, 57, 35, 186, 248, 217, 189, 112, 47],
                   [24, 125, 103, 111, 223, 206, 127, 16, 116, 172, 236, 170, 102, 104, 195, 138],
                   [12, 123, 213, 13, 250, 32, 203, 241, 149, 120, 191, 114, 234, 17, 42, 105],
                   [53, 245, 29, 207, 231, 93, 229, 50, 135, 252, 164, 255, 124, 121, 45, 115],
                   [139, 15, 141, 89, 192, 199, 233, 87, 239, 51, 71, 145, 84, 26, 77, 52],
                   [198, 27, 94, 72, 67, 2, 4, 40, 204, 88, 251, 148, 143, 5, 158, 159],
                   [219, 249, 176, 11, 79, 167, 91, 101, 92, 225, 73, 136, 39, 154, 38, 216],
                   [126, 82, 226, 181, 134, 14, 224, 222, 227, 31, 119, 197, 44, 246, 76, 78]]

        self.sbox1 = [[179, 219, 159, 217, 58, 234, 113, 62, 240, 199, 115, 232, 24, 72, 13, 83],
                 [130, 195, 16, 221, 70, 175, 64, 200, 231, 11, 119, 101, 138, 167, 92, 17],
                 [205, 239, 136, 32, 106, 152, 27, 137, 6, 111, 206, 30, 196, 154, 73, 9],
                 [208, 71, 112, 144, 45, 51, 123, 63, 117, 25, 96, 120, 104, 81, 94, 93],
                 [220, 249, 61, 86, 170, 108, 23, 246, 56, 215, 190, 156, 98, 77, 211, 100],
                 [202, 52, 80, 125, 183, 75, 60, 242, 49, 187, 103, 177, 161, 78, 176, 250],
                 [127, 79, 227, 168, 180, 174, 54, 192, 66, 19, 253, 3, 129, 160, 107, 46],
                 [82, 171, 226, 65, 173, 21, 237, 147, 207, 203, 109, 165, 28, 105, 121, 134],
                 [29, 186, 74, 172, 252, 204, 218, 131, 26, 8, 201, 85, 181, 158, 2, 122],
                 [210, 126, 251, 146, 163, 69, 216, 182, 43, 224, 244, 139, 22, 37, 59, 88],
                 [141, 1, 185, 89, 145, 150, 143, 133, 90, 68, 39, 247, 230, 33, 149, 213],
                 [114, 178, 169, 255, 55, 36, 155, 132, 57, 50, 124, 153, 140, 5, 162, 135],
                 [197, 233, 67, 189, 223, 193, 188, 238, 12, 35, 228, 20, 110, 44, 34, 15],
                 [254, 47, 42, 236, 97, 118, 116, 243, 48, 235, 191, 142, 151, 91, 128, 209],
                 [241, 41, 102, 7, 4, 87, 18, 212, 222, 198, 14, 53, 38, 248, 84, 0],
                 [76, 245, 95, 40, 148, 157, 184, 164, 166, 229, 99, 10, 31, 225, 194, 214]]

        if isdekrip == True:
            for i in range(16):
                self.shiftBoxRight(self.sbox1)
                self.shiftBoxDown(self.sbox1)


    def shiftBoxRight(self, sb):
        temp = sb[len(sb) - 1][len(sb[0]) - 1]
        for i in range(len(sb)*len(sb[0])-2,0,-1):
            sb[(i+1)/16][(i+1)%16] = sb[i/16][i%16]
        sb[0][0] = temp

    def shiftBoxLeft(self, sb):
        temp = sb[0][0]
        for i in range(0,len(sb)*len(sb[0])-1,1):
            sb[i/16][i%16] = sb[(i+1)/16][(i+1)%16]
        sb[len(sb) - 1][len(sb[0]) - 1] = temp

    def shiftBoxDown(self, sb):
        temp = sb[len(sb) - 1][len(sb[0]) - 1]
        for i in range(len(sb) * len(sb[0]) - 2, 0, -1):
            sb[(i + 1) % 16][(i + 1) / 16] = sb[i % 16][i / 16]
        sb[0][0] = temp

    def shiftBoxUp(self, sb):
        temp = sb[0][0]
        for i in range(0, len(sb) * len(sb[0]) - 1, 1):
            sb[i % 16][i / 16] = sb[(i + 1) % 16][(i + 1) / 16]
        sb[len(sb) - 1][len(sb[0]) - 1] = temp

    def xOREncryptKey(self):
        key = self.sboxkey[0]
        right1 = xor(self.right, key)
        self.right = right1

    def xOREncryptLeft(self, tmp):
        right1 = xor(self.right,tmp)
        return right1

    def substitutionEncrypt(self):
        right1 = []
        for i in range(len(self.right)):
            x = int(ord(self.right[i])/16)
            y = int(ord(self.right[i]))%16
            right1.append(chr(self.sbox1[x][y]))

    def rowTransposition(self):
        right1 = []
        for i in range(0,len(self.right),16):
            if len(self.right)-i >= 16:
                for j in range(len(self.rowtrp)):
                    right1.append(self.right[i+4*self.rowtrp[j]:i+4*(self.rowtrp[j]+1)])

    def columnTransposition(self):
        right1=[]
        for i in range(0,len(self.right),16):
            if len(self.right)-1 >= 16:
                for k in range (4):
                    for j in range(len(self.coltrp)):
                        right1.append(self.right[k%4+self.coltrp[j]])

    def assighnString(self, s, isdekrip):
        if isdekrip == False or isdekrip== True and len(s)%2 == 0:
            self.left = s[0:len(s)/2]
            self.right = s[len(s)/2:]
        else:
            self.left = s[0:len(s)/2]
            self.right = s[len(s)/2:]

def xor(a,b):
    xored = []
    for i in range(max(len(a), len(b))):
        xored_value = ord(a[i%len(a)]) ^ ord(b[i%len(b)])
        xored.append(hex(xored_value)[2:])
    return ''.join(xored)

