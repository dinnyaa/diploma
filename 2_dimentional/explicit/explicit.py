import math 
import numpy as np 
from matplotlib import cm
import matplotlib.pyplot as plt
import sympy as sp

def solution(x, t) :
    return 2.0 * t + (np.power(x, 2) - 2) * np.sin(t) + np.cos(math.pi * t) * np.cos(math.pi * x)

def f(x, t) :
    return -np.power(x, 2) * np.sin(t)


def initial1(x) :
    return np.cos(x * math.pi)

def initial2(x) :
    return np.power(x, 2)

def boundry1(t) :
    return 0

def boundry2(t) :
    return 2 * np.sin(t)

def scheme_solution(T, l, M, N) :

    #մուտքային պայմանների ստուգում
    if M <= 0 or N <= 0 :
        raise ValueError("Invalid step arguments")
    
    # քայլերի հաշվարկը
    h_x = l / M 
    h_t = T / N
    r = np.power(h_t / h_x, 2)

    #կայունության պայմանի ստուգում
    if r > 1 :
        raise ValueError("Stability condition not satisfied")
    
    # ցանցի կառուցում
    x_arr = np.linspace(0.0, l, M + 1)
    t_arr = np.linspace(0.0, T, N + 1)

    # լուծումների մատրից
    v = np.zeros((N + 1, M + 1), dtype=float)

    #սկզբանական պայմանների կիրառում 
    v[0] = initial1(x_arr)
    v[1] = v[0] + h_t * (initial2(x_arr) + (h_t/2)  * (-np.power(np.pi, 2) * np.cos(np.pi * x_arr) + f(x_arr, 0)))

    # բացահայտ սխեմայի կիրառում
    for n in range(1, N) :  
        for m in range(1, M) : 
            v[n+1][m] = r * v[n][m-1] + 2.0 * (1.0 - r) * v[n][m] + r * v[n][m+1] - v[n-1][m] + np.power(h_t, 2) * f(x_arr[m], t_arr[n])
        # եզրային պայմանների կիրառում
        v[n+1][0] = v[n+1][1] + h_x * boundry1(t_arr[n+1])
        v[n+1][M] = v[n+1][M-1] + h_x *  boundry2(t_arr[n+1])
   
    return v


def getter(M, N) :
    X, T = np.meshgrid(np.linspace(0.0, 1.0, M + 1), np.linspace(0.0, 1.0, N + 1))
    v = scheme_solution(1.0, 1.0, M, N)
    return X, T, v

T = 1.0
M = 30
N = 60
l = 1.0
v = scheme_solution(T, l, M, N)
X, T = np.meshgrid(np.linspace(0.0, 1.0, M + 1), np.linspace(0.0, 1.0, N + 1))

Z = solution(X, T)


plt.figure(1)
ax1 = plt.axes(projection='3d')
ax1.plot_surface(X, T, Z, rstride=1, cstride=1,
                cmap=cm.coolwarm, edgecolor='none')

plt.figure("hm")
ax2 = plt.axes(projection='3d')
ax2.plot_surface(X, T, v , rstride=1, cstride=1,
                cmap=cm.coolwarm, edgecolor='none')

ax1.set_xlim(0.0, 1.0)
ax1.set_ylim(0.0, 1.0)
ax1.set_xlabel('X-axis')
ax1.set_ylabel('T-axis')
ax1.set_zlabel('U-axis')

ax2.set_xlim(0.0, 1.0)
ax2.set_ylim(0.0, 1.0)
ax2.set_xlabel('X-axis')
ax2.set_ylabel('T-axis')
ax2.set_zlabel('V-axis')

plt.show()


