# Need to add the checks and add the sets
# Need to add the resets to the reset nodes


# For the update Nodes Rule
if getAttr('$type', '1') == '/Formalisms/WMS/WMS/Sink':  # Check if the node is a Sink
    if getAttr('$type', '3') == '/Formalisms/WMS/WMS/Source':  # Check if the node is a Sink
        if int(getAttr('cooldown', '3')) == 1:  # Check if the source cooldown is 1
            setAttr('cooldown', int(getAttr('rate', '3')), '3') # Reset the cooldown
            setAttr('counter', int(getAttr('counter', '3')) + 1, '3') # Update the counter of 3
            setAttr('counter', int(getAttr('counter', '1')) + 1, '1') # Update the counter of 1

    elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Segment':  # Check if the node is a Segment
        if  getAttr('got_watercraft', '3') and not getAttr('got_this_turn', '3'):  # Check if there is a Watercraft that can be taken
            setAttr('got_watercraft', False, '3')  # Take the Watercraft
            setAttr('counter', int(getAttr('counter', '1')) + 1, '1')  # Update the counter of 1
 
    elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Confluence':  # Check if the node is a Confluence
        if getAttr('got_watercraft', '3') and not getAttr('last_direction', '3') and not getAttr('got_this_turn', '3'): # Check if the confluence has a ship and if it points our direction
            setAttr('got_watercraft', False, '3')  # Take the Watercraft
            setAttr('counter', int(getAttr('counter', '1')) + 1, '1')  # Update the counter of 1

elif getAttr('$type', '1') == '/Formalisms/WMS/WMS/Segment': # Check if the node is a Segment
    if not getAttr('got_watercraft', '1'): # Check if the node has capacity
        if getAttr('$type', '3') == '/Formalisms/WMS/WMS/Source':  # Check if the node is a Sink
            if int(getAttr('cooldown', '3')) == 1:  # Check if the source cooldown is 1
                setAttr('cooldown', int(getAttr('rate', '3')), '3') # Reset the cooldown
                setAttr('counter', int(getAttr('counter', '3')) + 1, '3') # Update the counter of 3
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship 

        elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Segment' and not getAttr('got_this_turn', '3'):  # Check if the node is a Segment
            if  getAttr('got_watercraft', '3'):  # Check if there is a Watercraft that can be taken
                setAttr('got_watercraft', False, '3')  # Take the Watercraft
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship 

        elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Confluence':  # Check if the node is a Confluence
            if getAttr('got_watercraft', '3') and not getAttr('last_direction', '3') and not getAttr('got_this_turn', '3'): # Check if the confluence has a ship and if it points our direction
                setAttr('got_watercraft', False, '3')  # Take the Watercraft
                setAttr('got_watercraft', True, '1') # Take the watercraft 
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship


# For the Update confluence Rule
# 1 is the confluence
# 2 is the in 0
# 3 is the in 1
if not getAttr('got_watercraft', '1'):  # Check if the node has capacity
    if getAttr('last_direction', '1'):  # Determine the last direction
        # Check if the other tile can give us a ship
        if getAttr('$type', '2') == '/Formalisms/WMS/WMS/Source':
            if int(getAttr('cooldown', '2')) == 1:  # Check if the source cooldown is 1
                setAttr('counter', int(getAttr('counter', '2')) + 1, '2') # Update the counter of 3
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('last_direction', False, '1') # Update the direction
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

        elif getAttr('$type', '2') == '/Formalisms/WMS/WMS/Segment':
            if  getAttr('got_watercraft', '2') and not getAttr('got_this_turn', '2'):  # Check if there is a Watercraft that can be taken
                setAttr('got_watercraft', False, '2')  # Take the Watercraft
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('last_direction', False, '1') # Update the direction
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship 

        elif getAttr('$type', '2') == '/Formalisms/WMS/WMS/Confluence':
            # Check if it points our direction and only then take the watercraft
            if getAttr('got_watercraft', '2') and not getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'):
                setAttr('got_watercraft', False, '2')  # Take the Watercraft
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('last_direction', False, '1') # Update the direction
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship 

        if not getAttr('got_watercraft', '1'): # Check if there still is no watercraft
            # Check if the other tile can give us a ship
            if getAttr('$type', '3') == '/Formalisms/WMS/WMS/Source':
                if int(getAttr('cooldown', '3')) == 1:  # Check if the source cooldown is 1
                    setAttr('counter', int(getAttr('counter', '3')) + 1, '3') # Update the counter of 3
                    setAttr('got_watercraft', True, '1') # Take the watercraft
                    setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

            elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Segment':
                if  getAttr('got_watercraft', '3') and not getAttr('got_this_turn', '3'):  # Check if there is a Watercraft that can be taken
                    setAttr('got_watercraft', False, '3')  # Take the Watercraft
                    setAttr('got_watercraft', True, '1') # Take the watercraft
                    setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

            elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Confluence':
                # Check if it points our direction and only then take the watercraft
                if getAttr('got_watercraft', '3') and getAttr('last_direction', '3') and not getAttr('got_this_turn', '3'):
                    setAttr('got_watercraft', False, '3')  # Take the Watercraft
                    setAttr('got_watercraft', True, '1') # Take the watercraft
                    setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

    else:
        # Check if the other tile can give us a ship
        if getAttr('$type', '3') == '/Formalisms/WMS/WMS/Source':
            if int(getAttr('cooldown', '3')) == 1:  # Check if the source cooldown is 1
                setAttr('counter', int(getAttr('counter', '3')) + 1, '3') # Update the counter of 3
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('last_direction', True, '1') # Update the direction
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

        elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Segment':
            if  getAttr('got_watercraft', '3') and not getAttr('got_this_turn', '3'):  # Check if there is a Watercraft that can be taken
                setAttr('got_watercraft', False, '3')  # Take the Watercraft
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('last_direction', True, '1') # Update the direction
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship 

        elif getAttr('$type', '3') == '/Formalisms/WMS/WMS/Confluence':
            # Check if it points our direction and only then take the watercraft
            if getAttr('got_watercraft', '3') and getAttr('last_direction', '3') and not getAttr('got_this_turn', '3'):
                setAttr('got_watercraft', False, '3')  # Take the Watercraft
                setAttr('got_watercraft', True, '1') # Take the watercraft
                setAttr('last_direction', True, '1') # Update the direction
                setAttr('got_this_turn', True, '1') # Indicate that we just got the ship 
        
        if not getAttr('got_watercraft', '1'): # Check if there still is no watercraft
            # Check if the other tile can give us a ship
            if getAttr('$type', '2') == '/Formalisms/WMS/WMS/Source':
                if int(getAttr('cooldown', '2')) == 1:  # Check if the source cooldown is 1
                    setAttr('counter', int(getAttr('counter', '2')) + 1, '2') # Update the counter of 3
                    setAttr('got_watercraft', True, '1') # Take the watercraft
                    setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

            elif getAttr('$type', '2') == '/Formalisms/WMS/WMS/Segment':
                if  getAttr('got_watercraft', '2') and not getAttr('got_this_turn', '2'):  # Check if there is a Watercraft that can be taken
                    setAttr('got_watercraft', False, '2')  # Take the Watercraft
                    setAttr('got_watercraft', True, '1') # Take the watercraft
                    setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

            elif getAttr('$type', '2') == '/Formalisms/WMS/WMS/Confluence':
                # Check if it points our direction and only then take the watercraft
                if getAttr('got_watercraft', '2') and not getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'):
                    setAttr('got_watercraft', False, '2')  # Take the Watercraft
                    setAttr('got_watercraft', True, '1') # Take the watercraft
                    setAttr('got_this_turn', True, '1') # Indicate that we just got the ship


# For the post confluence Rule
if not getAttr('got_watercraft', '1'):  # Check if the node has capacity
    if getAttr('got_watercraft', '2') and getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'): # Check if the confluence has a ship and if it points our direction
        setAttr('got_watercraft', False, '2')  # Take the Watercraft
        setAttr('got_watercraft', True, '1') # Take the watercraft
        setAttr('got_this_turn', True, '1') # Indicate that we just got the ship


# For the Source Rule

# Check if our cooldown is not 1
# If so decrease
if int(getAttr('cooldown', '1')) != 1:
    setAttr('cooldown', int(getAttr('cooldown', '1')) - 1, '1') # Decrease the cooldown

pass

# Goes into the Reset Nodes Rule
if getAttr('$type', '2') == '/Formalisms/WMS/WMS/Segment' or getAttr('$type', '2') == '/Formalisms/WMS/WMS/Confluence':
    setAttr('got_this_turn', False, '2')


# Check that there is no node with a smaller PID than the current
# That has not yet stepped
# print(f"Try to find blocing node {getAttr('pId', '0')} for node {getAttr('pId', '1')}")
result = getAttr('has_stepped', '1') or (getAttr('pId', '0') < getAttr('pId', '1') and not getAttr('has_stepped', '0'))


# Update post confluence

# Just need to check the type
print(f"Simulate the moving of the ship from confluence {getAttr('pId', '2')} to {getAttr('pId', '1')}")


if getAttr('$type', '1') == '/Formalisms/WMS/WMS/Sink':  # Check if the node is a Sink$
    if getAttr('got_watercraft', '2') and getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'): # Check if the confluence has a ship and if it points our direction
        setAttr('got_watercraft', False, '2')  # Take the Watercraft
        setAttr('counter', int(getAttr('counter', '1')) + 1, '1') # Update the counter of 1
elif getAttr('$type', '1') == '/Formalisms/WMS/WMS/Segment':  # Check if the node is a Segment
    if not getAttr('got_watercraft', '1'):  # Check if the node has capacity
        if getAttr('got_watercraft', '2') and getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'): # Check if the confluence has a ship and if it points our direction
            setAttr('got_watercraft', False, '2')  # Take the Watercraft
            setAttr('got_watercraft', True, '1') # Take the watercraft
            setAttr('got_this_turn', True, '1') # Indicate that we just got the ship


elif getAttr('$type', '1') == '/Formalisms/WMS/WMS/Confluence':  # Check if the node is a Segment
    if not getAttr('got_watercraft', '1'):  # Check if the node has capacity
        if getAttr('got_watercraft', '2') and getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'): # Check if the confluence has a ship and if it points our direction
    pass


if not getAttr('got_watercraft', '1'):  # Check if the node has capacity
    if getAttr('got_watercraft', '2') and getAttr('last_direction', '2') and not getAttr('got_this_turn', '2'): # Check if the confluence has a ship and if it points our direction
        setAttr('got_watercraft', False, '2')  # Take the Watercraft
        setAttr('got_watercraft', True, '1') # Take the watercraft
        setAttr('got_this_turn', True, '1') # Indicate that we just got the ship

pass