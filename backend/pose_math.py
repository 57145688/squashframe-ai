import math
def angle(a,b,c):
    u=(a[0]-b[0],a[1]-b[1]);v=(c[0]-b[0],c[1]-b[1])
    n=math.hypot(*u)*math.hypot(*v)
    if n<1e-12:return None
    return round(math.degrees(math.acos(max(-1,min(1,(u[0]*v[0]+u[1]*v[1])/n)))),2)
