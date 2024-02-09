numberOfSeats = 31

numbersPort = numberOfSeats
charactersPort = 3
seatsPort = [['[ ]' for i in range(numbersPort)] for j in range(charactersPort)]

numbersStarboard = numberOfSeats
charactersStarboard = 3
seatsStarboard = [['[ ]' for i in range(numbersStarboard)] for j in range(charactersStarboard)]

# LEVEL 3 FUNCTIONS - ERROR CHECKING + HELPERS OF HELPERS

# LEVEL 2 FUCNTIONS - HELPERS

def SeatConversion(c, n):
    newChar = 0
    newNum = n + 1
    return [newChar, newNum]

def ConvertCharacterToNum(c="A", portSide = False):
    changedChar = ord(c.upper())
    convertedNum = 0
    if changedChar < 65+charactersPort: #or portSide
        convertedNum = charactersPort-(changedChar-65)
    else:
        convertedNum = charactersStarboard-(changedChar-(65+charactersPort))

    return convertedNum

    

# LEVEL 1 FUNCTIONS - USED IN MAIN CODE

def DisplaySeats():
    seatNumbers = "  "
    for i in range(1, numberOfSeats+1):
        if i == 10:
            seatNumbers += f" {i}"
        elif i > 10:
            seatNumbers += f" {i}"
        else:
            seatNumbers += f" {i} "
        
    print(seatNumbers)


    letter = 64 + charactersPort + charactersStarboard# chr(65) = A

    for x in seatsStarboard:
        lettersStarboard = ""
        for y in x:
            lettersStarboard+=y
        
        print(f"{chr(letter)} {lettersStarboard}")
        letter-=1
        
    aisle = "  "
    for a in range(numberOfSeats):
        aisle+="==="
    print(aisle)

    for x in seatsPort:
        lettersPort = ""
        for y in x:
            lettersPort+=y
        
        print(f"{chr(letter)} {lettersPort}")
        letter-=1
    
def BookSeat(c, n):
    seatNum = n-1
    if c > charactersPort:
        seatsStarboard[c-charactersPort-2][seatNum] = "[X]"
    else:
        seatsPort[c-1][seatNum] = "[X]"


# A to C WORKS, NEED TO IMPLEMENT CONVERTCHAR IN BookSeat() AND ADD LOGIC TO DETERMINE IF ITS PORT OR STARBOARD
x = ConvertCharacterToNum("D") #A=0 B=1 C=2 --  
print(x)
BookSeat(x,2)
DisplaySeats()