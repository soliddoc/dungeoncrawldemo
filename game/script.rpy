init python:
    # this is how i store the level, the string type is not optimal here, but it's easy for me to iterate over the string positions. It's not like we care about a little higher memory usage, 640K of memory is all that anybody with a computer would ever need, right?
    # the level is stored as a table, so right now it's 3 by 3 room
    # to access any given tile we use "level1[0][1]" where the numbers in brackets correspond to the position in the array
    # first one is a row, second one is a collumn, so [0][1] would mean first row (0 is a first number) and second member of that row (0+1, remember?)
    # the four numbers in the string represent walls, the order i used is "top, right, bottom, left". "1" means a wall, "0" means no wall
    level1 = [["1001","1100","0011"],
            ["0011","0000","1110"],
            ["1011","0010","1110"]]
    # these are the variables i made for the minimap size adjustments
    minimapslotsize = 50 # a square tile size i used is 50x50 pixels
    framebordersize = 12 # and i use a frame, so i require a small offset to account for that

    class Player: # we need to know player position and rotation, so this is a class we are going to use
        def __init__(self, slot, rotation):
            self.slot = slot
            self.rotation = rotation

    class Slot: # and these are the things we will use for tile information storing: it's position in the level array and possible neighbours that we are going to set up later
        def __init__(self, xposit, yposit, north, west, east, south):
            self.xposit = xposit
            self.yposit = yposit
            self.north = north
            self.west = west
            self.east = east
            self.south = south

    rotatelist = ["north", "east", "south", "west"] # i made a rotate list so i can iterate over rotations in the order of my choosing, more on this later

label start: # this is how it starts
    call setuplevel(level1) # we call in setuplevel label below and provide it with our level
    call setplayer(1,0,"north") # i use this label to spawn the player, see label below
    while True: # now we start an endless loop
        # this will allows us to go through these calls every time we call a label from the gameplay screen, automating our work
        # if you plan on finishing the gameplay loop, you might aswell add the win/lose condition to get out of this loop
        call checkmovement # we check for available movement here, more on this down below in the respective label
        call setupscreen # then we prepare visuals
        call screen minimapscreen # and we call our screen, awaiting user to click some button
    return # this will end the game, but i won't cause we will never get here because of the endless loop

label setuplevel(level):
    python:
        levelmap = [] # we will create a local levelmap from the provided array above, so we make an empty list

        for x in range(len(level)): # i use x and y identifiers for rows and collumns respectively, so we go through the rows here
            levelrow = [] # make an empty row list
            for y in range(len(level[x])): # now go through the members of that row
                slot = Slot(x, y, level[x][y][0], level[x][y][3], level[x][y][1], level[x][y][2]) # make a slot object based on the class i made previously
                # we provide it with x and y positions, then we access the string positions for the north, west, east and south parts
                # don't ask me about the order, i rushed this thing and didn't get much sleep
                levelrow.append(slot) # then we add this newly made slot into the row list
            levelmap.append(levelrow) # and once we go through all the row members, we add that row to our local map
            # now the cycle goes through the remaining rows, compiling the local map array from our provided level

        for x in range(len(levelmap)): # after we are done with setting up the local map, we go through every row of it
            for y in range(len(levelmap[x])): # and then through every member of every row
                if levelmap[x][y].north == "0": # we look at the string value to see if there is a wall there, if there is "0" that means no wall is there
                    if x-1 >= 0: # we check whether the position isn't outside the bounds of our map
                        levelmap[x][y].north = levelmap[x-1][y] # and if everything is alright, we replace the string with the reference to the neigbouring tile in that direction
                if levelmap[x][y].west == "0": # now we do the same for the west neigbour
                    if y-1 >= 0:
                        levelmap[x][y].west = levelmap[x][y-1]
                if levelmap[x][y].east == "0": # and the east one
                    if y+1 < len(levelmap[x]):
                        levelmap[x][y].east = levelmap[x][y+1]
                if levelmap[x][y].south == "0": # and, you guessed it, south
                    if x+1 < len(levelmap):
                        levelmap[x][y].south = levelmap[x+1][y]
    # our local map is finally setup with all the information we need, so we return back to start label
    return

label setplayer(slotx,sloty,rotation): # we are given the x and y position and rotation
    $ PlayerObj = Player(levelmap[slotx][sloty],rotation) # so we create a player object based on the class above, and put our position info into respective fields
    return # and we go back

label checkmovement: # okay, the movement check part, we need to know if we can move in a certain direction so the buttons are enabled
    $ canmoveforward = Null # we disable them by default every time
    $ canmoveleft = Null
    $ canmoveright = Null
    $ canmovebackward = Null
    # and then we start checking the possible directions, broken down by rotation
    # this is very not optimal, but this is what i started with and it works, so i didn't bother changing it later
    # i made a rotate list later on to avoid so much useless copying, so you can try replacing this with it, or something better if you like
    # or don't, you do you
    if PlayerObj.rotation == "north": # we take a look at the player rotation
        if PlayerObj.slot.north != "1": # then access the slot that the player is on, check the north neighbour, if it's not wall but a connected tile (we connected them in map setup before)
            $ canmoveforward = PlayerObj.slot.north # we add the north slot to the canmoveforward variable to be used by the forward button
        if PlayerObj.slot.east != "1": # then we do the same for the rest of the directions
            $ canmoveright = PlayerObj.slot.east
        if PlayerObj.slot.south != "1":
            $ canmovebackward = PlayerObj.slot.south
        if PlayerObj.slot.west != "1":
            $ canmoveleft = PlayerObj.slot.west

    if PlayerObj.rotation == "east": # and the not optimized part of checking every possible player rotation and assigning values according to the rotation
        if PlayerObj.slot.north != "1":
            $ canmoveleft = PlayerObj.slot.north
        if PlayerObj.slot.east != "1":
            $ canmoveforward = PlayerObj.slot.east
        if PlayerObj.slot.south != "1":
            $ canmoveright = PlayerObj.slot.south
        if PlayerObj.slot.west != "1":
            $ canmovebackward = PlayerObj.slot.west

    if PlayerObj.rotation == "south":
        if PlayerObj.slot.north != "1":
            $ canmovebackward = PlayerObj.slot.north
        if PlayerObj.slot.east != "1":
            $ canmoveleft = PlayerObj.slot.east
        if PlayerObj.slot.south != "1":
            $ canmoveforward = PlayerObj.slot.south
        if PlayerObj.slot.west != "1":
            $ canmoveright = PlayerObj.slot.west

    if PlayerObj.rotation == "west":
        if PlayerObj.slot.north != "1":
            $ canmoveright = PlayerObj.slot.north
        if PlayerObj.slot.east != "1":
            $ canmovebackward = PlayerObj.slot.east
        if PlayerObj.slot.south != "1":
            $ canmoveleft = PlayerObj.slot.south
        if PlayerObj.slot.west != "1":
            $ canmoveforward = PlayerObj.slot.west
    return

label setupscreen:
    # now thinga are about to get a bit technical
    # first we are resetting every visual part on every move or rotation
    $ first_row_wall_left = False
    $ first_row_wall = False
    $ first_row_wall_right = False
    $ first_row_floor_left = False
    $ first_row_floor_right = False
    $ second_row_floor = False
    $ second_row_wall_left = False
    $ second_row_wall = False
    $ second_row_wall_right = False
    $ second_row_diagonal_wall_right = False
    $ second_row_diagonal_wall_left = False
    $ second_row_floor_right = False
    $ second_row_floor_left = False
    $ third_row_wall_left = False
    $ third_row_wall_right = False
    $ third_row_floor = False
    $ third_wall = False
    $ third_row_wall_diagonal_right = False
    $ third_row_wall_diagonal_left = False
    $ third_row_floor_left = False
    $ third_row_floor_right = False
    $ fourth_row_wall_left = False
    $ fourth_row_wall_right = False

    python: # this thing is made to tell the side tiles based on the player rotation
        for x in range(len(rotatelist)): # we go through the rotatelist declared earlier
            if rotatelist[x] == PlayerObj.rotation: # and try to match it to players rotation
                if x-1 >= 0: # once we get it, we check whether our index-1 (rotation to the left) is outside the list
                    rotationanticlockwise = rotatelist[x-1] # if it's within the list, the we take the rotation to the left
                else: # otherwise we start at the end of the list if we were at the start
                    rotationanticlockwise = rotatelist[3]
                if x+1 < len(rotatelist): # same for the other way around
                    rotationclockwise = rotatelist[x+1]
                else: # if we reached the end of the list, we start at the beginning
                    rotationclockwise = rotatelist[0]

    # now to the main visualization part
    # we go through 3 by 3 field with character being in the bottom middle position, and the field extends in the direction of our rotation
    # this is easily the weakest part of the script due to all hardcoding. Was unable to sleep at night so came up with this simple solution, it's by no means the best, but it does it's job
    # if you're curious how it works step by step, you can comment out this whole block, then reintroduce the parts one by one, this won't break the visualization part since it's separate, it will just not show everything

    if canmoveforward == Null: # checking whether we can move forward
        $ first_row_wall = True # if not, then draw wall
    else: # if there is no wall
        $ second_row_floor = True # then we draw the floor in front
        if getattr(canmoveforward,PlayerObj.rotation) == "1": # we check the tile in front of us, seeing if there is a wall after it
            $ second_row_wall = True # then show the wall
        if getattr(canmoveforward,rotationclockwise) == "1": # we check the tile in front of us, based on clockwise rotation relative to the player
            $ second_row_diagonal_wall_right = True # and if there is a wall, we draw it
        else: # if there is no wall to the right of the tile in front of us
            $ second_row_floor_right = True # then we draw the floor
        if getattr(canmoveforward,rotationanticlockwise) == "1": # same for the anticlockwise
            $ second_row_diagonal_wall_left = True # wall to the left of it
        else: # no wall
            $ second_row_floor_left = True

        $ second_row_right = getattr(canmoveforward,rotationclockwise) # get to the second row right tile via middle tile, in case the sides are blocked by walls
        if second_row_right != "1": # if there is no wall
            if getattr(second_row_right,PlayerObj.rotation) == "1": # if the forward from second row right tile is a wall
                $ third_row_wall_right = True # then draw a wall
            else:
                $ third_row_floor_right = True # or a floor if not
                $ third_row_right = getattr(second_row_right,PlayerObj.rotation) # we setup the third row right tile via second row right forward position
                if getattr(third_row_right, PlayerObj.rotation) == "1": # check for wall
                    $ fourth_row_wall_right = True # and draw it
        $ second_row_left = getattr(canmoveforward,rotationanticlockwise) # same for the left tile
        if second_row_left != "1": # if there is no wall
            if getattr(second_row_left,PlayerObj.rotation) == "1": # if the forward from second row left tile is a wall
                $ third_row_wall_left = True # then draw a wall
            else:
                $ third_row_floor_left = True # or a floor if not
                $ third_row_left = getattr(second_row_left,PlayerObj.rotation) # we setup the third row left tile via second row left forward position
                if getattr(third_row_left, PlayerObj.rotation) == "1": # check for wall
                    $ fourth_row_wall_left = True # and draw it

        $ third_row_mid = getattr(canmoveforward,PlayerObj.rotation) # try to move forward for the third time
        if third_row_mid != "1": # if there is no wall
            $ third_row_floor = True # then there is a floor
            if getattr(third_row_mid,PlayerObj.rotation) == "1": # check the final visualized tile forward facing wall
                $ third_wall = True # and draw if true
                if getattr(third_row_mid,rotationanticlockwise) == "1": # check third row mid tile anticlockwise wall
                    $ third_row_wall_diagonal_left = True # if wall then wall
                else:
                    $ third_row_floor_left = True # if not, then floor
                    $ third_row_left = getattr(third_row_mid,rotationanticlockwise) # we register third row left tile
                    if getattr(third_row_left, PlayerObj.rotation) == "1": # if front of the third row left tile is a wall
                        $ fourth_row_wall_left = True # then draw a wall
                if getattr(third_row_mid,rotationclockwise) == "1": # check third row mid tile clockwise wall
                    $ third_row_wall_diagonal_right = True # if wall then wall
                else:
                    $ third_row_floor_right = True # if not, then floor
                    $ third_row_right = getattr(third_row_mid,rotationclockwise) # we register third row right tile
                    if getattr(third_row_right, PlayerObj.rotation) == "1": # if front of the third row right tile is a wall
                        $ fourth_row_wall_right = True # then draw a wall


    if canmoveleft == Null: # checking whether we can move to the left
        $ first_row_wall_left = True # if not, then draw wall
    else: # if there is no wall
        $ first_row_floor_left = True #then we draw the floor to the left
        if getattr(canmoveleft,PlayerObj.rotation) == "1": # we check the left tile based on the player rotation
            $ second_row_wall_left = True # if there is a wall, we draw it
        else:
            $ second_row_floor_left = True # otherwise we draw the next floor
        $ second_row_left = getattr(canmoveleft,PlayerObj.rotation) # we get the second row left tile by going left tile and then forward based on player rotation
        if second_row_left != "1": # if the direction towards second row not blocked by a wall
            if getattr(second_row_left,PlayerObj.rotation) == "1": # we check whether there is a wall in the direction of player rotation
                $ third_row_wall_left = True # and draw it
            else:
                $ third_row_floor_left = True # otherwise we draw the floor


    if canmoveright == Null: # checking whether we can move to the right
        $ first_row_wall_right = True # if not, then draw wall
    else: # if there is no wall
        $ first_row_floor_right = True #then we draw the floor to the right
        if getattr(canmoveright,PlayerObj.rotation) == "1": # we check the right tile based on the player rotation
            $ second_row_wall_right = True # if there is a wall, we draw it
        else:
            $ second_row_floor_right = True # otherwise we draw the next floor
        $ second_row_right = getattr(canmoveright,PlayerObj.rotation) # we get the second row right tile by going right tile and then forward based on player rotation
        if second_row_right != "1": # if the direction towards second row not blocked by a wall
            if getattr(second_row_right,PlayerObj.rotation) == "1": # we check whether there is a wall in the direction of player rotation
                $ third_row_wall_right = True # and draw it
            else:
                $ third_row_floor_right = True # otherwise we draw the floor
    return

label moveplayer(slot): # this is a command to move the player to a provided slot from the screen move buttons
    $ PlayerObj.slot = levelmap[slot.xposit][slot.yposit] # we just take our map, find the needed slot by the positions given and change the player slot
    return

label rotateplayer(rotation): # this is a label we use to rotate the player clockwise and anticlockwise
    # slightly not optimal but it does it's job. You can try to replace it with rotate python block in setupscreen label, but it doesn't matter honestly
    if rotation == -1: # this is for anticlockwise
        if PlayerObj.rotation == "north":
            $ PlayerObj.rotation = "west"
        elif PlayerObj.rotation == "east":
            $ PlayerObj.rotation = "north"
        elif PlayerObj.rotation == "south":
            $ PlayerObj.rotation = "east"
        elif PlayerObj.rotation == "west":
            $ PlayerObj.rotation = "south"
    elif rotation == 1: # this is for clockwise
        if PlayerObj.rotation == "north":
            $ PlayerObj.rotation = "east"
        elif PlayerObj.rotation == "east":
            $ PlayerObj.rotation = "south"
        elif PlayerObj.rotation == "south":
            $ PlayerObj.rotation = "west"
        elif PlayerObj.rotation == "west":
            $ PlayerObj.rotation = "north"
    return

screen minimapscreen: # now the fun part, our gameplay screen, don't mind the name, it started as a simple minimap
    # i use this to display the level visuals, it doesn't look well, it's probably not coded all that well, but i suck at visuals generally, so this is what i use. Sue me
    # the order of display: last ones are drawn over the first ones, so the row one goes last, this is so the walls in front cover the terrain behind them
    # the visualization is separate from calculations, in case someone wants to add a tileset support or something like this, maybe change the names cause mine are confusing even for myself sometimes
    if fourth_row_wall_right != False:
        add "wall4_right"
    if fourth_row_wall_left != False:
        add "wall4_left"
    if third_row_floor_left != False:
        add "floor3_left"
    if third_row_floor_right != False:
        add "floor3_right"
    if third_row_wall_diagonal_right != False:
        add "wall3_diagonal_right"
    if third_row_wall_diagonal_left != False:
        add "wall3_diagonal_left"
    if third_wall != False:
        add "wall3"
    if third_row_floor != False:
        add "floor3"
    if third_row_wall_left != False:
        add "wall3_left"
    if third_row_wall_right != False:
        add "wall3_right"
    if second_row_floor_right != False:
        add "floor2_right"
    if second_row_floor_left != False:
        add "floor2_left"
    if second_row_floor != False:
        add "floor2"
    if second_row_wall_left != False:
        add "wall2_left"
    if second_row_wall != False:
        add "wall2"
    if second_row_wall_right != False:
        add "wall2_right"
    if second_row_diagonal_wall_right != False:
        add "wall2_diagonal_right"
    if second_row_diagonal_wall_left != False:
        add "wall2_diagonal_left"
    if first_row_wall_left != False:
        add "wall1_left"
    if first_row_wall != False:
        add "wall1"
    if first_row_wall_right != False:
        add "wall1_right"
    if first_row_floor_left != False:
        add "floor1_left"
    if first_row_floor_right != False:
        add "floor1_right"
    add "floor1"

    frame: # we draw a frame, so we can display our minimap on it, not being blocked by other elements on the screen. It goes after the visual display, so it will be drawn over it
        ysize len(levelmap) * minimapslotsize + framebordersize # we specify the size for the minimap based on the values i made at the start
        xsize len(levelmap[0]) * minimapslotsize + framebordersize # changing them and the image files will automatically adjust it to what we need
        for x in range(len(levelmap)): # we go through rows
            for y in range(len(levelmap[x])): # then through the members of those rows
                if levelmap[x][y].north == "1": # if the north of a tile is a wall
                    add "wall top" xpos y * minimapslotsize ypos x * minimapslotsize # we draw a wall
                    # one thing to notice here, i use y for xpos and x for ypos when it comes to visuals
                    # this is because in renpy xpos is horizontal position and ypos is vertical
                    # but in the array first identifier is rows, which is vertical and then collumn, which is horizontal
                    # you could use y x position for your array position identifiers but x y is what i am used to, so i swap them during the visualization
                    # this way i can do all my calculations in my preferred way
                if levelmap[x][y].east == "1": # same for other directions
                    add "wall right" xpos y * minimapslotsize ypos x * minimapslotsize
                if levelmap[x][y].south == "1":
                    add "wall bottom" xpos y * minimapslotsize ypos x * minimapslotsize
                if levelmap[x][y].west == "1":
                    add "wall left" xpos y * minimapslotsize ypos x * minimapslotsize
        # once we've gone though all the tiles and drawn all the walls, we must display a player
        if PlayerObj.rotation == "north": # i check the rotation to display different image
        # could have been made better with formating to display the needed image based on the rotation string + playerimage
        # but i was lazy
            add "playerup" xpos PlayerObj.slot.yposit * minimapslotsize ypos PlayerObj.slot.xposit * minimapslotsize
        elif PlayerObj.rotation == "east":
            add "playerright" xpos PlayerObj.slot.yposit * minimapslotsize ypos PlayerObj.slot.xposit * minimapslotsize
        elif PlayerObj.rotation == "south":
            add "playerdown" xpos PlayerObj.slot.yposit * minimapslotsize ypos PlayerObj.slot.xposit * minimapslotsize
        else:
            add "playerleft" xpos PlayerObj.slot.yposit * minimapslotsize ypos PlayerObj.slot.xposit * minimapslotsize

    vbox: # we make a movement controls button here
        # we make a vbox at the bottom right corner
        xalign 1.0
        yalign 1.0
        hbox: # then divide it into hboxes, first row is turning and forward
            frame:
                textbutton "Turn left":
                    action Call("rotateplayer", -1) # we call the rotate player label with anticlockwise direction, then we return back to our loop to recalculate everything
            frame:
                textbutton "Forward":
                    if canmoveforward != Null: # this check is to disable the button if you can't move forward
                        action Call("moveplayer", canmoveforward) # we call player movement into the tile that is registered in canmoveforward previously
            frame:
                textbutton "Turn right":
                    action Call("rotateplayer", 1) # another turn into another direction
        hbox: # second row is move left and right, same as move forward
            xalign 0.5
            frame:
                textbutton "Move left":
                    if canmoveleft != Null:
                        action Call("moveplayer", canmoveleft)
            frame:
                textbutton "Move right":
                   if canmoveright != Null:
                        action Call("moveplayer", canmoveright)
        frame: # and a final row containing move back button
            xalign 0.5
            textbutton "Move back":
                if canmovebackward != Null:
                    action Call("moveplayer", canmovebackward)
