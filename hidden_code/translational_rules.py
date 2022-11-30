# Frustrations (so far)
# - connecting PN Place to Transition doesnt give choice and just puts genericGraph line --> no idea why
#   maybe just don't do the genericGraph thing until the transformation is written?
#
#-------------------------------------------------------------------------------------------------------
#
# Source transformation
# 
sourceRate = int(getAttr('rate', '0'))
sourceID = str(getAttr('pId','0'))

setAttr('capacity',sourceRate, '2')
setAttr('weight',sourceRate, '7')

setAttr('tname', sourceID+'spawn','1')
setAttr('pname', sourceID+'wait','2')
setAttr('pname', sourceID+'ctr','6')
setAttr('tname', sourceID+'out0','4')

#
# Segment transformation
# 
segmentID = str(getAttr('pId','0'))

setAttr('tname', sourceID+'in0','2')
setAttr('pname', sourceID+'tile','1')
setAttr('tname', sourceID+'out0','3')