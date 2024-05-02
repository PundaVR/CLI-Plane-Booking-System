# CLI-Plane-Booking-System
A plane booking system in the command line, highly customisable. Written in Python. School work.
Assignment is a create a plane booking system with columns ABC & DEF with 31 lines of seats.

# Requirements:
- Program loops until prompted to exit
- Passenger and Staff menus
- Seats B1, B2, B3, E1, E2, and E3 - Cannot be booked and must display as "unvavailable"

## Passengers 
Passengers must be booked one at a time
- Passenger portal loops until prompted to exit to main menu
- Ask for passenger full name and seat choice (seat booking formatted like B7, D29, etc)
- If a seat is already booked, display "Seat unavailable" and let the user try again
- Seat allocation system will distrubite weight across the plane. Columns [A B C] are grouped as one side, and [D E F] as the other. If one side has 10 more booked seats than the other, it will lock passengers from booking that side until balance has been restored (less than 10 seats more) 

## Staff
- Enter a seat (i.e. F4) and be able to view the name of the person in there
- Create or load manifest files (.txt files)
- Clear the plane's manifest