# Author: Aiden Faulconer
# Date created: October 22nd, 2019
# Date last changed: November 1st, 2019
# this program is a console application for calculating allowed mass for space exploration of given DESTINATIONS
# ...it uses a C-like procedural programming style, however due to global state we do not use pure functions, upon refactoring this program would use an object oriented paradigm to encapsulate state
# safely... this program has extensive use of list comprehension and lambda functions for a smaller and cleaner codebase
# Input: user input, Output: chosen or guided state of the console app
# Style: this program is in accordance with pythons official PEP 8 style guidee
# Input: user input with  comma seperated  numbers with max and minimum three comma seperated integers, output: none, except whats on the GUI
import py
import re as re

import tkinter as tki

import os as os

# constants, max weights apply PER ASTRONAUT, there is a total of 6 astronauts!!
MAXKG = 100
MAXSPECIALISTKG = 150


# input regex patterns, only accept valid choices and number input
CHARACTERPATTERN = '[abcdx|ABCDX]{1,}'
# will not recognize text after a special character
WORDPATTERN = '^([a-zA-Z][a-zA-Z|\s|]{1,})(?=)\1*'
# numbers must be seperated atleast three times, any further are ignored
NUMERICPATTERN = '^([\d]{1,}[,]){2}[\d]{1,}'


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

DESTINATIONS = {
    "Mercury": 0.378,
    "Venus": 0.907,
    "Moon": 0.166,
    "Mars": 0.377,
    "Io": 0.1835,
    "Europa": 0.1335,
    "Ganymede": 0.1448,
    "Callisto": 0.1264,
}

# we assume we have one global instance of a window, also for future refrence we assume we have a live render of our input
WINDOW = tki.Tk()
WINDOW.config(bg='white')
WINDOW.title("Astronaut Allowance Calculator")
WINDOW.resizable(0, 0)
WINDOW.geometry('500x600')


def calcMission():
    # calculate maximum weights given our current destinaiton

    crewRemainer = [
        *map(lambda c: int(MAXKG-c), currentmission[CREWMASS])]

    print(*currentmission[SPECIALISTMASS])

    specialistRemainer = [
        *map(lambda s: int(MAXSPECIALISTKG-s), currentmission[SPECIALISTMASS])]

    availibleMass = (*crewRemainer, *specialistRemainer)

    totalAvailibleMass = sum(availibleMass)

    if(totalAvailibleMass != 0):
        avgMass = totalAvailibleMass / 6  # we assume only 6 astronauts
    else:
        avgMass = 0

    avgDestMass = avgMass * float(DESTINATIONS[currentmission[DEST]])

    print(specialistRemainer)
    # mutate current mission state
    currentmission[TOTALAVAILIBLEMASS] = totalAvailibleMass
    currentmission[AVGAVAILIBLEMASS] = avgMass
    currentmission[AVGDESTDEFICITMASS] = avgDestMass


# the way tkinter is structured causes problems when you want to set unique attributes from variables on a loops stack, so we must handle this outside that very stack hence why I resorted to functions
# using a class would probably be a better approach but this works aswell (this takes a procedural programming approach versus an OO approach)

def renderResults():
    WINDOW.children['!label3'].config(text="""
            -------------------------------------------
            Crews masses:{0}
            Specialists masses:{1}
            -------------------------------------------
            Total remaining mass:{2} kg
            Avg remaining mass:{3:.2f} kg
            -------------------------------------------
            Avg remaining mass for {4}:
            {5: >20}{6:.2f} kg
            -------------------------------------------
            """.format(
        currentmission[CREWMASS],
        currentmission[SPECIALISTMASS],
        currentmission[TOTALAVAILIBLEMASS],
        currentmission[AVGAVAILIBLEMASS],
        currentmission[DEST], ' ', currentmission[AVGDESTDEFICITMASS]
    ), justify='left', anchor='e')

# this changes state for crew mass and specialistmass


def setMissionMass(crewMass, specialistMass):
    setState(CREWMASS, processInput(crewMass, 'numeric'))
    setState(SPECIALISTMASS, processInput(specialistMass, 'numeric'))

    # function to set the current mission state from an event in the UI (such as clicking a UI button)


def setState(key, value):
    currentmission[key] = value
    print('Changing state!')
    print('changing currentMission[{0}] value to {1}'.format(key, value))
    calcMission()  # change state
    renderResults()  # render our calculations according to new state


# configure a UI components state outside a loop, this is the only way to ensure the value is unique and not refrencing the last value of the loop
def setComponentState(key, stateKey, stateValue):
    # we access the TK window class and get a refrence to the given component class and configure it
    WINDOW.children[key].config(command=lambda: setState(stateKey, stateValue))


# this was not required for the assignment, but I wanted to make one, I will probably reuse this logic for other future small console projects
# processing for input, to handle this applications input for many edge cases (but not all)
# will break if coder does not use a valid inputtype, didnt want to spend more time on this so i leave it as is
def processInput(thisInput, inputType='default'):
    # we must see if the input returns a result with the current inputType regex
    if bool(re.search(
            *[CHARACTERPATTERN if inputType == 'default' else WORDPATTERN if inputType ==
              'word' else NUMERICPATTERN if inputType == 'numeric' else ''], thisInput
    )):
        # default only hanldes one character as input, and itll be the first occurance of a valid charecter
        if(inputType == 'default'):
            processed = str(
                re.search(CHARACTERPATTERN, thisInput).group()).split(" ")[0]
            return processed[0].upper()

        elif(inputType == 'numeric'):
            processed = [*map(int, str(
                re.search(NUMERICPATTERN, thisInput).group()).split(',')
            )]
            return processed
    else:
        return (0, 0, 0)


def main():
    # configures experience with funciton refrences, this is done because we use this config in these functions therefore we cannot assign the refrences before function declarations
    # enter a state machine from initial choice A, this state machine will never end until user enters x

    # enter default state of the current mission
    currentmission[DEST] = 'Moon'
    currentmission[CREWMASS] = (0, 0, 0)
    currentmission[SPECIALISTMASS] = (0, 0, 0)

    # destinations label
    label = tki.Label(
        WINDOW, text="Destinations", bg="lightblue", fg="black", width=25,
        padx=20, pady=20, borderwidth=0, relief="groove", highlightcolor="black", highlightthickness=4
    )

    # mission results label
    label2 = tki.Label(
        WINDOW, text="Mission results", bg="lightblue", fg="black", width=30,
        borderwidth=0, padx=20, pady=20, relief="groove", highlightcolor="white", highlightthickness=4
    )
    # results display
    label3 = tki.Label(
        WINDOW, anchor='e', width=30,
        bg="white", fg="black", borderwidth=0, padx=20, pady=20, relief="groove", highlightcolor="white", highlightthickness=4
    )

    label4 = tki.Label(
        WINDOW, justify='left',  width=10, text="Crew mass:",
        bg="white", fg="black", borderwidth=0, padx=20, pady=20, relief="ridge", highlightcolor="white", highlightthickness=4
    )
    label5 = tki.Label(
        WINDOW, justify='left', width=10, text="Specialist mass:",
        bg="white", fg="black", borderwidth=0, padx=20, pady=20, relief="ridge", highlightcolor="white", highlightthickness=4
    )

    # change each frame based on the input in entry components
    specialistMass = tki.StringVar(value='0,0,0')
    crewMass = tki.StringVar(value='0,0,0')

    entry1 = tki.Entry(
        WINDOW, width=18, textvariable=crewMass,
        bg="white", fg="black", borderwidth=2, relief="sunken", highlightcolor="lightblue", highlightthickness=4
    )
    entry2 = tki.Entry(
        WINDOW, width=18, textvariable=specialistMass,
        bg="white", fg="black", borderwidth=2, relief="sunken", highlightcolor="lightblue", highlightthickness=4
    )

    calculateButton = tki.Button(
        WINDOW, text='Calculate astronauts mass', bg="grey", fg="white", width=35,
        borderwidth=3, relief="ridge", highlightcolor="lightgrey", highlightthickness=4,
        command=lambda: setMissionMass(crewMass.get(), specialistMass.get()))
    # grid configuration at bottom for easy changing of all the UI components (its all in one spot)
    label.grid(row=0, column=0, columnspan=6)
    label2.grid(row=0, column=6, columnspan=6)
    label3.grid(row=1, rowspan=4, column=6, columnspan=2)
    renderResults()  # outsources rendering of ted on this label to a function, so we can call it every time we wish to change the text
    label4.grid(row=6, column=6)
    label5.grid(row=7, column=6)
    entry1.grid(row=6, column=7)
    entry2.grid(row=7, column=7)
    calculateButton.grid(row=8, column=6, columnspan=2)
    # for adjusting UI elements spawned from this loop
    rowCount = 1
    paddingX = 1
    paddingY = 1

    for key in DESTINATIONS:

        button = tki.Button(
            WINDOW, text=DESTINATIONS[key], bg="grey", fg="white", width=15,
            borderwidth=3, relief="ridge", highlightcolor="lightgrey", highlightthickness=4, command=lambda: setState(DEST, key)
        )

        destLabel = tki.Label(WINDOW, text=key, bg="white", fg="black", width=13,
                              borderwidth=0, relief="raised", highlightcolor="lightgrey", highlightthickness=4,)

        button.grid(row=rowCount, column=2, columnspan=3,
                    padx=paddingX, pady=paddingY)
        destLabel.grid(row=rowCount, column=0,
                       padx=paddingX, pady=paddingY,)

        rowCount += 1

        print(key)
        WINDOW.children.values().__str__()
        print(WINDOW.children['!button' + str('' if rowCount <
                                              2 else rowCount)]['command'])
        # ensures we have unique state set for a given button
        setComponentState(
            '!button' + str('' if rowCount <
                            2 else rowCount),
            DEST,
            key
        )

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
    main()
