# Agenda Purpose

Agenda Purpose is a Flask-based web application designed for managing meeting agendas, resolutions, and related information. The application provides a user-friendly interface to add, edit, delete, and search for meeting entries, facilitating efficient management of meeting records.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Add and manage meeting entries with detailed information.
- Upload and preview various file types associated with meetings (e.g., documents, images, videos).
- Search for meetings based on specific criteria.
- View a timeline of related meetings.
- Responsive design for a seamless user experience on different devices.

## Prerequisites

- Python 3.12
- Pipenv

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pchapha/agenda-project.git
   ```
   
2. Install dependencies using Pipenv::

   ```bash
   pipenv install
   ```

## Configuration

Update the Flask application configuration in app.py:

```python
# Set the Flask secret key
app.secret_key = 'your_secret_key_here'

# Update the database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/agendadb'
```
Replace your_secret_key_here, username, and password with appropriate values.

## Database Setup

Before running the application, you need to set up the PostgreSQL database and create the necessary table. Follow these steps to configure the database:

1. **Create PostgreSQL Database:**
   - Ensure you have PostgreSQL installed on your system.
   - Create a new database, for example, "agendadb."

2. **Execute SQL Script:**
   - Use a PostgreSQL client or command-line tools to connect to your database.
   - Copy and execute the following SQL script to create the "agenda" table with the specified columns:

   ```sql
   -- Table: public.agenda

   -- DROP TABLE IF EXISTS public.agenda;

   CREATE TABLE IF NOT EXISTS public.agenda
   (
       meeting_id integer NOT NULL DEFAULT nextval('agenda_id_seq'::regclass),
       meeting_count integer,
       workyear integer,
       date date,
       agenda_number numeric(3,1),
       purpose character(255) COLLATE pg_catalog."default",
       agenda_name character(1000) COLLATE pg_catalog."default",
       resolution text COLLATE pg_catalog."default",
       note text COLLATE pg_catalog."default",
       department character(255) COLLATE pg_catalog."default",
       status character(255) COLLATE pg_catalog."default",
       is_first_time boolean,
       related_meeting integer,
       committee character(255) COLLATE pg_catalog."default"
   )

   TABLESPACE pg_default;

   ALTER TABLE IF EXISTS public.agenda
       OWNER to pym;
   
## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Visit http://127.0.0.1:5000/ in your web browser.
3. Interact with the application to manage meeting agendas and related information.

## Contributing

Contributions are highly encouraged! The project is actively seeking assistance to fix various bugs, make adjustments, and enhance features. Here are some areas that need attention:

1. **Bug Fixes and Adjustments:** The project currently has several bugs and requires adjustments. If you encounter issues or have suggestions for improvements, please open an issue or submit a pull request.

2. **Upload Function Enhancement:** The upload function is not complete yet. Consider contributing to enhance this functionality. Some specific areas that need attention include:

    - **Save Files According to Meeting ID:** Files should be saved in folders corresponding to their meeting_id for better organization.

    - **Display Corresponding Files for Each Meeting ID:** Create a space or page within the application to display and manage files associated with each meeting_id.

3. **Improve Data Presentation with Datatables:**
   Utilize the Datatables library to enhance the presentation of data on the index page. This can improve sorting, searching, and overall data interaction.

4. **Apply the Xenon Theme for a Beautiful Interface:**
   Implement the Xenon theme to enhance the visual appeal of the application. A more beautiful interface contributes to a positive user experience.

5. **Use Dropdowns for Some Input Fields:**
   Enhance user interaction by converting certain input fields into dropdowns. This can improve the ease of selection and contribute to a more intuitive interface.

6. **Rename Columns or Adjust for Better Alignment with Requirements:**
   Review and adjust column names to ensure they align better with project requirements. This helps in maintaining consistency and clarity in data representation.

7. **Adjust UX/UI for a Better User Experience:**
   Contribute to the improvement of the User Experience (UX) and User Interface (UI) design. Make adjustments to create a more user-friendly and intuitive application.

Your help is essential for the continuous improvement of the project.


