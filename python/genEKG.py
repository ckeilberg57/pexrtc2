import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Prompt for initial values
initial_hr_value = float(input("Enter initial heart rate value (bpm): "))
initial_o2_value = float(input("Enter initial oxygen saturation value (%%): "))
initial_systolic_value = float(input("Enter initial systolic blood pressure value (mmHg): "))
initial_diastolic_value = float(input("Enter initial diastolic blood pressure value (mmHg): "))

# Define parameters
start_x = 70
end_x = 200
update_interval = 50  # Time between updates in milliseconds
update_interval_sec = update_interval / 1000  # Convert milliseconds to seconds
update_cycle_hr = 5  # Update HR value every 5 seconds
update_cycle_o2 = 10  # Update O2 value every 10 seconds
update_cycle_bp = 60  # Update BP value every 1 minute (60 seconds)
fluctuation_range_hr = 15  # Maximum fluctuation range for HR
fluctuation_range_o2 = 3   # Maximum fluctuation range for O2 (±3)
fluctuation_range_bp = 10  # Maximum fluctuation range for BP (±10)

# Initialize HR, O2, and BP data
def initialize_data():
    return np.full_like(t, initial_hr_value), np.full_like(t, initial_o2_value), np.full_like(t, initial_systolic_value), np.full_like(t, initial_diastolic_value)

# Function to update the HR value
def update_hr_value():
    global current_hr_value
    fluctuation = np.random.uniform(-fluctuation_range_hr, fluctuation_range_hr)
    current_hr_value += fluctuation
    current_hr_value = max(min(current_hr_value, initial_hr_value + fluctuation_range_hr), initial_hr_value - fluctuation_range_hr)
    return current_hr_value

# Function to update the O2 value
def update_o2_value():
    global current_o2_value
    fluctuation = np.random.uniform(-fluctuation_range_o2, fluctuation_range_o2)
    current_o2_value += fluctuation
    current_o2_value = max(min(current_o2_value, 100), 0)  # Ensure O2 level does not exceed 100%
    return current_o2_value

# Function to update the BP values
def update_bp_values():
    global current_systolic_value, current_diastolic_value
    systolic_fluctuation = np.random.uniform(-fluctuation_range_bp, fluctuation_range_bp)
    diastolic_fluctuation = np.random.uniform(-fluctuation_range_bp, fluctuation_range_bp)
    current_systolic_value += systolic_fluctuation
    current_diastolic_value += diastolic_fluctuation
    # Ensure values are within a reasonable range
    current_systolic_value = max(min(current_systolic_value, initial_systolic_value + fluctuation_range_bp), initial_systolic_value - fluctuation_range_bp)
    current_diastolic_value = max(min(current_diastolic_value, initial_diastolic_value + fluctuation_range_bp), initial_diastolic_value - fluctuation_range_bp)
    return current_systolic_value, current_diastolic_value

# Update function for animation
def update(frame):
    global last_update_time_hr, last_update_time_o2, last_update_time_bp
    global current_hr_value, highest_value, lowest_value
    global current_o2_value, highest_o2_value, lowest_o2_value
    global current_systolic_value, current_diastolic_value
    global highest_systolic_value, lowest_systolic_value
    global highest_diastolic_value, lowest_diastolic_value

    current_time = frame * update_interval_sec

    # Update HR value every 5 seconds
    if current_time - last_update_time_hr >= update_cycle_hr:
        last_update_time_hr = current_time
        current_hr_value = update_hr_value()  # Update HR value

        # Update highest and lowest HR values
        if current_hr_value > highest_value:
            highest_value = current_hr_value
        if current_hr_value < lowest_value:
            lowest_value = current_hr_value

    # Update O2 value every 10 seconds
    if current_time - last_update_time_o2 >= update_cycle_o2:
        last_update_time_o2 = current_time
        current_o2_value = update_o2_value()  # Update O2 value

        # Update highest and lowest O2 values
        if current_o2_value > highest_o2_value:
            highest_o2_value = current_o2_value
        if current_o2_value < lowest_o2_value:
            lowest_o2_value = current_o2_value

    # Update BP values every 1 minute
    if current_time - last_update_time_bp >= update_cycle_bp:
        last_update_time_bp = current_time
        current_systolic_value, current_diastolic_value = update_bp_values()  # Update BP values

        # Update highest and lowest BP values
        if current_systolic_value > highest_systolic_value:
            highest_systolic_value = current_systolic_value
        if current_systolic_value < lowest_systolic_value:
            lowest_systolic_value = current_systolic_value
        if current_diastolic_value > highest_diastolic_value:
            highest_diastolic_value = current_diastolic_value
        if current_diastolic_value < lowest_diastolic_value:
            lowest_diastolic_value = current_diastolic_value

    # Generate the HR line data
    x_data = np.linspace(start_x, end_x, len(hr_line_data))
    hr_line_data[:-1] = hr_line_data[1:]  # Shift data to the left
    hr_line_data[-1] = current_hr_value  # Set new value at the end

    # Generate the O2 line data
    o2_line_data[:-1] = o2_line_data[1:]  # Shift data to the left
    o2_line_data[-1] = current_o2_value  # Set new value at the end

    # Generate the BP line data
    systolic_line_data[:-1] = systolic_line_data[1:]  # Shift data to the left
    systolic_line_data[-1] = current_systolic_value  # Set new value at the end

    diastolic_line_data[:-1] = diastolic_line_data[1:]  # Shift data to the left
    diastolic_line_data[-1] = current_diastolic_value  # Set new value at the end

    # Update line data
    line_hr.set_xdata(x_data)
    line_hr.set_ydata(hr_line_data)
    
    line_o2.set_xdata(x_data)
    line_o2.set_ydata(o2_line_data)
    
    line_systolic.set_xdata(x_data)
    line_systolic.set_ydata(systolic_line_data)
    
    line_diastolic.set_xdata(x_data)
    line_diastolic.set_ydata(diastolic_line_data)

    # Update text annotations with real-time values
    text_hr_current.set_text(f'Current HR: {int(current_hr_value)} bpm')
    text_hr_max.set_text(f'Max HR: {int(highest_value)} bpm')
    text_hr_min.set_text(f'Min HR: {int(lowest_value)} bpm')
    
    text_o2_current.set_text(f'Current O2: {int(current_o2_value)} %')
    text_o2_max.set_text(f'Max O2: {int(highest_o2_value)} %')
    text_o2_min.set_text(f'Min O2: {int(lowest_o2_value)} %')

    text_systolic_current.set_text(f'Current Systolic BP: {int(current_systolic_value)} mmHg')
    text_systolic_max.set_text(f'Max Systolic BP: {int(highest_systolic_value)} mmHg')
    text_systolic_min.set_text(f'Min Systolic BP: {int(lowest_systolic_value)} mmHg')

    text_diastolic_current.set_text(f'Current Diastolic BP: {int(current_diastolic_value)} mmHg')
    text_diastolic_max.set_text(f'Max Diastolic BP: {int(highest_diastolic_value)} mmHg')
    text_diastolic_min.set_text(f'Min Diastolic BP: {int(lowest_diastolic_value)} mmHg')

    return line_hr, line_o2, line_systolic, line_diastolic, text_hr_current, text_hr_max, text_hr_min, text_o2_current, text_o2_max, text_o2_min, text_systolic_current, text_systolic_max, text_systolic_min, text_diastolic_current, text_diastolic_max, text_diastolic_min

# Set up the figure and axes
fig, (ax_hr, ax_o2, ax_bp) = plt.subplots(3, 1, figsize=(14, 12))  # Increase figure width for space
plt.subplots_adjust(hspace=0.5, right=0.8)  # Adjust spacing and figure layout

# Set background color for axes
ax_hr.set_facecolor('black')
ax_o2.set_facecolor('black')
ax_bp.set_facecolor('black')

# Set background color for figure
fig.patch.set_facecolor('#0a2136')

# Grid lines
ax_hr.grid(True, color='gray')
ax_o2.grid(True, color='gray')
ax_bp.grid(True, color='gray')

# Set color for axis labels, titles, and ticks
ax_hr.xaxis.label.set_color('white')
ax_hr.yaxis.label.set_color('white')
ax_o2.xaxis.label.set_color('white')
ax_o2.yaxis.label.set_color('white')
ax_bp.xaxis.label.set_color('white')
ax_bp.yaxis.label.set_color('white')

ax_hr.tick_params(axis='both', colors='white')
ax_o2.tick_params(axis='both', colors='white')
ax_bp.tick_params(axis='both', colors='white')

# Initialize data arrays
t = np.linspace(start_x, end_x, int((end_x - start_x) / update_interval_sec))
hr_line_data, o2_line_data, systolic_line_data, diastolic_line_data = initialize_data()

# Plot lines
line_hr, = ax_hr.plot(t, hr_line_data, color='cyan', label='Heart Rate (HR)')
line_o2, = ax_o2.plot(t, o2_line_data, color='green', label='Oxygen Saturation (O2)')
line_systolic, = ax_bp.plot(t, systolic_line_data, color='red', label='Systolic BP')
line_diastolic, = ax_bp.plot(t, diastolic_line_data, color='blue', label='Diastolic BP')

# Set axis labels and titles
ax_hr.set_xlabel('Time (s)', color='white')
ax_hr.set_ylabel('HR (bpm)', color='white')
ax_hr.set_title('Heart Rate (HR) Over Time', color='white')
ax_hr.set_ylim(40, 200)  # Set y-axis limits for HR

ax_o2.set_xlabel('Time (s)', color='white')
ax_o2.set_ylabel('Oxygen Saturation (%)', color='white')
ax_o2.set_title('Oxygen Saturation (O2) Over Time', color='white')
ax_o2.set_ylim(80, 100)  # Set y-axis limits for O2

ax_bp.set_xlabel('Time (s)', color='white')
ax_bp.set_ylabel('Blood Pressure (mmHg)', color='white')
ax_bp.set_title('Blood Pressure (BP) Over Time', color='white')
ax_bp.set_ylim(50, 180)  # Set y-axis limits for Blood Pressure

# Add text annotations for HR (outside the graph on the right)
text_hr_current = ax_hr.text(1.05, 0.95, '', transform=ax_hr.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_hr_max = ax_hr.text(1.05, 0.85, '', transform=ax_hr.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_hr_min = ax_hr.text(1.05, 0.75, '', transform=ax_hr.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')

# Add text annotations for O2 (outside the graph on the right)
text_o2_current = ax_o2.text(1.05, 0.95, '', transform=ax_o2.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_o2_max = ax_o2.text(1.05, 0.85, '', transform=ax_o2.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_o2_min = ax_o2.text(1.05, 0.75, '', transform=ax_o2.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')

# Add text annotations for Systolic BP (outside the graph on the right)
text_systolic_current = ax_bp.text(1.05, 0.95, '', transform=ax_bp.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_systolic_max = ax_bp.text(1.05, 0.85, '', transform=ax_bp.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_systolic_min = ax_bp.text(1.05, 0.75, '', transform=ax_bp.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')

# Add text annotations for Diastolic BP (outside the graph on the right)
text_diastolic_current = ax_bp.text(1.05, 0.65, '', transform=ax_bp.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_diastolic_max = ax_bp.text(1.05, 0.55, '', transform=ax_bp.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')
text_diastolic_min = ax_bp.text(1.05, 0.45, '', transform=ax_bp.transAxes, color='white', fontsize=10, verticalalignment='top', horizontalalignment='left')

# Initialize update times
last_update_time_hr = 0
last_update_time_o2 = 0
last_update_time_bp = 0

# Initialize current values
current_hr_value = initial_hr_value
highest_value = initial_hr_value
lowest_value = initial_hr_value

current_o2_value = initial_o2_value
highest_o2_value = initial_o2_value
lowest_o2_value = initial_o2_value

current_systolic_value = initial_systolic_value
current_diastolic_value = initial_diastolic_value
highest_systolic_value = initial_systolic_value
lowest_systolic_value = initial_systolic_value
highest_diastolic_value = initial_diastolic_value
lowest_diastolic_value = initial_diastolic_value

# Set up animation
ani = animation.FuncAnimation(fig, update, frames=int(end_x / update_interval_sec), interval=update_interval, blit=True)

plt.show()
