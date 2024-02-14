import sqlite3

def book_hall(user_name, hall_name, booking_date):
    try:
        connection = sqlite3.connect("HallManagement.db")
        cursor = connection.cursor()
        
        # Check if there is already a booking for the same hall and date
        cursor.execute("SELECT * FROM bookings WHERE hall_name = ? AND booking_date = ?", (hall_name, booking_date))
        existing_booking = cursor.fetchone()
        if existing_booking:
            return "A booking for the same hall and date already exists."
        # If no existing booking found, proceed to insert the new booking
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
                            id INTEGER PRIMARY KEY,
                            user_name TEXT NOT NULL,
                            hall_name TEXT NOT NULL,
                            booking_date DATE NOT NULL,
                            status TEXT NOT NULL
                        )''')

        cursor.execute('''INSERT INTO bookings (user_name, hall_name, booking_date, status)
                          VALUES (?, ?, ?, ?)''', (user_name, hall_name, booking_date, 'Pending'))

        connection.commit()
        return "Booking request submitted successfully!"
    except sqlite3.Error as error:
        return f"Failed to book hall: {error}"
    finally:
        connection.close()
