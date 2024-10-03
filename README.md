![route-optimized](https://github.com/user-attachments/assets/abf72f3b-4dc1-467a-8fbb-0f3b0cfc91ff)

# Employee Route Simulation and Payroll Calculator

This Python project simulates a group of employees visiting multiple stores, calculating driving distances, time spent in stores, and total payroll. The project uses Google Maps' API to calculate the driving distances and times between stores, and it generates reports of the employees' activity. It also visualizes the routes taken and stores visited on a map.

## Features

- **Employee Simulation**: Simulates the workday of multiple employees, logging time spent driving, time spent in stores, and distances covered.
- **Google Maps Integration**: Uses the Google Maps API to calculate driving distances and times between stores.
- **Payroll Calculation**: Calculates payroll for each employee, including labor time and mileage reimbursement.
- **Route Visualization**: Plots the routes taken by employees and stores visited on a map.
- **Customizable Parameters**: Includes adjustable settings for time spent in stores, max hours per day, and mileage reimbursement rates.

## How It Works

1. **Employee Class**: Each employee has a unique ID and attributes like time spent driving, time in store, miles driven, and payroll. The class includes methods for updating the employee's time and payroll.
   
2. **Distance and Time Calculation**: The program uses the Google Maps Distance Matrix API to calculate driving time and distance between two locations.

3. **Route Generation**: The program simulates each employee visiting a set of stores. If an employee's work time exceeds the maximum time on the clock for the day, they stop working and the next employee takes over.

4. **Payroll Calculation**: For each employee, the program calculates:
   - **Driving Time**: Time spent driving between stores.
   - **Store Time**: Time spent at each store.
   - **Mileage Payroll**: Based on the miles driven.
   - **Labor Payroll**: Based on the time spent driving and in stores.
   - **Total Payroll**: Sum of labor and mileage payroll.

5. **Report Generation**: The program generates a CSV report and a map visualizing the routes taken by employees and stores visited.

## Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- googlemaps
- random
- logging
- sys
- math

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/employee-route-simulation.git
   cd employee-route-simulation
   ```

2. Install the required libraries:
   ```bash
   pip install pandas numpy matplotlib googlemaps
   ```

3. Obtain a Google Maps API key:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Distance Matrix API.
   - Get an API key and replace the empty string `gmaps = googlemaps.Client(key='')` with your key in the code.

## Usage

1. Prepare your geocoded data (latitude, longitude, and addresses) in CSV format.
2. Run the script:
   ```bash
   python employee_route_simulation.py
   ```
3. The program will:
   - Simulate the employees' routes.
   - Generate a text report of each employee's day, saved in `output.txt`.
   - Save a CSV file `routes.csv` with detailed data about each employee's hours, miles driven, and payroll.
   - Visualize the employees' routes on a map.

## Customization

You can adjust several parameters in the script to customize the simulation:

- **min_time_in_store**: Minimum time spent at each store (default: 3600 seconds).
- **max_time_in_store**: Maximum time spent at each store (default: 5400 seconds).
- **max_time_on_clock**: Maximum working time per day for each employee (default: 28800 seconds).
- **lunch_time**: Time deducted for lunch (default: 1800 seconds).
- **max_distance_to_next_location**: Maximum distance between stores (default: 100 miles).
- **pay_rate**: The hourly pay rate (default: $25/hour).
- **mile_rate**: The reimbursement rate for miles driven (default: $0.67/mile).

## Output

### Text Report
For each employee, the program generates a report in `output.txt` with:
- Employee ID
- Hours driving and in-store
- Total time on the clock
- Miles driven
- Payroll (labor and mileage)
- Total payroll
- Number of stops and stores visited

### CSV Report
A CSV file `routes.csv` is generated with the following columns:
- `Employee ID`
- `Hours Driving`
- `Hours in Store`
- `Total Paid Hours`
- `Miles Driven`
- `Labor Payroll`
- `Miles Payroll`
- `Total Payroll`
- `Stops`
- `Stores Visited` (in JSON format)

### Route Visualization
The program also visualizes the employees' routes on a map using `matplotlib`. Each employee's route is plotted as a series of connected points, with different colors for each employee.

## Example

1. **Simulated Route**:
   - The route for each employee is visualized as a scatter plot with the stores visited.
   - The routes taken by the employees are shown as lines connecting the stores.
   
2. **Payroll Report**:
   - Each employee's driving time, in-store time, total miles, and payroll are calculated and logged in the report.

## Future Improvements

- **Add Lunch Breaks**: Automatically add a lunch break after a certain number of hours worked.
- **Dynamic Store Selection**: Improve the algorithm for selecting the next store to visit based on factors like priority or distance.

## License

This project is licensed under the MIT License.
