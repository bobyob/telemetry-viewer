## Goal

Build a PC app that shows live car telemetry as graphs, saves all of the data, and let's anyone open and plot logged data easily without needing someone who knows the scripts. Built a Python live dashboard that parses and validates comma-separated sensor data, rejects corrupted lines, and plots 4 channels in real time.

**Problems with current setup**
- No live viewing, existing code prints individual strings instead of full data lines
- Data disappears when the laptop disconnects
- Graphs aren't saved
- Manual data retrieval -> pulling off SD card out of the car
- Logged data is in a messy CSV, someone has to extract and plot it by hand.

**Solutions**
- Live viewer
	- GUI with real-time graphs, one plot per variable, and looks good to show judges
- Saved data: all received data is written to a CSV as it arrives
- Playback: open any saved CSV or an SD log and plot it immediately
- SD access without removing the card
- Two data paths
	- Wireless during the run
	- USB cable after the run as backup
- Intuitive -> anyone on the team can run it without knowing the code

Currently implementing auto-saving data with timestamped CSV

Sample Live Plot
<img width="990" height="921" alt="image" src="https://github.com/user-attachments/assets/c38db80b-4494-4a20-be84-d626415b2042" />
