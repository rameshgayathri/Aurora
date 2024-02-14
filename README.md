# Seminar-Hall-Management
**Seminar Hall Management Web Application**

---

### Overview

This repository contains the source code for a Seminar Hall Management Web Application built using Python and Flask framework. The application allows users to sign up, log in, book seminar halls, and provides an admin interface for approving or rejecting booking requests.

### Features

- **User Authentication**: Users can sign up with a username, email, and password. Existing users can log in to access their accounts.
- **Hall Booking**: Registered users can book seminar halls by specifying the hall name and booking date.
- **Admin Approval**: Admin users have the authority to approve or reject booking requests submitted by users.
- **Real-time Validation**: Client-side validation ensures data integrity and provides a seamless user experience.
- **Dynamic Content Rendering**: Booking requests and result messages are dynamically rendered using Jinja2 templating engine.

### File Structure

- **app.py**: Contains the main Flask application with routing, views, and database operations.
- **user_booking.py**: Implements the functionality for booking seminar halls.
- **templates/**: Directory containing HTML templates for various pages.
- **HallManagement.db**: SQLite database file storing user data and booking information.

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/rameshgayathri/seminar-hall-management.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Access the application in your web browser at `http://localhost:5000`.

### Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

### License

This project is licensed under the [MIT License](LICENSE).
