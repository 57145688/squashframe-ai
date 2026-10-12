from pose_math import angle
def test_right():assert angle((1,0),(0,0),(0,1))==90
def test_straight():assert angle((-1,0),(0,0),(1,0))==180
def test_zero():assert angle((0,0),(0,0),(1,0)) is None
