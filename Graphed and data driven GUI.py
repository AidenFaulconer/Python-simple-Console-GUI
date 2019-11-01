# Author: Aiden Faulconer
# Date created: October 22nd, 2019
# Date last changed: November 1st, 2019
#  This program works on global state, upon further refactoring this would be encapsulated in a class but is not the current design,
# How state is handled is inspired by the React web framework where all state muct call a top level method called setState, which is the same
# in this program, even allowing cutsomization for which state we wish to modify
# Style: this program is in accordance with pythons official PEP 8 style guide
# Input: .txts with atleast 8 comma seperated lines with the first value being a string, output: none, except whats on the GUI
import py
import re as re
import collections
# for basic GUI
from tkinter.filedialog import askopenfilename
import tkinter as tki
# for graph GUI
import turtle as tur

from turtle import RawTurtle

# constants, max weights apply PER ASTRONAUT, there is a total of 6 astronauts!!
MAXKG = 100
MAXSPECIALISTKG = 150

# 'enums' so we have consistent spelling of the keys, and because im clumsy af
DEST = 'DEST'  # shorthand for destination and more distinguishable from 'DESTINATIONS'
SPECIALISTMASS = 'SPECIALISTMASS'
CREWMASS = 'CREWMASS'
AVALIBLEMASS = 'AVALIBLEMASS'
AVGAVAILIBLEMASS = 'AVGAVAILIBLEMASS'
AVGDESTDEFICITMASS = 'AVGDESTDEFICITMASS'
TOTALAVAILIBLEMASS = 'TOTALAVAILIBLEMASS'

# global dynamic state, encapsulated in a dict for ease of use,
currentmission = {
    DEST: "",
    CREWMASS: (0, 0, 0),
    SPECIALISTMASS: (0, 0, 0),
    AVALIBLEMASS: (),
    TOTALAVAILIBLEMASS: 0,
    AVGAVAILIBLEMASS: 0,
    AVGDESTDEFICITMASS: 0,
}

missions = []

DESTINATIONS = {
}

# we assume we have one global instance of a window, also for future refrence we assume we have a live render of our input
WINDOW = tki.Tk()
WINDOW.config(bg='darkgrey')
WINDOW.title("Astronaut Allowance Calculator")
WINDOW.resizable(0, 0)
WINDOW.geometry('700x700')
WIDTH, HEIGHT = 460, 500  # coordinate system size

# for graph sizing
CANVAS = tki.Canvas(WINDOW, width=WIDTH, height=HEIGHT, background='white')


GRAPH = tur.RawTurtle(CANVAS, visible=False)


listBox = tki.Listbox(
    WINDOW, bg="grey", fg="white", width=30, height=28, name='listBox',
    borderwidth=3, relief="ridge", highlightcolor="lightgrey", highlightthickness=4
)

# changes current state given new state, upon refactoring, everything here would be encapsulated in a class and this would become a static method


def calcMission():
    # calculate maximum weights given our current destinaiton

    crewRemainer = [
        *map(lambda c: int(MAXKG-c), currentmission[CREWMASS])]

    specialistRemainer = [
        *map(lambda s: int(MAXSPECIALISTKG-s), currentmission[SPECIALISTMASS])]

    availibleMass = (*crewRemainer, *specialistRemainer)

    totalAvailibleMass = sum(availibleMass)

    if(totalAvailibleMass != 0):
        avgMass = totalAvailibleMass / 6  # we assume only 6 astronauts
    else:
        avgMass = 0

    avgDestMass = avgMass * float(DESTINATIONS[currentmission[DEST]])

    # mutate current mission state
    currentmission[TOTALAVAILIBLEMASS] = totalAvailibleMass
    currentmission[AVGAVAILIBLEMASS] = avgMass
    currentmission[AVGDESTDEFICITMASS] = avgDestMass
    print('debug: {0}'.format(currentmission[AVGDESTDEFICITMASS]))


# the way tkinter is structured causes problems when you want to set unique attributes from variables on a loops stack, so we must handle this outside that very stack hence why I resorted to functions
# using a class would probably be a better approach but this works aswell (this takes a procedural programming approach versus an OO approach)

def renderResults(resultLabel):
    # remove previous data if any exists
    listBox.delete(0, tki.END)
    outputText = ''
    for mission in missions:
        outputText += """
                _____________________________________________________________________________________________________________________________________________
                For {4} Mission... Our Crews masses:{0} & Our Specialists masses:{1}..
                With Total remaining mass:{2} kg & Avg remaining mass:{3:.2f} kg... Finally our Avg remaining mass for {4} is {6:.2f} kg
                _____________________________________________________________________________________________________________________________________________
                """.format(
            mission[CREWMASS],
            mission[SPECIALISTMASS],
            mission[TOTALAVAILIBLEMASS],
            mission[AVGAVAILIBLEMASS],
            mission[DEST], ' ', mission[AVGDESTDEFICITMASS])
    resultLabel.config(text=outputText, anchor='e')


def renderCurrentDestination():
    selectedMissionResults = """
    ---------------------------------------------------------------------------------------
    Selection: {0} Crew:{1} Specialist:{2} Total Mass:{3}
    Total remaining mass:{4} Avg remaining mass: {5:.3f}
    ---------------------------------------------------------------------------------------
    """.format(currentmission[DEST], currentmission[CREWMASS], currentmission[SPECIALISTMASS], currentmission[TOTALAVAILIBLEMASS],
               currentmission[AVGAVAILIBLEMASS], currentmission[AVGDESTDEFICITMASS])
    WINDOW.children['renderCurrentDestination'].config(
        text=selectedMissionResults, justify='left', anchor='e'
    )


def renderDestinations():

    # for adjusting UI elements spawned from this loop
    rowCount = 1
    paddingX = 1
    paddingY = 1

    for key in DESTINATIONS:

        listBox.insert(rowCount, str(key))
        # create our ui components

        listBox.grid(row=1, column=1)

        rowCount += 1

    renderGraph()
# this changes state for crew mass and specialistmass

# for rendering graphs


def barDraw(turtle, key, maxheight, dataLen):
    turtle.begin_fill()  # start fillin pen outline
    turtle.left(90)
    turtle.forward(maxheight)
    # words
    turtle.write(key)

    turtle.right(90)
    # maintain a width relative to the canvas container
    turtle.forward(WIDTH/dataLen)
    turtle.right(90)
    turtle.forward(maxheight)
    turtle.left(90)
    turtle.end_fill()  # stop fillin pen outline


def renderGraph():
    # clear canvas
    GRAPH.clear()
    GRAPH.speed('slow')
    GRAPH.setheading(90)
    if len(DESTINATIONS.values()) > 0:
        dataLen = len(DESTINATIONS.values())
    else:
        return
    # NO DRAWING UNTIL BARDRAW
    GRAPH.penup()
    # set frame delay for draw speed
    GRAPH._delay(1)
    # position in bottom left corner
    GRAPH.setposition(-WIDTH/2, -HEIGHT/2)
    GRAPH._rotate(270)
    # set aesthetics
    GRAPH.color('black')
    GRAPH.fillcolor('lightblue')
    GRAPH.pensize(2)
    # WE MAY BEGIN DRAWING
    GRAPH.pendown()
    for key in DESTINATIONS:
        print(key)
        barDraw(GRAPH, key, float(DESTINATIONS[key])*HEIGHT, dataLen)

# this function sets both states at once, because I would often write these two lines repetitively


def setMissionMass(crewMass, specialistMass):
    setState(CREWMASS, crewMass)
    setState(SPECIALISTMASS, specialistMass)

    # function to set any state in this app, it defaults to mission state if no paramater is provided


def setState(key, value, stateSource=currentmission):
    stateSource[key] = value
    print('Changing state!')
    print('changing currentMission[{0}] value to {1}'.format(key, value))
    calcMission()  # change state
    # update the current mission status renderer to reflect current results
    renderCurrentDestination()


def setNewFileState():
   # WINDOW.withdraw()  # stops from spawning another window
    # show an open dialog box and return path to the choosen file
    filename = askopenfilename()
    filepath = filename.replace('/', '\\')
    readFile(filepath)

    # after we read the file we create a new window to put the results in
    ResultWindow = tki.Tk()
    ResultWindow.config(bg='black')
    ResultWindow.title("Astronaut Allowance Calculator")
    ResultWindow.resizable(0, 0)
    ResultWindow.geometry('730x880')
    resultLabel = tki.Label(
        ResultWindow, anchor='e', width=102, height=50,
        bg="white", fg="black", borderwidth=6, relief="ridge",
        highlightcolor="lightgrey", highlightthickness=4
    )
    resultLabel.grid(row=0, rowspan=3, column=0, columnspan=3)
    # now we render the results into that window
    renderResults(resultLabel)

    # draw a graph and show the destinations
    renderDestinations()


def readFile(filepath):
    global DESTINATIONS
    for line in enumerate(open(filepath)):
        processed = line[1].split(',')

        # set destination state
        setState(processed[0], processed[1], DESTINATIONS)
        # set destination state in currentmission
        setState(DEST, processed[0])
        #print("Crew data {0}".format([*map(int, processed[2:4])]))
        setMissionMass([*map(int, processed[2:5])],
                       [*map(int, processed[5:8])])
        # add the missions results, copy so we dont append a mutable refrenced dict
        missions.append(currentmission.copy())
    # sort dict in descending order
    sortDict = sorted(DESTINATIONS.items(),
                      key=lambda x: x[1], reverse=False)
    DESTINATIONS = collections.OrderedDict(sortDict)


def main():

    # to use a canvas and a grid we must use a Frame
    # enter default state of the current mission
    currentmission[DEST] = 'Mercury'
    currentmission[CREWMASS] = (0, 0, 0)
    currentmission[SPECIALISTMASS] = (0, 0, 0)

    renderDestinations()

    # destinations label
    label = tki.Label(
        WINDOW, text="Destinations", bg="lightblue", fg="black", width=25,
        padx=20, pady=20, borderwidth=0, relief="groove", highlightcolor="black", highlightthickness=4
    )

    graphlabel = tki.Label(
        WINDOW, text="Destination masses", bg="lightblue", fg="black", width=60,
        borderwidth=0, padx=20, pady=20, relief="groove", highlightcolor="white", highlightthickness=4
    )
    # button to spawn a file open dialouge
    openFileButton = tki.Button(
        WINDOW, text="Open new file", bg="tan", fg="white", width=15, name='openFileButton',
        borderwidth=3, relief="ridge", highlightcolor="lightgrey", highlightthickness=4, command=setNewFileState,
    )
    openFileButton.widgetName = 'openFileButton'

    renderCurrentDestination = tki.Label(
        WINDOW, text="please select a properly formatted text file", bg="white", fg="black", width=65, height=5, name='renderCurrentDestination',
        borderwidth=6, relief="ridge", highlightcolor="black", highlightthickness=4
    )

    label.grid(row=0, column=0, columnspan=6)
    graphlabel.grid(row=0, column=12, columnspan=6)

    openFileButton.grid(row=5, column=1)

    renderCurrentDestination.grid(row=5, column=12, columnspan=2)
    CANVAS.config(borderwidth=0.5, relief="sunken",
                  highlightcolor="lightgrey", highlightthickness=4)
    CANVAS.grid(row=1, rowspan=4, column=12, columnspan=6)

    # callback events from our listbox
    # enter gui loop so we can do polling for events and interactions
    WINDOW.bind("<<ListboxSelect>>", lambda _: setState(
        DEST, listBox.get(listBox.curselection()) if listBox.get(listBox.curselection()) != '' else 'Mercury'))

    WINDOW.mainloop()
# fg effects text color
# bg effects background color
# padx is like padding on x in css
# pady is like padding on y in css
# fill removes margin in the specified x and y

# border width creates a border with the foreground color, and sets thickness
# relief sets a variety of presets for the border styling, solid, groove, ridge, sunken, raised

# we call the mainloop which is equivilent to the render method on the top level component
# https://stackoverflow.com/questions/39416021/border-for-tkinter-label


# application works by entering D then following the prompt to calculate a "missions" mass allowance
if __name__ == "__main__":
        # creates a WINDOW object which instances TK allowing us to modify and use its contents
    main()
