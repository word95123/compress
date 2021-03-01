import cv2
class press():
    def trees(self,a,c,d):
        #print()
        for i in range(2):
            for j in range(i+1,len(a)):
                if(a[i]>a[j]):
                    e = a[i]
                    a[i] = a[j]
                    a[j] = e

                    e = c[i]
                    c[i] = c[j]
                    c[j] = e


        if(type(c[0]) is tuple):
            for i in range(len(c[0])):
                d[c[0][i]] += '1'
        else:
            d[c[0]] = '1'
        if(type(c[1]) is tuple):
            for i in range(len(c[1])):
                d[c[1][i]] += '0'
        else:
            d[c[1]] = '0'

        #print(d)
        if(type(c[0]) is tuple and type(c[1]) is tuple):
            c.insert(2,(c[0]+c[1]))
            c.pop(0)
            c.pop(0)
        elif(type(c[0]) is tuple and type(c[1]) is not tuple):
            c.insert(2,(c[0]+(c[1],)))
            c.pop(0)
            c.pop(0)
        elif(type(c[0]) is not tuple and type(c[1]) is tuple):
            c.insert(2,((c[0],)+c[1]))
            c.pop(0)
            c.pop(0)
        else:
            c.insert(2,(c[0],c[1]))
            c.pop(0)
            c.pop(0)
        #print(c)
        a.insert(2,a[0]+a[1])
        a.pop(0)
        a.pop(0)
        #print(a)

        return a,c,d

    def hoff(self,a,c,d):
        while(True):
            if(len(a)==1):
                break
            a,c,d = self.trees(a,c,d)
        return d

if __name__ == "__main__":
    
    
    press = press()
    '''
    a = [1,2,2,2,3,3,4,5,6,1,2,5,7,9,8,4,2,5,5,5,1,2,3,4,6,4,5,8,7,9,1,1,2,3,1,1]
    b = {}

    for i in range(len(a)):
        if a[i] in b:
            b[a[i]] += 1
        else:
            b[a[i]] = 1

    a=[]
    c=[]

    for j in range(len(b)):
        for i in b.keys():
            if b[i] == min(b.values()):
                a.append(b[i])
                c.append(i)
                b.pop(i)
                break
    print(c)
    print(a)

    d = {}
    press.hoff(a,c,d)
    '''
    img = cv2.imread('C:/Users/ice/Desktop/test.JPG',cv2.IMREAD_GRAYSCALE)
    b = {}
    a = []
    counts = 0
    for i in range(len(img)):
        for j in range(len(img[i])):
            a.append(img[i][j])
            counts += 1
    for i in range(len(a)):
        if a[i] in b:
            b[a[i]] += 1
        else:
            b[a[i]] = 1
    a=[]
    c=[]
    total = b.copy()
    for j in range(len(b)):
        for i in b.keys():
            if b[i] == min(b.values()):
                a.append(b[i])
                c.append(i)
                b.pop(i)
                break
    d = {}
    d = press.hoff(a,c,d)
    
    #print(d)
    efficiency = 0
    for i in range(255):
        if i in total:
            efficiency += total[i] * len(d[i])

    print('efficiency:' + str((counts * 8)/efficiency))
    pass








