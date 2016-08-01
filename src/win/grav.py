import numpy as np

def deg2rad(deg):
    return ((deg * np.pi) / 180)


def contains(character, string):
    equals = 0
    for char in string:
        if char == character:
            equals += 1
    if equals == 0:
        return False
    else:
        return True

def raiseGeneralError(arg):
    with open('err.log', "a") as errlog:
        errlog.write("Error: %s\n" % arg)
    exit(arg)

def readHeader(file_name):
    with open(file_name, 'r') as f:
        return f.readline().rstrip()


class ReadConfig(object):
    ### Initialize Variables ###
    latitude            = -1
    relative_height     = -1
    avg_density         = -1
    data_file           = ''
    base1               = -1
    base2               = -1
    total_time          = -1
    base_height         = -1

    options_from_config = [
            'latitude',     # 0
            'avg_density',  # 1
            'data_file',    # 2
            'base1',        # 3
            'base2',        # 4
            'total_time',   # 5
            'base_height',  # 6
        ]

    def __init__(self, file_name):

        self.file_name = file_name

        # open file and read contents to store in variables
        with open(file_name) as f:
            content = f.readlines()
        line_num = 1
        for line in content:
            if not line.startswith('#') and not line.isspace():
                if not contains("=", line):
                    raiseGeneralError("Could not find an '=' %d: %s" %  (line_num, line))


                variable = line.split()[0]
                equal    = line.split()[1]
                value    = line.split()[2]
                if len(line.split()) > 3:
                    raiseGeneralError("Wrong Syntax on line, %s: %s" % (line_num, line))
                if equal != '=':
                    exit("This shouldn't appear.Ever.")
                if not variable in str(self.options_from_config):
                    raiseGeneralError("Couldn't find %s in options_from_config list" % variable)
                else:
                    #print variable, equal, value
                    if variable == self.options_from_config[0]:
                        self.latitude = value
                    elif variable == self.options_from_config[1]:
                        self.avg_density = float(value)
                    elif variable == self.options_from_config[2]:
                        self.data_file = value
                    elif variable == self.options_from_config[3]:
                        self.base1 = float(value)
                    elif variable == self.options_from_config[4]:
                        self.base2 = float(value)
                    elif variable == self.options_from_config[5]:
                        self.total_time = float(value)
                    elif variable == self.options_from_config[6]:
                        self.base_height = float(value)
                    else:
                        raiseGeneralError("Variable not found in options from config file: %s" % variable)
            line_num += 1


def main(data_f):
    if data_f == '':
        exit("data_f is blank - report bug.")
    try:
        print '-> Loading %s' % data_f
        data = np.loadtxt(data_f)
    except IOError:
        exit("Data file couldn't")

    y     = data[:,0]
    x     = data[:,1]

    print '-> Extracting Raw Gravity Data.'
    raw_g = data[:,2]

    print '-> Extracting Time Elapsed Data.'
    time = data[:,3]

    print '-> Extracting Relevent Height Data'
    rel_h = data[:,4]
    lat = deg2rad(float(config.latitude))
    ### Do calculations

    # observed g
    g_o = raw_g - (((time * (config.base2 - config.base1)) / config.total_time) + config.base1)

    # Latitude Correction
    g_l = (0.000812 * np.sin(lat *2)) * y

    #Free Air Correction
    g_fa = 0.3086 * (rel_h - config.base_height)

    # Bouguer Correction
    g_b = (0.0000419 * (rel_h - config.base_height) * config.avg_density)

    final = g_o - g_l + g_fa - g_b

    ###
    print "-> Attaching All Data."
    final = np.stack((x, y, raw_g, time, rel_h, final), axis=-1)

    print "-> Saving Corrected Grav Data to: grav_corr.txt"
    np.savetxt('grav_corr.txt', final, newline='\n', fmt='%.6f', header="x\t\t\ty\t\traw_g\t\ttime\t\trel_h\t\tGB")


print "-> Reading Configuration File."
config = ReadConfig('config.txt')
main(config.data_file)
