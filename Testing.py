from Fierkes import Fierkes

Fr = Fierkes()
msg = "brbr lebiiiihhhh panjang ga kaen ya? coba dl"

for i in range(16):
    Fr.fn.assighnString(msg,False)
    msg = Fr.Encrypt()
print(msg)

for i in range(16):
    Fr.fnd.assighnString(msg,True)
    msg = Fr.Decrypt()
print(msg)
