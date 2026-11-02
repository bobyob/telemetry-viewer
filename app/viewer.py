import pandas as pd
import pyqtgraph as pg

#Load the CSV file into a pandas DataFrame
CSV_PATH = "sample_data/fake_run.csv" #data location

df = pd.read_csv(CSV_PATH) #opens the file and turns it into a dataframe
t_s = (df["t_ms"] / 1000).to_numpy()

#Build list of column names to plot
COLUMNS = []
for name in df.columns:
    if name != "t_ms":
        COLUMNS.append(name)


#Create a plot for each column in the DataFrame
app = pg.mkQApp("Telemetry Viewer")

win = pg.GraphicsLayoutWidget(title="Telemetry Viewer")
win.resize(1000, 600)

first_plot = None

for row, name in enumerate(COLUMNS):
    plot = win.addPlot(row=row, col=0, title=name)
    plot.setLabel("bottom", "Time", units="s")
    plot.showGrid(x=True, y=True)
    plot.plot(t_s, df[name].to_numpy(), pen=pg.mkPen(width=2))

    if first_plot is None:
        first_plot = plot
    else:
        plot.setXLink(first_plot)

win.show()
pg.exec()