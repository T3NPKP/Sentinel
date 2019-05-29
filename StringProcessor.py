class product_info:
    def __init__(self, name, coordinates, time):
        self.name = name
        self.coordinates = coordinates
        self.time = time


def divide_string(original):
    str_lists = str.split(original)
    cood = str_lists[70:77]
    cood[0] = cood[0][17:]
    cood[6] = cood[6][0:-20]
    time = ""
    for i in range(29, 36):
        time += str_lists[i]
    time = time[18: -2]
    info = product_info(str_lists[1], cood, time)
    tmp = len(info.name) - 2
    info.name = info.name[1: tmp]
    return info
