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



# -- Source Rule: Action --
sourceRate = int(getAttr('rate', '0'))
sourceID = str(getAttr('pId','0'))

# Set the values related to the tile
setAttr('capacity',sourceRate, '2')
setAttr('weight',sourceRate, '7')

# Name the transitions and places related to the tile
setAttr('tname', sourceID+'spawn','1')
setAttr('pname', sourceID+'wait','2')
setAttr('tname', sourceID+'out','4')

# Name the guard related
setAttr('pname', 'inG' + sourceID, '11')
setAttr('pname', sourceID + 'g', '12')
setAttr('pname', sourceID + 'outG', '13')

setAttr('tname', sourceID + 'g1', '18')
setAttr('tname', sourceID + 'g2', '19')


# -- Segement Rule: Action --
segmentID = str(getAttr('pId','0'))

# Name the place related items
setAttr('pname', 'in0_' + segmentID + '_out0', '1')

# Name the guard related items
setAttr('pname', 'inG_' + segmentID + '_outG', '2')


# -- Sink Rule: Action --
segmentID = str(getAttr('pId','0'))

# Name the place related items
setAttr('pname', 'in0_' + segmentID,'1')

# Name the guard related items
setAttr('pname', 'inG_' + segmentID + '_outG', '3')


# -- Confluence Rule: Action --
cofluenceID = str(getAttr('pId','0'))

# Name the transitions and places realted to the tile
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

# Name the transitions and places realted to the guard
setAttr('pname', 'inG_' + cofluenceID , '28')
setAttr('pname', cofluenceID + 'g1', '29')
setAttr('pname', cofluenceID + 'g2', '30')
setAttr('pname', cofluenceID + 'g3', '31')
setAttr('pname', cofluenceID + '_outG', '32')

setAttr('tname', cofluenceID + 'g4', '33')
setAttr('tname', cofluenceID + 'g5', '34')
setAttr('tname', cofluenceID + 'g6', '35')
setAttr('tname', cofluenceID + 'g7', '36')