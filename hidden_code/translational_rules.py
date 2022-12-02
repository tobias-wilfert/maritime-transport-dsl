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

# Segment transformation
segmentID = str(getAttr('pId','0'))

setAttr('pname', 'in0_' + segmentID + '_out0', '1')


# Confluence transformation
cofluenceID = str(getAttr('pId','0'))

setAttr('pname', 'in0_' + cofluenceID, '5')
setAttr('pname', cofluenceID + 'confluence', '6')
setAttr('pname', cofluenceID + 'guard0', '7')
setAttr('pname', cofluenceID + 'guard1', '8')
setAttr('pname', 'in1_' + cofluenceID, '9')
setAttr('pname', cofluenceID + '_out0', '10')
setAttr('pname', cofluenceID + '_out1', '11')

setAttr('tname', cofluenceID + 't_in0', '1')
setAttr('tname', cofluenceID + 't_in1', '2')
setAttr('tname', cofluenceID + 't_out0', '3')
setAttr('tname', cofluenceID + 't_out1', '4')

# Sink transformation
segmentID = str(getAttr('pId','0'))

setAttr('pname', 'in0_' + segmentID,'1')


# Link0 transtlation !Sink
# Grab the correct nodes to link
nameNode3 = str(getAttr('pname','3'))
nameNode4 = str(getAttr('pname','4'))

# Checks
result  = nameNode4.startswith('in0') and nameNode3.endswith('out0')


# Naming the link
leftID = str(getAttr('pId','0'))
rightID = str(getAttr('pId','1'))

setAttr('tname', leftID + '_trans_' + rightID, '7')