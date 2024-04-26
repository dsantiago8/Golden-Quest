init -1 python:
    img = ["images/lock_plate.png", "images/lock_cylinder.png",
        "images/lock_tension.png", "lock_pick.png"]
    """
    Important: You should have four images listed in this order--The Lock Plate,
    The Lock Cylinder, The Lock Tension Bar, The Lock Pick
    """
    renpy.music.register_channel("Lock_Move", mixer= "sfx", loop=True)
    renpy.music.register_channel("Lock_Click", mixer= "sfx", loop=False, tight=True)
    """These are here so that the various lock sounds play on their own sound channels."""

    """As a Creater Defined Displayable this needs to extend the Displayable class)"""
    class Lock(renpy.Displayable):

        #The lock class constructor
        def __init__(self, difficulty, loot, resize=1920, **kwargs):
            """
            This constructor takes the following arguments:
            difficulty=How accurate the player has to be, how quickly lock picks break
            difficulty is given as a number between 1 and 29 - the lower the number, the more difficult the lock
            loot=What the player gets for successfully picking the lock
            resize=Your screen width
            """
            super(Lock, self).__init__(**kwargs)

            #These lines are for setting up the images used and the size of them
            self.width = resize
            self.lock_plate_image = im.Scale(img[0], resize, resize)
            self.lock_cylinder_image = im.Scale(img[1], resize, resize)
            self.lock_tension_image = im.Scale(img[2], resize, resize)
            self.lock_pick_image = im.Scale(img[3], resize, resize)
            self.offset = (resize*2**0.5-resize)/2

            #Variables
            self.cylinder_min = 0
            self.cylinder_max = 90
            self.cylinder_pos = 0 #where the cylinder currently is
            self.cylinder_try_rotate = False #if the cylinder is attempting to rotate
            self.cylinder_can_rotate = False #if the cylinder is allowed to rotate
            self.cylinder_released = False #checking if the cylinder has JUST been released
            self.pick_min = 0
            self.pick_max = 180
            self.pick_pos = 90 #where the pick currently is
            self.pick_can_rotate = True
            self.pick_broke = False #if the pick just broke
            self.sweet_spot = renpy.random.randint(0,180) #a point between 0 and 180 determined randomly when the lock is created
            self.difficulty = difficulty #a number between 1 and 29 - the lower the number, the more difficult the lock
            self.breakage = (difficulty/7 + 0.75) #a number based on difficulty, the amount of time before the lock pick breaks

            self.loot = loot #something to give the player if they successfully pick the lock

        def event(self, ev, x, y, st):
            import pygame
            LEFT = 1
            RIGHT = 3

            remaining = 0 + st

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == LEFT:
                self.cylinder_try_rotate = True
                self.cylinder_released = False
            elif ev.type == pygame.MOUSEBUTTONUP and ev.button == LEFT:
                renpy.sound.stop(channel="Lock_Move")
                self.cylinder_try_rotate = False
                self.cylinder_released = True
                self.pick_can_rotate = True
                self.pick_broke = False
                #global timers
                #timers = 0
            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == RIGHT:
                #exit lockpicking
                global current_chest
                current_chest = None
                renpy.hide_screen("lockpicking")



        # Function that continuously updates the graphics of the lock
        def render(self, width, height, st, at):
            import pygame

            #normalize the difficulty between 1 and 29 (even 20 is pretty easy though)
            if self.difficulty > 29:
                self.difficulty = 29
            elif self.difficulty < 1:
                self.difficulty = 1

            if self.pick_can_rotate == True:
                x, y = renpy.get_mouse_pos()
                self.pick_pos = x/5.3333333333 -90

                #the lock pick can only move between 0 and 180 degrees
                if self.pick_pos > 180:
                    self.pick_pos = 180
                elif self.pick_pos < 0:
                    self.pick_pos = 0


                #if the position of the pick is close to the sweet spot, the cylinder can rotate
                if self.pick_pos > self.sweet_spot:
                    if (self.pick_pos - self.sweet_spot) < self.difficulty:
                        #if it's "close enough" as determined by the difficulty
                        self.cylinder_can_rotate = True
                        self.cylinder_max = 90
                    else:
                        self.cylinder_can_rotate = True
                        self.cylinder_max = 90 - (self.pick_pos - self.sweet_spot)*(30/self.difficulty)
                        #if it's not close enough, it can still rotate a bit, based on how far away it is
                        if self.cylinder_max < 0:
                            self.cylinder_max = 0

                elif self.pick_pos < self.sweet_spot:
                    if (self.sweet_spot - self.pick_pos) < self.difficulty:
                        #if it's "close enough" as determined by the difficulty
                        self.cylinder_can_rotate = True
                        self.cylinder_max = 90
                    else:
                        self.cylinder_can_rotate = True
                        self.cylinder_max = 90 - (self.sweet_spot - self.pick_pos)*(30/self.difficulty)
                        #if it's not close enough, it can still rotate a bit, based on how far away it is
                        if self.cylinder_max < 0:
                            self.cylinder_max = 0


                else: #self.pick_pos == self.sweet_spot
                    self.cylinder_can_rotate = True
                    self.cylinder_max = 90

            #move the pick
            if self.pick_broke == True:
                pick = Transform(child=None)
            else:
                pick = Transform(child=self.lock_pick_image, rotate=self.pick_pos, subpixel=True)

            #global variables to use with displays for debugging
            global display_pos
            display_pos = self.pick_pos

            global display_spot
            display_spot = self.sweet_spot


            #The following is all the render information for Lock and parts
            # Create transform to rotate the moving parts
            if self.cylinder_try_rotate == True:

                #if the pick is in the correct position, set self.cylinder_can_rotate to True
                #else: set self.cylinder_can_rotate = False

                #if the cylinder CAN rotate
                if self.cylinder_can_rotate:

                    self.cylinder_pos += (2*st)/(at+1)

                    cylinder = Transform(child=self.lock_cylinder_image, rotate=self.cylinder_pos, subpixel=True)
                    tension = Transform(child=self.lock_tension_image, rotate=self.cylinder_pos, subpixel=True)

                    #it can only rotate up to self.cylinder_max
                    if self.cylinder_pos > self.cylinder_max:
                        self.cylinder_pos = self.cylinder_max

                        # if it gets to 90, you win
                        if self.cylinder_pos == 90:
                            renpy.sound.stop(channel="Lock_Move")
                            renpy.sound.play("audio/lock_unlock.mp3", channel="Lock_Click")
                            renpy.notify("You unlocked the chest!")
                            self.cylinder_max = 90
                            self.cylinder_pos = 90
                            global set_timers
                            global timers
                            timers = 0
                            set_timers = False
                            pygame.time.wait(150)
                            self.cylinder_can_rotate = False
                            renpy.jump("opened_chest")
                        else:
                            #jiggle when it gets to self.cylinder_max
                            if renpy.sound.is_playing != True:
                                renpy.sound.play("audio/lock_moving.mp3", channel="Lock_Move")

                            angle1 = self.cylinder_pos + renpy.random.randint(-2,2)
                            angle2 = self.cylinder_pos + renpy.random.randint(-4,4)
                            cylinder = Transform(child=self.lock_cylinder_image, subpixel=True, rotate=angle1)
                            tension = Transform(child=self.lock_tension_image, subpixel=True, rotate=angle2)

                            self.pick_can_rotate = False

                            global lockpicks
                            #if a timer here exceeds self.breakage, break a lock pick (play a sound and hide the image momentarily), reset its position, decrement number of lockpicks
                            global set_timers
                            global timers
                            if set_timers == False:
                                timers = at
                                set_timers = True

                            if set_timers == True:
                                if at > timers+self.breakage:
                                    renpy.sound.stop(channel="Lock_Move")
                                    renpy.sound.play("audio/lock_pick_break.mp3", channel="Lock_Click")
                                    renpy.notify("Broke a lock pick!")
                                    mispick = renpy.random.randint(-30, 30)
                                    pick = Transform(child=self.lock_pick_image, rotate=self.pick_pos+(2*mispick), subpixel=True)
                                    self.pick_can_rotate = False
                                    pygame.time.wait(200)
                                    self.pick_broke = True
                                    self.cylinder_try_rotate = False
                                    lockpicks -= 1
                                    timers = 0
                                    set_timers = False
                                    pygame.mouse.set_pos([self.width/2, self.width/4])
                                    pygame.time.wait(100)

                else:
                    #jiggle if it can't rotate
                    if renpy.sound.is_playing != True:
                        renpy.sound.play("audio/lock_moving.mp3", loop=True, channel="Lock_Move")
                    angle1 = self.cylinder_pos + renpy.random.randint(-2,2)
                    angle2 = self.cylinder_pos + renpy.random.randint(-4,4)
                    cylinder = Transform(child=self.lock_cylinder_image, subpixel=True, rotate=angle1)
                    tension = Transform(child=self.lock_tension_image, subpixel=True, rotate=angle2)

                    self.pick_can_rotate = False

                    global lockpicks
                    #if a timer here exceeds self.breakage, break a lock pick (play a sound and hide the image momentarily), reset its position, decrement number of lockpicks
                    global set_timers
                    global timers
                    if set_timers == False:
                        timers = at
                        set_timers = True

                    if set_timers == True:
                        if at > timers+self.breakage:
                            renpy.sound.stop(channel="Lock_Move")
                            renpy.sound.play("audio/lock_pick_break.mp3", channel="Lock_Click")
                            renpy.notify("Broke a lock pick!")
                            mispick = renpy.random.randint(-30, 30)
                            pick = Transform(child=self.lock_pick_image, rotate=self.pick_pos+(2*mispick), subpixel=True)
                            self.pick_can_rotate = False
                            pygame.time.wait(200)
                            self.pick_broke = True
                            self.cylinder_try_rotate = False
                            lockpicks -= 1
                            timers = 0
                            set_timers = False
                            pygame.mouse.set_pos([self.width/2, self.width/4])
                            pygame.time.wait(100)


            else: #release, go back to the starting position
                if self.cylinder_released == True:
                    if self.cylinder_pos > 15:
                        renpy.sound.play("audio/lock_moving_back.mp3", channel="Lock_Click")
                    self.pick_can_rotate = True
                    self.cylinder_pos -= (5*st)/(at+1)

                    if self.cylinder_pos < self.cylinder_min:
                        self.cylinder_pos = self.cylinder_min
                        self.cylinder_released = False
                        renpy.sound.stop(channel="Lock_Click")
                        #global set_timers
                        #global timers
                        #set_timers = False
                        #timers = 0
                cylinder = Transform(child=self.lock_cylinder_image, rotate=self.cylinder_pos, subpixel=True)
                tension = Transform(child=self.lock_tension_image, rotate=self.cylinder_pos, subpixel=True)



            # Create a render for the children.
            lock_plate_render = renpy.render(self.lock_plate_image, width, height, st, at)
            lock_cylinder_render = renpy.render(cylinder, width, height, st, at)
            lock_tension_render = renpy.render(tension, width, height, st, at)
            lock_pick_render = renpy.render(pick, width, height, st, at)

            # Create the render we will return.
            render = renpy.Render(self.width, self.width)

            # Blit (draw) the child's render to our render.
            render.blit(lock_plate_render, (0, 0))
            render.blit(lock_cylinder_render, (-self.offset, -self.offset))
            render.blit(lock_tension_render, (-self.offset, -self.offset))
            render.blit(lock_pick_render, (-self.offset, -self.offset))

            #This makes sure our object redraws itself after it makes changes
            renpy.redraw(self, 0)

            # Return the render.
            return render


        #reser the lock after opening
        def reset(self):
            self.cylinder_min = 0
            self.cylinder_max = 90
            self.cylinder_pos = 0 #where the cylinder currently is
            self.cylinder_try_rotate = False #if the cylinder is attempting to rotate
            self.cylinder_can_rotate = False #if the cylinder is allowed to rotate
            self.pick_min = 0
            self.pick_max = 180
            self.pick_pos = 90 #where the pick currently is
            self.sweet_spot = renpy.random.randint(0,180) #a point between 0 and 180 determined randomly when the lock is created

    def str_to_class(str):
        return getattr(sys.modules[__name__], str)



init python:
    def counter(st, at):

        f = 0.0

        if hasattr(store, 'display_pos'):
            f = store.display_pos #display the position of the pick, for debug purposes

        return Text("%.1f" % f, color="#09c", size=30), .1
    def counter2(st, at):

        f = 0.0

        if hasattr(store, 'display_spot'):
            f = store.display_spot #display the position of the goal, for debug purposes

        return Text("%.1f" % f, color="#09c", size=30), .1

image counter = DynamicDisplayable(counter)
image counter2 = DynamicDisplayable(counter2)

default display_pos = 0
default display_spot = 0
default timers = 0
default set_timers = 0
default current_chest = None

image lock_dark = Solid("#000c")
image lock_plate = "lock_plate.png"
image lock_cylinder = "lock_cylinder.png"
image lock_tension = "lock_tension.png"
image lock_pick = "lock_pick.png"


#image definitions are not necessary, but these are the named images needed for each locked object
image lock_chest1_closed = "lock_chest1_closed.png"
image lock_chest1_hover = "lock_chest1_hover.png"
image lock_chest1_open = "lock_chest1_open.png"
image lock_chest1_open_hover = "lock_chest1_open_hover.png"
default lock_chest1_lock = Lock(20, 100)
default lock_chest1_have_key = False
default lock_chest1_opened = False


default lock_chest2_lock = Lock(15, 100)
default lock_chest2_have_key = False
default lock_chest2_opened = False

default lock_chest3_lock = Lock(10, 100)
default lock_chest3_have_key = False
default lock_chest3_opened = False

default lock_chest4_lock = Lock(7, 100)
default lock_chest4_have_key = False
default lock_chest4_opened = False

default lock_chest5_lock = Lock(4, 100)
default lock_chest5_have_key = False
default lock_chest5_opened = False

# '{}_closed'.format(chest_name)
# '{}_hover'.format(chest_name)
# '{}_open'.format(chest_name)
# '{}_lock'.format(chest_name)
# '{}_have_key'.format(chest_name)
# '{}_opened'.format(chest_name)

default lockpicks = 5


screen click_chest(chest1_name, chest2_name=None, chest3_name=None, chest4_name=None, chest5_name=None):
    if str_to_class("{}_opened".format(chest1_name)) != True:
        imagebutton:
            idle "images/{}_closed.png".format(chest1_name)
            hover "images/{}_hover.png".format(chest1_name)
            focus_mask True
            action Show("pick_choose", dissolve, chest1_name)

    else:
        imagebutton:
            idle "images/{}_open.png".format(chest1_name)
            hover "images/{}_open_hover.png".format(chest1_name)
            focus_mask True
            action Show("pick_choose", dissolve, chest1_name)

    if chest2_name != None:
        if str_to_class("{}_opened".format(chest2_name)) != True:
            imagebutton:
                idle "images/{}_closed.png".format(chest2_name)
                hover "images/{}_hover.png".format(chest2_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest2_name)

        else:
            imagebutton:
                idle "images/{}_open.png".format(chest2_name)
                hover "images/{}_open_hover.png".format(chest2_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest2_name)

    if chest3_name != None:
        if str_to_class("{}_opened".format(chest3_name)) != True:
            imagebutton:
                idle "images/{}_closed.png".format(chest3_name)
                hover "images/{}_hover.png".format(chest3_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest3_name)

        else:
            imagebutton:
                idle "images/{}_open.png".format(chest3_name)
                hover "images/{}_open_hover.png".format(chest3_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest3_name)

    if chest4_name != None:
        if str_to_class("{}_opened".format(chest4_name)) != True:
            imagebutton:
                idle "images/{}_closed.png".format(chest4_name)
                hover "images/{}_hover.png".format(chest4_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest4_name)

        else:
            imagebutton:
                idle "images/{}_open.png".format(chest4_name)
                hover "images/{}_open_hover.png".format(chest4_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest4_name)

    if chest5_name != None:
        if str_to_class("{}_opened".format(chest5_name)) != True:
            imagebutton:
                idle "images/{}_closed.png".format(chest5_name)
                hover "images/{}_hover.png".format(chest5_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest5_name)

        else:
            imagebutton:
                idle "images/{}_open.png".format(chest5_name)
                hover "images/{}_open_hover.png".format(chest5_name)
                focus_mask True
                action Show("pick_choose", dissolve, chest5_name)


    textbutton "Reset":
        xalign 0.5
        yalign 0.9
        text_size 60
        text_idle_color "#300"
        text_hover_color "#f00"
        text_insensitive_color "#300"
        text_selected_color "#a00"
        action [
            SetVariable("current_chest", None),
            Function(str_to_class('{}_lock'.format(chest1_name)).reset),
            Function(str_to_class('{}_lock'.format(chest2_name)).reset),
            Function(str_to_class('{}_lock'.format(chest3_name)).reset),
            Function(str_to_class('{}_lock'.format(chest4_name)).reset),
            Function(str_to_class('{}_lock'.format(chest5_name)).reset),
            If(str_to_class('{}_opened'.format(chest1_name)), true = SetVariable('{}_opened'.format(chest1_name), False)),
            If(str_to_class('{}_opened'.format(chest2_name)), true = SetVariable('{}_opened'.format(chest2_name), False)),
            If(str_to_class('{}_opened'.format(chest3_name)), true = SetVariable('{}_opened'.format(chest3_name), False)),
            If(str_to_class('{}_opened'.format(chest4_name)), true = SetVariable('{}_opened'.format(chest4_name), False)),
            If(str_to_class('{}_opened'.format(chest5_name)), true = SetVariable('{}_opened'.format(chest5_name), False)),
            If(str_to_class('{}_have_key'.format(chest1_name)), true = SetVariable('{}_have_key'.format(chest1_name), False)),
            If(str_to_class('{}_have_key'.format(chest2_name)), true = SetVariable('{}_have_key'.format(chest2_name), False)),
            If(str_to_class('{}_have_key'.format(chest3_name)), true = SetVariable('{}_have_key'.format(chest3_name), False)),
            If(str_to_class('{}_have_key'.format(chest4_name)), true = SetVariable('{}_have_key'.format(chest4_name), False)),
            If(str_to_class('{}_have_key'.format(chest5_name)), true = SetVariable('{}_have_key'.format(chest5_name), False))
        ]

screen pick_choose(chest_name):
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 300
        vbox:
            xalign 0.5
            yalign 0.5
            spacing 50

            textbutton "Open":
                xalign 0.5
                yalign 0.1
                action If(str_to_class('{}_opened'.format(chest_name)), true = [SetVariable("current_chest", chest_name), Hide("pick_choose"), Jump("opened_chest")], false = Notify("It's locked!"))
            hbox:
                xalign 0.5
                yalign 0.5
                spacing 60
                textbutton "Use a Key":
                    xalign 0.2
                    action If(str_to_class('{}_have_key'.format(chest_name)), true = [Play("Lock_Click", "audio/lock_unlock.mp3"), SetVariable("current_chest", chest_name), Hide("pick_choose"), Jump("opened_chest")], false = Notify("You don't have the key!"))
                textbutton "Pick the Lock - Lockpicks: [lockpicks]":
                    xalign 0.8
                    action [Function(str_to_class('{}_lock'.format(chest_name)).reset), SetVariable("current_chest", chest_name), Hide("pick_choose"), Show("lockpicking", dissolve, str_to_class('{}_lock'.format(chest_name)), chest_name)]

            textbutton "Cancel":
                xalign 0.5
                yalign 1.0
                action Hide("pick_choose")


screen lockpicking(lock, chest_name):
    modal True

    add "lock_dark"
    add lock:
        xalign 0.5
        yalign 0.5

    vbox:
        # Displays for debugging
        # hbox:
        #     label "Pick Position: "
        #     add "counter"
        # hbox:
        #     label "Sweet Spot: "
        #     add "counter2"
        hbox:
            label "Lockpicks: [lockpicks]"

    

screen temp_screen(chest_name):
    on "show":
        action [SetVariable('{}_opened'.format(chest_name), True), Hide("temp_screen")] #sets chest to open, doesn't lose the key for debugging purposes, this is the final in-game version
        #action [SetVariable('{}_have_key'.format(chest_name), False), Hide("temp_screen")] ###################### <---- lose the key, doesn't open the chest, for debugging purposes
        #action [SetVariable('{}_have_key'.format(chest_name), False), SetVariable('{}_opened'.format(chest_name), True), Hide("temp_screen")] ###################### <---- set the chest to "opened", loses the key, for debugging purposes

label opened_chest:
    show screen temp_screen(current_chest)
    hide screen lockpicking
    with dissolve
    "You opened the lock and found a map!"
    #"You got the loot!" #???
    window hide
    pause(1.0)
    $ current_chest = None
    jump continue_game

    
