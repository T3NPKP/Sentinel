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
    info = product_info(str_lists[1], cood, time)
    print(f'coordinate is {info.coordinates}')
    print(f'name is {info.name}')
    print(f'time is {info.time}')
    return info
