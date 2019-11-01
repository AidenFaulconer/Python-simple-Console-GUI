# Author: Aiden Faulconer
# Date created: October 22nd, 2019
# Date last changed: November 1st, 2019
# this program is a console application for calculating allowed mass for space exploration of given destinations
# ...it uses a C-like state machine pattern-paradigm, with extensive use of list comprehension and lambda functions for a smaller and cleaner codebase
# Input: user input, Output: chosen or guided state of the console app
# Style: this program is in accordance with pythons official PEP 8 style guide
import re as re

# constants, max weights apply PER ASTRONAUT, there is a total of 6 astronauts!!
MAXKG = 100  # 300 max for three astronauts
MAXSPECIALISTKG = 150  # 750 max for three astronauts without weight offset applied
destinations = {
    "Mercury": 0.378,
    "Venus": 0.907,
    "Moon": 0.166,
    "Mars": 0.377,
    "Io": 0.1835,
    "Europa": 0.1335,
    "Ganymede": 0.1448,
    "Callisto": 0.1264,
}
# default state for app (could change during runtime, but shouldn't in this case)
DEFAULTCHOICE = 'A'

# input regex patterns, only accept valid choices and number input
CHARACTERPATTERN = '[abcdx|ABCDX]{1,}'
# will not recognize text after a special character
WORDPATTERN = '^([a-zA-Z][a-zA-Z|\s|]{1,})(?=)\1*'
# numbers must be seperated atleast three times, any further are ignored
NUMERICPATTERN = '^([\d]{1,}[,]){2}[\d]{1,}'


# 'enums' so we have consistent spelling of the keys, and because im clumsy af
DEST = 'DEST'  # shorthand for destination and more distinguishable from 'destinations'
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


# possible states [configured at main()], THIS IS NOT A CONSTANT AND WILL NOT BE CAPITALIZED AS SUCH
# main proprietor of the state machine, functions callback to the refrenced funcitons in here usually
choices = {}

# NOTE two distinct mass calculations, crew and specailaist
# functions that compute values based on current state in destinations


def calcMission():
    # calculate maximum weights given our current destinaiton

    crewRemainer = [
        *map(lambda a: int(MAXKG-a), currentmission[CREWMASS])]
    specialistRemainer = [
        *map(lambda a: int(MAXSPECIALISTKG-a), currentmission[SPECIALISTMASS])]
    availibleMass = (*crewRemainer, *specialistRemainer)
    totalAvailibleMass = sum(availibleMass)

    # print("Availible mass for astronauts:{0}  {1}".format(
    #     crewRemainer, specialistRemainer))

    if(totalAvailibleMass != 0):
        avgMass = totalAvailibleMass / 6  # we assume only 6 astronauts
    else:
        avgMass = 0
    avgDestMass = avgMass * destinations[currentmission[DEST]]
    # mutate current mission state
    currentmission[TOTALAVAILIBLEMASS] = totalAvailibleMass
    currentmission[AVGAVAILIBLEMASS] = avgMass
    currentmission[AVGDESTDEFICITMASS] = avgDestMass


def printMenu():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Astronaut Mass Allowence Calculator")
    print("A: Display Program options")
    print("B: Display destinations with Mass Multipliers")
    print("C: Display current summary")
    print("D: Calculate a missions availible mass")
    print("X: Exit program")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # modify choice, seperated into a function in case we ever change how we handle input
    return choices[processInput(input())]()


def showSummary():
    print("----------------------------------------------------")
    print("Destination: {0}".format(currentmission[DEST]))
    print("Total Availible Mass for Crew Members:{0}".format(
        currentmission[CREWMASS]))
    print("Total Availible Mass for Specialists:{0}".format(
        currentmission[SPECIALISTMASS]))
    print("----------------------------------------------------")
    print("Total availible mass {0} kg".format(
        currentmission[TOTALAVAILIBLEMASS]))
    print("----------------------------------------------------")
    print("Average availible mass  is {0:.6f} kg".format(
        currentmission[AVGAVAILIBLEMASS]))
    print("----------------------------------------------------")
    print("Average availible weight on {0} is {1:.6f} kg".format(
        currentmission[DEST], currentmission[AVGDESTDEFICITMASS]))
    print("----------------------------------------------------")
    return choices[DEFAULTCHOICE]()


def showDestinations():
    # apply to globals
    print("====================================================")
    print("Availible destinations:")
    # adds a newline to each listed destination
    print(*map(lambda k: "destination:"+str(k) +
               "mass multiplier:"+str(destinations[k])+"\n", destinations))
    print("====================================================")
    return choices[DEFAULTCHOICE]()


def createMission():
    # apply inputs to global mission state holder
    print("================================================")
    print("Please enter a destination, your choices are")
    print(*map(lambda a: a+"\n", destinations))
    print("================================================")
    missiondestination = processInput(input(), 'word')

    print("================================================")
    print("Please enter tool weights for crew members:")
    print("================================================")
    missioncrewmass = processInput(input(), 'numeric')

    print("================================================")
    print("Please enter tool weights for crew specialists:")
    print("================================================")
    missionSPECIALISTMASS = processInput(input(), 'numeric')

    # change current state
    currentmission[DEST] = missiondestination
    currentmission[CREWMASS] = missioncrewmass
    currentmission[SPECIALISTMASS] = missionSPECIALISTMASS
    # compute current state
    calcMission()  # calculates mass from current state, modifying it since I assuming we will not need to remember the original tool weights after the calculation

    return choices['C']()  # prints a summarry


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

        # we assume the destinations are title cased
        elif(inputType == 'word'):
            processed = str(
                re.search(WORDPATTERN, thisInput).group()).split(" ")[0]
            if processed.title() in destinations.keys():
                return processed.title()
            else:
                print("please input a valid destination")
                processInput(input(), 'word')

    else:
        print(
            "You must enter atleast one valid input, try a number, a valid choice, or word")
        # recursivly check input until its valid input (input that will return something from the reges)
        print(inputType)
        return processInput(input(), inputType)

# this applicaiton is highly scalable and configurable because of how its structured, everything is a sort of modular state we can add in or remove


def main():
    # configures experience with funciton refrences, this is done because we use this config in these functions therefore we cannot assign the refrences before function declarations
    # enter a state machine from initial choice A, this state machine will never end until user enters x
    choices['A'] = printMenu
    choices['B'] = showDestinations
    choices['C'] = showSummary
    choices['D'] = createMission
    choices['X'] = exit
    # enter default state of the current mission
    currentmission[DEST] = 'Moon'
    currentmission[CREWMASS] = (100, 100, 100)
    currentmission[SPECIALISTMASS] = (150, 150, 150)
    calcMission()
    # currentmission[AVGAVAILIBLEMASS] = mass[0]
    # currentmission[AVGDESTDEFICITMASS] = mass[0]
    # end of program configuration
    return choices[DEFAULTCHOICE]()


# application works by entering D then following the prompt to calculate a "missions" mass allowance
if __name__ == "__main__":
    main()
