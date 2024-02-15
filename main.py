AppConfigs = {
    "debug": True,
    "requirePromptDisplaySeats": False
}

manifest = {} # seat : passenger 

numberOfSeats = 31

numbersPort = numberOfSeats
charactersPort = 3

seatBooked = '[X]'
seatAvailable = '[0]'

seatsPort = [[seatAvailable for i in range(numbersPort)] for j in range(charactersPort)]

numbersStarboard = numberOfSeats
charactersStarboard = 3
seatsStarboard = [[seatAvailable for i in range(numbersStarboard)] for j in range(charactersStarboard)]



# LEVEL 3 FUNCTIONS - ERROR CHECKING + HELPERS OF HELPERS

def ValidateUserInputNumbers(userInput, maxMenuNumberOption, excludeZero = False):
    validInput = False
    if (userInput.isnumeric() and int(userInput) <= maxMenuNumberOption and int(userInput) >= 0):
        if(excludeZero and userInput=="0"):
            validInput = False
        else:
            validInput = True
    return validInput

def ValidateSeatInput(seat=""):
    isValid = False
    if(len(seat) == 2):
        if (seat[0].isalpha() and seat[1].isnumeric()): # check string is 2 characters (1st is num and 2nd is char)
            if (ord(seat[0]) >= 65 and ord(seat[0]) <= (64+charactersPort+charactersStarboard) and int(seat[1]) > 0 and int(seat[1]) <= numberOfSeats):
                isValid = True
    elif(len(seat) == 3):
        if (seat[0].isalpha() and seat[1].isnumeric() and seat[2].isnumeric()): # check string is 2 characters (1st is num and 2nd is char)
            if (ord(seat[0]) >= 65 and ord(seat[0]) <= (64+charactersPort+charactersStarboard) and int(seat.split(seat[0])[-1]) > 0 and int(seat.split(seat[0])[-1]) <= numberOfSeats):
                isValid = True

    return isValid

def InputSeat():
    seat = "null"
    seatInput = input("Choose Seat (i.e. B7):\n>>>").upper()
    while(ValidateSeatInput(seatInput) == False):
        seatInput = input("Choose Seat (i.e. B7):\n>>>").upper()
    seat = seatInput
    return seat


# LEVEL 2 FUCNTIONS - HELPERS

def SeatConversion(c, n):
    newChar = 0
    newNum = n + 1
    return [newChar, newNum]

def ConvertCharacterToNum(c="A"):
    changedChar = ord(c.upper())
    convertedNum = 0
    isPortSide = False
    if changedChar < 65+charactersPort: #or portSide
        convertedNum = charactersPort-(changedChar-65)
        isPortSide =  True
    else:
        convertedNum = charactersStarboard-(changedChar-(65+charactersPort)-1)

    return (convertedNum, isPortSide)

def StoreBookingInformation(seat, passenger):
    manifest[seat]= passenger
    # store to a file as well
    print(manifest)

def SeatGet(rowStr: str, seatNumStr: str):
    isAvailable = True
    if (seatNumStr.isnumeric()):
        seatNum = int(seatNumStr)-1
        row = ConvertCharacterToNum(rowStr)[0]
        portSide = ConvertCharacterToNum(rowStr)[1]

        if portSide:
            if (seatsPort[row-1][seatNum] == seatBooked):
                isAvailable = False
        elif (seatsStarboard[row-charactersPort-2][seatNum] == seatBooked):
           isAvailable = False
        else: isAvailable = True
    return isAvailable

def SeatSet(rowStr, seatNumStr):
    success = False
    if (seatNumStr.isnumeric() and SeatGet(rowStr, seatNumStr)):
        seatNum = int(seatNumStr)-1
        row = ConvertCharacterToNum(rowStr)[0]
        portSide = ConvertCharacterToNum(rowStr)[1]
        
        if portSide:
            seatsPort[row-1][seatNum] = seatBooked
            success = True
        else:
            seatsStarboard[row-charactersPort-2][seatNum] = seatBooked
            success = True
    else:
        print("Seat unavailable")
    return success

def SeatLookup(seat: str):
    
    seatInfo = manifest.get(seat)
    if (seatInfo is None):
        print("Seat Available")
    else:
        print(seatInfo)
        

# LEVEL 1 FUNCTIONS - USED IN MAIN CODE

def DisplaySeats(display = False):
    # Check if user wants to display the seat layout
    if (display == False and AppConfigs["requirePromptDisplaySeats"]):
        inp = input("Display seating diagram? y/n\n")
        print("\n")
        if(inp.lower() != "y"):
            return
    
    # Display Seat Numbers
    seatNumbers = "  "
    for i in range(1, numberOfSeats+1):
        if i == 10:
            seatNumbers += f" {i}"
        elif i > 10:
            seatNumbers += f" {i}"
        else:
            seatNumbers += f" {i} "
        
    print(seatNumbers)

    # Display Starboard (Right) Seats
    letter = 64 + charactersPort + charactersStarboard# chr(65) = A

    for x in seatsStarboard:
        lettersStarboard = ""
        for y in x:
            lettersStarboard+=y
        
        print(f"{chr(letter)} {lettersStarboard}")
        letter-=1
<<<<<<< HEAD

    # Display Middle Walkway 
    walkway = "  "
=======
        
    aisle = "  "
>>>>>>> 0cd80da841c48b891341fe084744600606dd3cc9
    for a in range(numberOfSeats):
        aisle+="==="
    print(aisle)

    # Display Port (Left) Seats
    for x in seatsPort:
        lettersPort = ""
        for y in x:
            lettersPort+=y
        
        print(f"{chr(letter)} {lettersPort}")
        letter-=1
    
def BookSeat(rowStr: str, seatNumStr: str, passengerFullName = "Seat Unavailable"):
    success = SeatSet(rowStr, seatNumStr)

    if success == True:
        StoreBookingInformation(f"{rowStr}{seatNumStr}", passengerFullName)
    return success

def BlockSeats():
    BookSeat("B", "1") # B1
    BookSeat("B", "2") # B2
    BookSeat("B", "3") # B3
    BookSeat("E", "1") # E1
    BookSeat("E", "2") # E2
    BookSeat("E", "3") # E3


def DisplayMenu():
    # display menu options
    print("\n\n1. Passenger Portal")
    print("2. Staff Portal")
    print("0. Exit Program")
    inp = input("Select an option: ")
    while (ValidateUserInputNumbers(inp, 2) is False):
        inp = input("Invalid Input!\nSelect an option: ")
    match (inp):
        case "0":
            quit()
        case "1":
            PassengerPortal()
        case "2": 
            StaffPortal()


def StaffPortal():
    # display menu options
    print("1. Seat Lookup")
    print("0. Return to Menu")
    inp = input("Select an option: ")
    while (ValidateUserInputNumbers(inp, 1) is False):
        inp = input("Invalid Input!\nSelect an option: ")
    match (inp):
        case "0":
            DisplayMenu()
        case "1":
            DisplaySeats(True)
            seat = InputSeat()
            SeatLookup(seat)


def PassengerPortal():
    DisplaySeats()
    passengerFullName = input("Enter full name:\n")
    
    passengerSeat = InputSeat()

    while(BookSeat(passengerSeat[0], passengerSeat.split(passengerSeat[0])[-1], passengerFullName) is False):
        passengerSeat = InputSeat()
    print("Booked Seat!")



def BookingSystem():
    # clear database etc etc
    BlockSeats()
    while(True):
        DisplayMenu()

def UnitTest_UserInputs():
    print("TESTING FUNCTION: ValidateUserInputNumbers()")
    for i in range(-1, 10, 1):
        print(f"{i} -> (maxNumber = 5, excludeZero = False): {ValidateUserInputNumbers(str(i), 5)}")
        print(f"{i} -> (maxNumber = 2, excludeZero = True): {ValidateUserInputNumbers(str(i), 2, True)}")

def UnitTest_SeatInputs():
    print("TESTING FUNCTION: ValidateSeatInput()")
    for i in range(-2, 10):
        print(f"{chr(i+64)}{3*i} : {ValidateSeatInput(f'{chr(i+65)}{3*i}')}")
        print(f"{chr(i+80)}{3+(i*2)} : {ValidateSeatInput(f'{chr(i+80)}{3+(i*2)}')}")
        
def UnitTest_BookSeat():
    pass

def UnitTest_SeatSet():
    pass

def UnitTest_SeatGet():
    pass

def UnitTest_SeatLookup():
    pass

#UnitTest_UserInputs()
#UnitTest_SeatInputs()
#
BookingSystem()

