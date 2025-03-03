# Flight schedule and booking

Welcome to the Flight schedule and booking – a sophisticated **Django** application engineered to replicate the complex operations of a modern airport. This project exemplifies advanced web development practices by integrating a robust backend with an intuitive, user-centric interface. Utilizing a highly secure **PostgreSQL** database, all essential data—from user profiles to flight schedules and ticket reservations—is meticulously managed and safeguarded.

---

## 🚀 Features

### 1. **User Authentication & Security**
- **Register/Login/Logout**: Seamless account creation and secure access.
- **Password Management**: Effortless password changes with robust security.
- **Email Confirmation**: Mandatory email verification ensures valid user accounts.
- **Advanced Security Measures**:
  - **Login Protection**: Three failed login attempts within two minutes trigger an automatic email alert to administrators about potential suspicious activity.
  - **Username Guard**: Any attempt to register with the username "admin" is instantly rejected, and administrators receive an alert—keeping the system secure at all times.

### 2. **Flight Management**
- **Detailed Flight Listings**: View comprehensive details including departure and destination points, precise schedules, and pricing information.
- **Admin Control**: Easily add, update, or remove flight records directly in the PostgreSQL database.
- **Promotional Alerts**: Stay informed with email notifications about exclusive flight promotions based on your interests.

### 3. **Real-Time Booking System**
- **Dynamic Ticket Booking**: Add or remove flight tickets using a responsive virtual shopping cart.
- **Instant Updates**: Enjoy real-time updates to your cart’s total ticket count through powerful JavaScript functionality.

### 4. **Interactive Contact Page**
- **Comprehensive Contact Form**: Reach out with ease using a form that captures essential details:
  - First Name, Last Name, and Birth Date
  - Email and Email Confirmation (ensuring accuracy)
  - Message Type (Complaint, Question, Review, Request, Appointment)
  - Subject, Minimum Waiting Days, and an Elaborate Message
- **Smart Validations**:
  - Email consistency checks.
  - Age verification to ensure the sender is of legal age.
  - Word count limits (5 to 100 words) and hyperlink restrictions for clean, genuine messages.
  - Mandatory message signature for authenticity.

### 5. **Automated Task Management**
- **User Cleanup**: Automatically delete accounts that haven’t confirmed their email addresses.
- **Newsletter Dispatch**: Send engaging newsletters to users registered for over a day.
- **Ticket Expiry**: Remove outdated flight tickets seamlessly.
- **Weekly Performance Report**: Receive detailed reports on new user registrations and ticket sales, keeping administrators in the loop.

### 6. **Custom Error Handling**
- **403 Error Page**: A custom error page that informs users that access to the requested resource is forbidden. If a user is logged in, the error message displays their username to indicate which account encountered the issue; otherwise, a generic access-denied message is shown.
- **Dynamic Messaging**: Customizable error messages ensure clear, context-sensitive feedback.

---

## 🗄️ Database

All vital data is securely managed within a **PostgreSQL database**, including:
- **User Data**: Profiles, authentication details, and personal information.
- **Flight Information**: Comprehensive details on departures, destinations, schedules, and pricing.
- **Booking & Ticket Data**: Real-time management of ticket purchases and reservations.
- **Contact Form Submissions**: Securely stored messages for future reference.


