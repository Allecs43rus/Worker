# WORKER
#### Video Demo:  <URL https://youtu.be/OhO7lAmGIGA>
#### Description:
A web application that runs on the flask framework.

The project folder includes several files and folders:
- The static folder includes: 
  - the css file that is responsible for the appearance of the pages
  - Several pictures that are used in the application: favicon and picture for the error page
  - File with a program to get the administrator password hash

- The following templates file consists of html files. The layout.html file is the main layout for the rest of the files.The syntax of the jinja language was used to build and layout HTML pages.

- The app.py file does the main job of interacting with the database GUI. And distributes routes depending on user requests. The file is written in python using the flask framework.

- The helpers.py file includes several functions that are regularly used in the app.py file:
    - function decorators
    - function of determining the name of the month
    - session detection function
    - function to define user or administrator
    - redirect function in case of incorrect input

- The worker.db file is a database carrier that stores information about:
    - users
    - passwords
    - positions
    - work shifts


### This application has two access levels - user and administrator.

#### User:

- Log in - First you need to login with your username and password

- Current shedule - This page shows the current chart. If you want to edit the current shift schedule, below there is a button that will redirect you to the appropriate page.

- My shifts - Page with information for the user of the current session. The calendar of the current month is displayed here with the days highlighted in different colors. To the right of the calendar are explanations of the colors and their number.
Below the table is general information. At the beginning of the page there is a selection menu with the names of the months that have a chart in the database and a year selection menu. After selecting the desired month, a button will appear under it. And after pressing which the necessary information will be displayed.

- Edit current shedule - The page starts with a header and a month selection menu. The default is the current month, if there is a schedule for the next month, it will be displayed in the selection menu. The shedule will be displayed depending on the selected month.
Employee names are fixed. Opposite each employee in the table there are selection menus, in the amount equal to the days in the selected month. Each of the selection menu items corresponds to a work shift:
I - inspector
I(aquamarine) - major
D - driver
D(aquamarine) - major - driver
After making changes in the chart, you need to confirm them by clicking on the button "Edit"


- Log out - Exiting the current session

#### Administrator:

- Log in - First you need to login with your username and password (Access to the administrative panel is available only to a user manually entered into the database and having a special identifier.)

- Current shedule - This page shows the current chart. If you want to edit the current shift schedule, below there is a button that will redirect you to the appropriate page.

- My shifts - Page with information for the user of the current session. The calendar of the current month is displayed here with the days highlighted in different colors. To the right of the calendar are explanations of the colors and their number.
Below the table is general information. At the beginning of the page there is a selection menu with the names of the months that have a chart in the database and a year selection menu. After selecting the desired month, a button will appear under it. And after pressing which the necessary information will be displayed.
 
- Edit current shedule - The page starts with a header and a month selection menu. The default is the current month, if there is a schedule for the next month, it will be displayed in the selection menu. The shedule will be displayed depending on the selected month.
Employee names are fixed. Opposite each employee in the table there are selection menus, in the amount equal to the days in the selected month. Each of the selection menu items corresponds to a work shift:
I - inspector
I(aquamarine) - major
D - driver
D(aquamarine) - major - driver
After making changes in the chart, you need to confirm them by clicking on the button "Edit"

- New Shedule - The page starts with a month and year selection menu. Year selection is limited to current and next only. Below is a button
"Create", confirming the choice of month and year, and redirecting to the section for creating a chart.
After pressing the button, a table appears with 12 rows, each of which has a selection menu:
in the name column, you can select any employee from the database
all other columns are the days of the month under which there are shift selection menus:
I - inspector
I(aquamarine) - major
D - driver
D(aquamarine) - major - driver
After drawing up the graph, under the table, you need to click the button "Create",
and you will be redirected to the current chart page

- Registration/Delete employee - The page is a table with a database of employees. It displays the names, positions, passwords of employees, excluding the administrator.
Below are two buttons:
-New employee - when you click on this button, a form opens in which you need to enter the name, surname, desired password and position of the new employee. After submitting this form, the new employee will appear in the database.
-Delete employee - when you click this button, a form will open where you need to enter the first and last name of the employee you want to delete from the database. If you are confident in your actions, you need to confirm this. After submitting the form, the employee's data will be deleted from the database.

- Edit shift cost -The page consists of four forms, in the header of which there is information with the name and current cost of the shift. After there is an input field and a button "Edit", when clicked, the cost will change to the one entered by the administrator.

- Bookkeeping - This page is a report for the last month about each employee, all information is obtained from the database

### The application is made to facilitate the interaction between different structures of the enterprise, such as employees, bosses and accountants.