from Fiestel import Fiestel

class Fierkes:
    fn = Fiestel(False)
    fnd = Fiestel(True)

    def Encrypt(self):
        tmpleft = self.fn.left
        self.fn.left = self.fn.right
        self.fn.xOREncryptKey()
        self.fn.shiftBoxRight(self.fn.sboxkey)
        self.fn.substitutionEncrypt()
        self.fn.shiftBoxDown(self.fn.sbox1)
        self.fn.rowTransposition()
        self.fn.columnTransposition()
        self.fn.right = self.fn.xOREncryptLeft(tmpleft)
        return self.fn.left + self.fn.right

    def Decrypt(self):
        tempRight = self.fnd.right
        tempLeft = self.fnd.left
        self.fnd.right = self.fnd.left
        self.fnd.shiftBoxLeft(self.fnd.sboxkey)
        self.fnd.xOREncryptKey()
        self.fnd.shiftBoxUp(self.fnd.sbox1)
        self.fnd.substitutionEncrypt()
        self.fnd.rowTransposition()
        self.fnd.columnTransposition()
        self.fnd.left = self.fnd.xOREncryptLeft(tempRight)
        self.fnd.right = tempLeft
        return self.fnd.left + self.fnd.right