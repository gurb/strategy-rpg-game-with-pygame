import random
import numpy as np
from pygame.math import Vector2

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def generate_seed():
    seed_ = []
    for i in range(256):
        seed_.append(i)
    random.shuffle(seed_)
    for i in range(256):
        seed_.append(seed_[i])
    random.shuffle(seed_)
    return seed_

def calculate_constant_vec(seed_value):
    mod = seed_value % 4
    if mod == 0: return Vec2(1.0, 1.0)
    elif mod == 1: return Vec2(-1.0, 1.0)
    elif mod == 2: return Vec2(-1.0, -1.0)
    else: return Vec2(1.0, -1.0)

def fade(t):
    return ((6*t - 15)*t + 10)*t*t*t

def linear_interpolate(t, a1, a2):
    return a1 + t*(a2-a1)

def dot_product(vec1, vec2):
    return vec1.x * vec2.x + vec1.y * vec2.y

# seed = generate_seed()
seed = [161, 196, 17, 137, 214, 127, 22, 144, 25, 139, 235, 26, 164, 65, 224, 60, 148, 170, 221, 133, 
85, 142, 25, 5, 62, 48, 224, 101, 111, 253, 71, 134, 113, 20, 113, 166, 229, 161, 93, 88, 68, 234, 132, 
157, 4, 141, 108, 217, 136, 91, 67, 252, 197, 191, 6, 67, 14, 136, 100, 28, 176, 152, 251, 58, 77, 8, 52, 
250, 193, 121, 39, 121, 81, 226, 48, 242, 116, 74, 97, 185, 146, 151, 244, 3, 158, 156, 242, 31, 149, 13, 
230, 105, 73, 122, 250, 238, 235, 164, 1, 231, 238, 75, 150, 34, 112, 1, 187, 214, 247, 211, 122, 28, 192, 
2, 61, 160, 251, 98, 177, 167, 174, 63, 248, 62, 79, 54, 51, 45, 76, 146, 38, 216, 10, 27, 110, 5, 127, 120, 
130, 119, 168, 252, 40, 95, 145, 80, 83, 19, 32, 210, 131, 31, 173, 135, 85, 159, 216, 70, 131, 95, 198, 183, 
94, 176, 199, 221, 137, 8, 186, 21, 57, 220, 69, 143, 227, 135, 96, 148, 143, 42, 201, 19, 182, 141, 153, 
165, 169, 134, 183, 166, 12, 106, 43, 92, 243, 226, 233, 46, 42, 11, 26, 119, 199, 222, 64, 159, 177, 133, 246, 
180, 82, 30, 212, 130, 37, 152, 174, 139, 209, 12, 153, 190, 38, 11, 212, 3, 241, 172, 150, 204, 184, 0, 111, 
47, 81, 44, 94, 93, 7, 195, 247, 66, 154, 158, 84, 190, 232, 35, 246, 126, 18, 109, 215, 9, 87, 225, 228, 194, 73, 
4, 237, 98, 162, 165, 23, 239, 233, 194, 0, 172, 236, 188, 69, 33, 245, 45, 61, 218, 56, 39, 22, 36, 249, 197, 213, 
49, 124, 188, 71, 178, 213, 115, 230, 103, 56, 239, 86, 129, 21, 6, 76, 51, 236, 220, 205, 50, 36, 16, 33, 185, 124, 
75, 192, 55, 100, 189, 208, 225, 160, 193, 140, 204, 206, 99, 129, 231, 173, 105, 112, 37, 80, 198, 163, 53, 255, 
59, 154, 167, 102, 244, 208, 132, 52, 64, 189, 138, 223, 41, 120, 44, 182, 107, 211, 46, 142, 179, 207, 202, 196, 
91, 27, 155, 186, 117, 29, 99, 171, 201, 178, 41, 144, 179, 35, 184, 187, 175, 203, 254, 49, 82, 107, 249, 29, 43, 
203, 58, 200, 90, 240, 234, 30, 126, 24, 89, 88, 151, 2, 118, 102, 128, 54, 13, 72, 118, 10, 248, 243, 32, 228, 209, 
128, 96, 215, 218, 40, 109, 106, 205, 210, 163, 157, 90, 53, 77, 254, 147, 206, 117, 219, 14, 200, 195, 79, 84, 156, 
72, 175, 47, 229, 89, 253, 149, 57, 155, 70, 97, 103, 15, 191, 125, 7, 227, 207, 108, 181, 104, 66, 168, 202, 63, 50, 
60, 59, 17, 74, 123, 147, 83, 20, 78, 114, 255, 140, 180, 65, 116, 24, 217, 101, 223, 87, 16, 169, 181, 78, 86, 240, 
219, 9, 23, 237, 138, 15, 232, 68, 34, 55, 222, 162, 114, 171, 104, 115, 241, 245, 110, 123, 170, 145, 92, 125, 18]
# print(seed)

# this function return value as between 0.0 and 1.0
def Noise(x, y):
    x_ = int((x // 1) % 256)
    y_ = int((y // 1) % 256)
    
    xf = x - (x // 1)
    yf = y - (y // 1)

    top_right = Vec2(xf - 1.0, yf - 1.0)
    top_left  = Vec2(xf, yf - 1.0)
    bottom_right = Vec2(xf-1.0, yf)
    bottom_left = Vec2(xf, yf)

    # select a value in the array for each of the 4 corners
    value_top_right = seed[seed[x_ + 1] + y_ + 1]
    value_top_left  = seed[seed[x_] + y_ + 1]
    value_bottom_right = seed[seed[x_ + 1] + y_]
    value_bottom_left = seed[seed[x_] + y_]

    dot_top_right = dot_product(top_right, calculate_constant_vec(value_top_right))
    dot_top_left = dot_product(top_left, calculate_constant_vec(value_top_left))
    dot_bottom_left = dot_product(bottom_left, calculate_constant_vec(value_bottom_left))
    dot_bottom_right = dot_product(bottom_right, calculate_constant_vec(value_bottom_right))

    u, v = fade(xf), fade(yf)

    a_1 = linear_interpolate(v, dot_bottom_left, dot_top_left)
    a_2 = linear_interpolate(v, dot_bottom_right, dot_top_right)


    n = linear_interpolate(u, a_1, a_2)
    # n = (n+1)/2
    return n

if __name__ == "__main__":
    print(Noise(3 * 0.02, 4 * 0.02))
    print(len(seed))