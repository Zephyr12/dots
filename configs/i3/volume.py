import subprocess

def getVolumeBraille(vols):
    return ":"
def getVolumeSettings():
    volumePercentages = [int(100*(int(i)/65536)) for i in str(subprocess.check_output('amixer cget numid=3 | grep ": values="', shell=True)).split('=')[1][:-3].split(",")]
    vol_chara = getVolumeBraille(volumePercentages)
    print(vol_chara + "".join([str(i)+"-" for i in volumePercentages])[:-1])
    print()
    if volumePercentages[0] >= 66:
        print("#C7C799")
    elif volumePercentages[0] >= 33:
        print("#C50C99")
    elif volumePercentages[0] > 0:
        print("#FBFCFE")
    else:
        print("#FBFCFE")
getVolumeSettings()