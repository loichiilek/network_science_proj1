To install:

    pip install -r requirements.txt

To use PyQt5, the system requires Tkinter. Some systems come pre-installed with it, and there are different steps to install it for Windows or Linux. An easy way is to set up a condas virtual env, which comes preinstalled with Tkinter.

After the packages have been installed, run: 

    python project.py

The program dynamically generates and stores intermediate results as csv files, json files, or png in the same folder. These files can be ignored by the user.

When the program is processing, sometimes the GUI shows Not Responding on Windows. This is normal for the PyQt interface. Please do not close the program but allow it to run to completion. The fetching of the DBLP API takes approximately 2 minutes. Also, question analysis may take up to 5 mins to run.
