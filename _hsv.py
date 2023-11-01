def from_rgb_to_hsv(r, g, b):
    hue = 0

    _max = max(r, g, b)
    _min = min(r, g, b)
    _diff = _max - _min

    if r == _max:
        hue = 0 + (0 if _diff == 0 else (1/6)*(g-b)/_diff)
    elif g == _max:
        hue = 1/3 + (0 if _diff == 0 else (1/6)*(b-r)/_diff)
    else:
        hue = 2/3 + (0 if _diff == 0 else (1/6)*(r-g)/_diff)
    
    if hue < 0:
        hue += 1

    saturation = 0 if _max == 0 else _diff/_max
    value = _max/255
    return (hue, saturation, value)

# Given hsv in [0,1]
# Produce rgb in [0, 255]
def from_hsv_to_rgb(h, s, v):
    r = 255
    g = 255
    b = 255

    _max = v * 255
    _min = (1-s)*_max
    _mn = (1-s)*v
    _diff = _max-_min
    _d = _diff/255


    # Red rotated toward green
    if h < 1/6:
        r = _max
        g = 6*h*_diff + _min
        b = _min
    # Green rotated toward red
    elif h < 2/6:
        r =  _min-(h-1/3)*_diff*6 
        g = _max
        b = _min
    # Green rotated toward blue
    elif h < 3/6:
        r = _min
        g = _max
        b = 6*h*_diff + _min
    # Blue rotated toward green
    elif h < 4/6:
        r = _min
        g =  _min-(h-2/3)*_diff*6 
        b = _max
    # Blue rotated toward red
    elif h < 5/6:
        r = 6*h*_diff + _min
        g = _min
        b = _max
    # Red rotated toward blue
    else:
        r = _max
        g = _min
        b = _min-(h-1)*_diff*6

    while r < 0: r += 255
    while g < 0: g += 255
    while b < 0: b += 255

    

    return (r, g, b)

# 255,0, 128 -> .916, 1, 1
# 128, 255, 0 -> .25, 1, 1
# 128, 255, 100 -> .303, .607, 1

print(from_rgb_to_hsv(255, 0, 128))
print(from_rgb_to_hsv(128, 255, 0))
print(from_rgb_to_hsv(128, 255, 100))
print()
print(from_hsv_to_rgb(.916, 1, 1))
print(from_hsv_to_rgb(.25, 1, 1))
print(from_hsv_to_rgb(.303, .607, 1))
print()
print(from_hsv_to_rgb(*from_rgb_to_hsv(255, 0, 128)))
print(from_hsv_to_rgb(*from_rgb_to_hsv(128, 255, 0)))
print(from_hsv_to_rgb(*from_rgb_to_hsv(128, 255, 100)))
