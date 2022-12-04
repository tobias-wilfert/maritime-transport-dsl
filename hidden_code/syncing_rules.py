# syncGotWatercraft
# LHS - in Place 
result = "shipPos" in getAttr() # check if shipPos is in Place

# RHS
val = (int(getAttr('tokens','1')) == 1)
setAttr('got_watercraft',val,'0')

# syncCtrs
# LHS - in Place

# RHS
val = int(getAttr('tokens','1'))
setAttr('counter', val, '0')