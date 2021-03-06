import subprocess


def getBatteryStatus():
    rawBatteryStatus = str(subprocess.check_output("acpi")).strip()
    tokens = rawBatteryStatus.split()
    if(len(tokens) > 5):  # Not Full
        chargestate = tokens[2][:-1]
        perc = tokens[3][:-1]
        percInt = int(perc[:-1])
        if (chargestate[0] == "C"):
            print(""+perc)
            print("")
            print("#A2B28E")
        if(percInt > 90):
            print(" " + perc)
            print("")
            print("#A2B28E")
        if(percInt > 75):
            print("" + perc)
            print("")
            print("#A2B28E")  # green
        elif(percInt > 50):
            print("" + perc)
            print("")
            print("#B2B28E")  # yellow
        elif(percInt > 25):
            print("" + perc)
            print("")
            print("#B2B28E")  # yellow
        else:
            print(""+perc)
            print("")
            print("#662828")  # yellow

    else:  # Full
        print(" full")
        print("")
        print("#A2B28E")

try:
    getBatteryStatus()
except:
    print("")
    print("")
    print("#A2B28E")