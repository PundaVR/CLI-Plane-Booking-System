AppConfigs = {
    "debug": True,
    "requirePromptDisplaySeats": False
}

manifest = {} # seat : passenger 
global manifestFile 
manifestFile = "manifest_0.txt"
#bookingsPort = int(0)
#bookingsStarboard = int(0)
sideBalanceThreshold = 10 # how many seats extra before side balancing occurs

numberOfSeats = 31

numbersPort = numberOfSeats
charactersPort = 3

seatBooked = '[X]'
seatAvailable = '[ ]'
A320_array = [[seatAvailable]*31]*6


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
    if(AppConfigs["debug"]): print(f"> validInput: {validInput}")
    return validInput

def ValidateSeatInput(seat=""):
    validInput = False
    if(len(seat) == 2):
        if (seat[0].isalpha() and seat[1].isnumeric()): # check string is 2 characters (1st is num and 2nd is char)
            if (ord(seat[0]) >= 65 and ord(seat[0]) <= (64+charactersPort+charactersStarboard) and int(seat[1]) > 0 and int(seat[1]) <= numberOfSeats):
                validInput = True
    elif(len(seat) == 3):
        if (seat[0].isalpha() and seat[1].isnumeric() and seat[2].isnumeric()): # check string is 2 characters (1st is num and 2nd is char)
            if (ord(seat[0]) >= 65 and ord(seat[0]) <= (64+charactersPort+charactersStarboard) and int(seat.split(seat[0])[-1]) > 0 and int(seat.split(seat[0])[-1]) <= numberOfSeats):
                validInput = True
    if(AppConfigs["debug"]): print(f"> RETURN: validInput: {validInput}")
    return validInput

def InputSeat():
    seat = "null"
    seatInput = input("Choose Seat (i.e. B7):\n>>>").upper()
    while(ValidateSeatInput(seatInput) == False):
        seatInput = input("Choose Seat (i.e. B7):\n>>>").upper()
    seat = seatInput
    if(AppConfigs["debug"]): print(f"> RETURN: seat: {seat}")
    return seat

def ResetSeats(saveToManifestFile = False):
    if(AppConfigs["debug"]): print(f"ResetSeats()")
    manifest.clear()
    if saveToManifestFile: StoreBookingInformation(skipNewBooking=True)

    # Set all seats on the port side to Available side
    for seatNum in range(1, numberOfSeats+1, 1):
        for character in range(charactersPort):
            SeatSet(f"{chr(65+character)}", f"{seatNum}", True, True)

    # Set all seats on the starboard side to Available status
    for seatNum in range(1, numberOfSeats+1, 1):
        for character in range(charactersStarboard):
            SeatSet(f"{chr(65+charactersPort+character)}", f"{seatNum}", True, True)
    
   
def LoadManifestFile(getFilePath = False):
    global manifestFile
    filePath = manifestFile # default session filepath
    ResetSeats()
    if getFilePath:
        filePath = input("Enter Manifest File Name:\n>>> ")
        manifestFile = filePath

    if(AppConfigs["debug"]): print(f"LoadManifestFile(filePath = {filePath})")
    manifestData = "data"
    newManifest = {}
    try:
        with open(filePath, "r") as f:
            if(AppConfigs["debug"]): print(f"> filePath {manifestFile} Exists")
    except:
        with open(filePath, "x") as f:
            manifestFile = filePath
            if(AppConfigs["debug"]): print(f"> Created new file: {manifestFile}")
        
    with open(manifestFile, "r") as f:
        manifestData = f.read()
    
    

    for entry in manifestData.replace(",", "").splitlines():#.split(","):
        print(f">> {entry}")
        newManifest[entry.split("-")[0]]=entry.split("-")[1]
    print(manifestData)

    print("----")
    for seat, name in manifest.items():
        #manifest[seat] = name
        print(f"{seat} | {name}")
    print("----")
    #manifest.clear()
    for seat, name in newManifest.items():
        manifest[seat] = name
        print(f"{seat} | {name}")

    print("------")
    
    

def AssignSeatsFromManifest():
    if(AppConfigs["debug"]): print(f"AssignSeatsFromManifest()")

    # Clear all seats
    k = 0
    for i in seatsPort:
        for j in range(0,len(i)):
            seatsPort[k][j] = seatAvailable
        k+=1
    z = 0
    for x in seatsStarboard:
        for y in range(0,len(x)):
            seatsStarboard[z][y] = seatAvailable
        z+=1

    # Re-assign all seats in the manifest
    for seat in manifest:
        print(f"SEAT IN MANIFEST: {seat}")
        if(len(seat) == 3):
            SeatSet(seat[0], f"{seat[1]}{seat[2]}")
        else:
            SeatSet(seat[0], seat[1])

def BalanceLockSide(portSide : bool):
    if(AppConfigs["debug"]): print(f"ResetSeats(portSide: {portSide})")

    if portSide:
        a = 0
        for i in seatsPort:
            for j in range(0,len(i)):
                seatsPort[a][j] = seatBooked
            a+=1
    else:
        z = 0
        for x in seatsStarboard:
            for y in range(0,len(x)):
                seatsStarboard[z][y] = seatBooked
            z+=1


def UpdateBookingSides():
    if(AppConfigs["debug"]): print(f"UpdateBookingSides()")

    bookingsPort = 0
    bookingsStarboard = 0
    for seat in manifest:
        if (ord(seat[0]) >= 65+charactersPort):
            bookingsStarboard+=1
        elif (ord(seat[0]) >= 65):
            bookingsPort+=1
    if(AppConfigs["debug"]): print(f"> RETURN: [bookingsPort: {bookingsPort}, bookingsStarboard: {bookingsStarboard}]")
    return [bookingsPort, bookingsStarboard]
        

def SideBalancer():
    if(AppConfigs["debug"]): print(f"SideBalancer()")

    bookingSides = UpdateBookingSides()
    bookingsPort = bookingSides[0]
    bookingsStarboard = bookingSides[1]

    if (bookingsPort-bookingsStarboard >= sideBalanceThreshold):
        if(AppConfigs["debug"]): print(f"> PORT >{sideBalanceThreshold} STARBOARD")
        BalanceLockSide(True)

    elif (bookingsStarboard-bookingsPort >= sideBalanceThreshold):
        if(AppConfigs["debug"]): print(f"> STARBOARD >{sideBalanceThreshold} PORT")
        BalanceLockSide(False)

    else:
        AssignSeatsFromManifest()



# LEVEL 2 FUCNTIONS - HELPERS

def SeatConversion(c, n):
    if(AppConfigs["debug"]): print(f"SeatConversion(c: {c}, n: {n})")
    newChar = 0
    newNum = n + 1
    if(AppConfigs["debug"]): print(f"> RETURN: [newChar: {newChar}, newNum: {newNum}]")
    return [newChar, newNum]

def ConvertCharacterToNum(c="A"):
    if(AppConfigs["debug"]): print(f"ConvertCharacterToNum(c: {c})")
    changedChar = ord(c.upper())
    convertedNum = 0
    isPortSide = False
    if changedChar < 65+charactersPort: #or portSide
        convertedNum = charactersPort-(changedChar-65)
        isPortSide =  True
    else:
        convertedNum = charactersStarboard-(changedChar-(65+charactersPort)-1)
    if(AppConfigs["debug"]): print(f"> RETURN: (convertedNum: {convertedNum}, isPortSide: {isPortSide})")
    return (convertedNum, isPortSide)

def StoreBookingInformation(seat="A1", passenger="FirstName LastName", skipNewBooking = False):
    if(AppConfigs["debug"]): print(f"StoreBookingInformation(seat: {seat}, passenger: {passenger})")
    if skipNewBooking == False:
        manifest[seat] = passenger
    
    manifestStr = ""
    for key, value in manifest.items():
        manifestStr += f"{key}-{value},\n"
    print(manifestStr)
    with open(manifestFile, 'w') as file:
        file.write(manifestStr)
    # store to a file as well
    #print(manifest)

def SeatGet(rowStr: str, seatNumStr: str, override = False):
    if(AppConfigs["debug"]): print(f"SeatGet(rowStr: {rowStr}, seatNumStr: {seatNumStr}, override: {override})")
    isAvailable = True
    if (seatNumStr.isnumeric()):
        seatNum = int(seatNumStr)-1
        conversion = ConvertCharacterToNum(rowStr)
        row = conversion[0]
        portSide = conversion[1]

        if portSide:
            if (seatsPort[row-1][seatNum] == seatBooked):
                isAvailable = False
        elif (seatsStarboard[row-charactersPort-2][seatNum] == seatBooked):
           isAvailable = False
        else: isAvailable = True
    if override:
            isAvailable = True
    if(AppConfigs["debug"]): print(f"> RETURN: isAvailable: {isAvailable}")
    return isAvailable

def SeatSet(rowStr, seatNumStr, override = False, makeSeatAvailable = False):
    if(AppConfigs["debug"]): print(f"SeatSet(rowStr: {rowStr}, seatNumStr: {seatNumStr}, override: {override}, makeSeatAvailable: {makeSeatAvailable})")
    success = False
    seatSymbol = seatBooked
    if (makeSeatAvailable):
        seatSymbol = seatAvailable
    
    if (seatNumStr.isnumeric() and SeatGet(rowStr, seatNumStr, override)):
        seatNum = int(seatNumStr)-1
        conversion = ConvertCharacterToNum(rowStr)
        row = conversion[0]
        portSide = conversion[1]
        
        if portSide:
            seatsPort[row-1][seatNum] = seatSymbol
            success = True
        else:
            seatsStarboard[row-charactersPort-2][seatNum] = seatSymbol
            success = True
    else:
        print("Seat unavailable")
    if(AppConfigs["debug"]): print(f"> RETURN: success: {success}")
    return success

def SeatLookup(seat: str):
    if(AppConfigs["debug"]): print(f"SeatLookup(seat: {seat})")
    seatInfo = manifest.get(seat)
    if (seatInfo is None):
        print("Seat Available")
    else:
        print(seatInfo)
    input("Press enter to continue...")


# LEVEL 1 FUNCTIONS - USED IN MAIN CODE

def DisplaySeats(display = False):
    if(AppConfigs["debug"]): print(f"DisplaySeats(display: {display})")
    # Check if user wants to display the seat layout
    if (display == False and AppConfigs["requirePromptDisplaySeats"]):
        inp = input("Display seating diagram? y/n\n")
        print("\n")
        if(inp.lower() != "y"):
            if(AppConfigs["debug"]): print(f"> RETURN")
            return
    SideBalancer()
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

    # Display Middle Walkway 
    walkway = "  "
    for a in range(numberOfSeats):
        walkway+="==="
    print(walkway)

    # Display Port (Left) Seats
    for x in seatsPort:
        lettersPort = ""
        for y in x:
            lettersPort+=y
        
        print(f"{chr(letter)} {lettersPort}")
        letter-=1
    
def BookSeat(rowStr: str, seatNumStr: str, passengerFullName = "Seat Unavailable"):
    if(AppConfigs["debug"]): print(f"BookSeat(rowStr: {rowStr}, seatNumStr: {seatNumStr}, passengerFullName: {passengerFullName})")
    success = SeatSet(rowStr, seatNumStr)

    if (success == True):
        StoreBookingInformation(f"{rowStr}{seatNumStr}", passengerFullName)

    if(AppConfigs["debug"]): print(f"> RETURN: success: {success}")
    return success

def BlockSeats():
    if(AppConfigs["debug"]): print(f"BlockSeats()")
    BookSeat("B", "1") # B1
    BookSeat("B", "2") # B2
    BookSeat("B", "3") # B3
    BookSeat("E", "1") # E1
    BookSeat("E", "2") # E2
    BookSeat("E", "3") # E3
    #UnitTest_BookSeat()


def DisplayMenu():
    if(AppConfigs["debug"]): print(f"DisplayMenu()")
    # display menu options
    if (DisplaySeats(AppConfigs["requirePromptDisplaySeats"])): DisplaySeats()
    print("\n1. Passenger Portal")
    print("2. Staff Portal")
    print("0. Exit Program")
    inp = input("Select an option: ")
    while (ValidateUserInputNumbers(inp, 4) is False):
        inp = input("Invalid Input!\nSelect an option: ")
    match (inp):
        case "0":
            quit()
        case "1":
            PassengerPortal()
        case "2": 
            StaffPortal()



def StaffPortal():
    if(AppConfigs["debug"]): print(f"StaffPortal()")
    # display menu options
    print("1. Seat Lookup")
    print("2. Clear Manifest")
    print("3. Load Manifest")
    print("0. Return to Menu")
    inp = input("Select an option: ")
    while (ValidateUserInputNumbers(inp, 4) is False):
        inp = input("Invalid Input!\nSelect an option: ")
    match (inp):
        case "0":
            DisplayMenu()
        case "1":
            DisplaySeats(True)
            seat = InputSeat()
            SeatLookup(seat)
        case "2":
            ResetSeats()
        case "3":
            LoadManifestFile(True)


def PassengerPortal():
    if(AppConfigs["debug"]): print(f"PassengerPortal()")
    DisplaySeats()
    passengerFullName = input("Enter full name:\n")
    
    passengerSeat = InputSeat()
    while(BookSeat(passengerSeat[0], passengerSeat.split(passengerSeat[0])[-1], passengerFullName) is False):
        passengerSeat = InputSeat()
    print("Booked Seat!")



def BookingSystem():
    if(AppConfigs["debug"]): print(f"BookingSystem()")
    # clear database etc etc
    BlockSeats()
    while(True):
        DisplayMenu()
        


def UnitTest_ValidateUserInputNumbers():
    print("TESTING FUNCTION: ValidateUserInputNumbers()")
    for i in range(-1, 10, 1):
        print(f"{i} -> (maxNumber = 5, excludeZero = False): {ValidateUserInputNumbers(str(i), 5)}")
        print(f"{i} -> (maxNumber = 2, excludeZero = True): {ValidateUserInputNumbers(str(i), 2, True)}")

def UnitTest_ValidateSeatInput():
    print("TESTING FUNCTION: ValidateSeatInput()")
    for i in range(-2, 10):
        print(f"{chr(i+64)}{3*i} : {ValidateSeatInput(f'{chr(i+65)}{3*i}')}")
        print(f"{chr(i+80)}{3+(i*2)} : {ValidateSeatInput(f'{chr(i+80)}{3+(i*2)}')}")
        
def UnitTest_ResetSeats():
    pass

def UnitTest_LoadManifestFile():
    pass

def UnitTest_AssignSeatsFromManifest():
    pass

def UnitTest_BalanceLockSide():
    pass

def UnitTest_UpdateBookingSides():
    pass

def UnitTest_SideBalancer():
    pass

def UnitTest_SeatConversion():
    pass

def UnitTest_StoreBookingInformation():
    pass

def UnitTest_SeatGet():
    pass

def UnitTest_SeatSet():
    pass

def UnitTest_SeatLookup():
    pass

def UnitTest_DisplaySeats():
    pass

def UnitTest_BookSeat():
    for i in range(10):
        BookSeat("A", f"{i}")
    BookSeat("D", "9")
    BookSeat("B", "9")

def UnitTest_BlockSeats():
    pass

def UnitTest_DisplayMenu():
    pass

def UnitTest_StaffPortal():
    pass

def UnitTest_PassengerPortal():
    pass

def UnitTest_BookingSystem():
    pass    

#ResetSeats()
BookingSystem()
#LoadManifestFile()
#BlockSeats()
#DisplaySeats()