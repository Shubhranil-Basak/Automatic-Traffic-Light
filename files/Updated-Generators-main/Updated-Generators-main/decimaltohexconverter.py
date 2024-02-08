def decToHexa(n, size):

    hexaDeciNum = ''

    i = 0
    while(n != 0):
  
        temp = n % 16
  
        # check if temp < 10
        if(temp < 10):
            hexaDeciNum+=chr(temp + 48)  
        else:
            hexaDeciNum+=chr(temp + 55)
            
        n = int(n / 16)
        hexaDeciNum = hexaDeciNum[-1:-9:-1]
        i+=1

    return '0'*(size//4-i)+hexaDeciNum

if __name__ == "__main__":
    print(decToHexa(1023, 32))