import numpy as np

if __name__ == '__main__':
    a = np.array([[1,2,3], [4,5,6], [-7,-8,-9]])
    print(a)
    b = [0.5,0.5, 0.3333]
    print(b)
    print(np.matmul(a,b))