# Klein Glotzi

Simple Arduino based two axis camera gimbal for fitting a Microsoft LifeCam.

# Arduino sketch

You have to try out the calibration settings for the servos you're using, just modify the min and max settings in the sketch.

## Panning with the control box

There's a control-box attached to the arduino with just two potentiometers for controlling each of the axes.

## Panning via serial port

You can use the serial port in 9600,8,N,1 mode to send a string of two comma separated integers to control the panning via software.

Just send something like this: `512,512\n` to center the camera, minimum value is zero, maximum is 1023.

Sending a positioning coordinate disables the control box. Send a `-1` for the axis you want to re-enable

# Printing the STLs

You can use the `All_Parts_Plate.stl` file to print all parts at once or just print all things one by one.

The base box has no bottom and no lid as printing such big monotonous forms will most likely deform while printing. Just use a sheet of acrylic or some aluminium to make the top and bottom plates.

If you want to modify the parts to fit your needs get an OnShape Account, the Link to the project is following:

https://cad.onshape.com/documents/6b43bf9158c2330bf8f3274f/w/bf932df38055a7275eddfee5/e/89a3396a8a0f5c6514141639

# Python GUI

There is a simple python GUI to control Klein Glotzi from a Linux computer. You'll need GTK 3, the python gi and serial modules.
Install them from your distro repos or create a virtualenv and install the requirements:

```bash
cd glotzi
pyvenv ~/.virtualenvs/glotzi
. ~/.virtualenvs/glotzi/bin/activate
cd pygui
python main.py
```

Just run `main.py` and a window should show up. When selecting a serial port the GUI immediately takes over control and centers the camera. If you close the window control is returned to the control-box.

# TODO

- Make all parts available on OnShape