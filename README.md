
Skills: Programming with Advanced Computer Languages

# Climbing Tracker
This is a Python-based project that climbers can use to track their climbing history and evaluate their development. It uses the json, tkinter and statistics libraries.

 ## Project Structure
The project has the following file structure:

```
climbing-tracker
├── climbing_data.json
├── user_details.json
├── climbing_tracker.py
requirements.txt
README.md
```
- `climbing_data.json`: This file includes all the saved climbing routes, difficulty levels, number of attempts and completed(yes/no) provided via user input
- `user_details.json`: This file includes the user information name, age and level
- `climbing_tracker`: This file is the main script for the project. It interacts with the user via an interface in which the user can insert information on the climbing routes. It also evaluates the user input and provides statistics on the climbing development of the user.
- `README.md`: This file contains the documentation for the project.
- `requirements.txt`: This file lists the required Python packages for the project, including json, tkinter, statistics, pandas, matplotlib

## Usage
To use the climbing tracker, run the `climbing_tracker.py` script. The script asks the user to login then input their climbing routes and allows them to visualise and track their climbing progress.

## Requirements
To install the required packages, run pip install -r `requirements.txt`.
