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


# --  Guard Connnection Rule -- 
# Grab the correct nodes to link
nameNode2 = str(getAttr('pname','2'))
nameNode3 = str(getAttr('pname','3'))
nameNode8 = str(getAttr('pname','8'))

# Also need to check that node0 has a PID of just smaller than node1 
node0PID = int(getAttr('pId','0'))
node1PID = int(getAttr('pId','1'))

print("<Check>")
print(f"NameNode2: {nameNode2}")
print(f"NameNode3: {nameNode3}")
print(f"NameNode8: {nameNode8}")
print(f"node0PID: {node0PID}")
print(f"node1PID: {node1PID}")
print("</Check>")

# Checks
result  = (node0PID+1 == node1PID) and nameNode2.endswith('outG') and nameNode3.startswith('in0') and nameNode8.startswith('inG')




# --  Guard Connnection Rule Confluence -- 
# Grab the correct nodes to link
nameNode2 = str(getAttr('pname','2'))
nameNode3 = str(getAttr('pname','3'))
nameNode8 = str(getAttr('pname','8'))
nameNode12 = str(getAttr('pname','12'))

# Also need to check that node0 has a PID of just smaller than node1 
node0PID = int(getAttr('pId','0'))
node1PID = int(getAttr('pId','1'))

# Checks
result  = (node0PID+1 == node1PID) and nameNode2.endswith('outG') and nameNode3.startswith('in0') and nameNode8.startswith('inG') and nameNode12.startswith('in1')


leftID = str(getAttr('pId','0'))
rightID = str(getAttr('pId','1'))

setAttr('pname', leftID + '_ptrans_' + rightID, '14')
setAttr('tname', leftID + '_g1trans_' + rightID, '15')
setAttr('tname', leftID + '_g2trans_' + rightID, '16')


# Grab the correct nodes to link
nameNode2 = str(getAttr('pname','2'))
nameNode3 = str(getAttr('pname','3'))
nameNode8 = str(getAttr('pname','8'))
nameNode12 = str(getAttr('pname','12'))

# Also need to check that node0 has a PID of just smaller than node1 
node0PID = int(getAttr('pId','0'))
node1PID = int(getAttr('pId','1'))

# Checks
result  = (node0PID+1 == node1PID) and nameNode2.endswith('outG') and nameNode3.startswith('in0') and nameNode8.startswith('inG') and nameNode12.startswith('in1')



# Check that there is no node with a smaller PID than the current
# That has not yet stepped
# print(f"Try to find blocing node {getAttr('pId', '0')} for node {getAttr('pId', '1')}")


# Check to make sure 0 is the smallest node and 1 is the biggest node
# False means it doesn't match
result = (getAttr('pId', '0') > getAttr('pId', '2')) and (getAttr('pId', '1') < getAttr('pId', '3'))



# Want False to not apply it
# 1 should be the smallest
# 0 should be the biggest
result = (getAttr('pId', '0') < getAttr('pId', '2')) and (getAttr('pId', '1') > getAttr('pId', '3'))





# Grab the correct nodes to link
nameNode2 = str(getAttr('pname','2'))
nameNode3 = str(getAttr('pname','3'))
nameNode8 = str(getAttr('pname','8'))

# Also need to check that node0 has a PID of just smaller than node1 
node0PID = int(getAttr('pId','0'))
node1PID = int(getAttr('pId','1'))

# Checks
result  = (node0PID+1 == node1PID) and nameNode2.endswith('outG') and nameNode3.startswith('in0') and nameNode8.startswith('inG')



leftID = str(getAttr('pId','0'))
rightID = str(getAttr('pId','1'))

setAttr('tname', leftID + '_gtrans_' + rightID, '10')



# O is biggest, 1 is smallest
result = (getAttr('pId', '0') > getAttr('pId', '2')) and (getAttr('pId', '1') < getAttr('pId', '3'))


print(f"{int(getAttr('pId', '2'))} : {int(getAttr('pId', '1'))}")
result = int(getAttr('pId', '2')) < int(getAttr('pId', '1'))


result = (int(getAttr('pId', '2')) < int(getAttr('pId', '1'))) and (int(getAttr('pId', '0')) < int(getAttr('pId', '3')))




# Grab the correct nodes to link
nameNode3 = str(getAttr('pname','3'))
nameNode8 = str(getAttr('pname','8'))

# Checks
result  =  nameNode3.startswith('in0') and nameNode8.startswith('inG')




rightID = str(getAttr('pId','1'))

setAttr('tname', 'first_t1_' + rightID, '4')
setAttr('tname', 'first_t2_' + rightID, '10')


print(f"{getAttr('pId', '15')} : {getAttr('pId', '1')}")

# If this is True the Rule is not applied
result = getAttr('$type', '1') == '/Formalisms/WMS/WMS/Confluence' or (int(getAttr('pId', '15')) < int(getAttr('pId', '1'))) or (int(getAttr('pId', '17')) > int(getAttr('pId', '16')))

result =  getAttr('$type', '1') == '/Formalisms/WMS/WMS/Confluence' or getAttr('$type', '0') == '/Formalisms/WMS/WMS/Source'


result = getAttr('$type', '0') == '/Formalisms/WMS/WMS/Source'


leftID = "-1"
rightID = str(getAttr('pId','1'))

setAttr('pname', leftID + '_ptrans_' + rightID, '14')
setAttr('tname', leftID + '_g1trans_' + rightID, '15')
setAttr('tname', leftID + '_g2trans_' + rightID, '16')

# Change the name of 15 and 4
setAttr('tname', 'first_t1_' + rightID, '4')
setAttr('tname', 'first_t2_' + rightID, '15')



# Translate Last order Rule
# Need to find the biggest Node
result = (int(getAttr('pId', '3')) > int(getAttr('pId', '1')))



# Grab the correct node and transition
nameNode = str(getAttr('pname','8'))
transitionName = str(getAttr('tname','4'))

# Checks
result  = nameNode.endswith('outG') and transitionName.startswith('first')
