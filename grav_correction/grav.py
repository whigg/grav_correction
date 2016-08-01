import numpy as np

class ReadConfig(object):

    def __init__(self, file_name, *args):
        self.options_from_config = []
        self.variable = []
        self.value = []

        for num in args:
            self.options_from_config.append(num)
        self.file_name = file_name

        # open file and read contents to store in variables
        with open(file_name) as f:
            content = f.readlines()
        line_num = 1
        for line in content:
            if not line.startswith('#') and not line.isspace():
                if not self.contains("=", line):
                    self.raiseGeneralError("Could not find an '=' %d: %s" %  (line_num, line))


                self.variable.append(line.split()[0])
                equal    = line.split()[1]
                self.value.append(line.split()[2])

                if len(line.split()) > 3:
                    self.raiseGeneralError("Wrong Syntax on line, %s: %s" % (line_num, line))
                if equal != '=':
                    raise StandardError("Could not find '=' on line %s : %s" % (line_num, line))


            line_num += 1
        for val in self.variable:
            if val not in self.options_from_config:
                raise StandardError("Could not find '%s' in config file" % val)

        self.options_from_config = dict(zip(self.variable, self.value))

    def contains(self, character, string):
        equals = 0
        for char in string:
            if char == character:
                equals += 1
        if equals == 0:
            return False
        else:
            return True

    def raiseGeneralError(self, *args):
        exit(*args)

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

def readHeader(file_name):
    with open(file_name, 'r') as f:
        return f.readline().rstrip()


def main(data_f):
    if data_f == '':
        exit("data_f is blank - report bug.")
    try:
        print '-> Loading %s' % data_f
        data = np.loadtxt(data_f)
    except IOError:
        exit("Data file couldn't")

    options = config.options_from_config
    base2 = float(options['base2'])
    base1 = float(options['base1'])
    total_time = float(options['total_time'])
    lat = float(options['latitude'])
    avg_density = float(options['avg_density'])
    base_height = float(options['base_height'])
    output_file = str(options['output_file'])

    y     = data[:,0]
    x     = data[:,1]

    print '-> Extracting Raw Gravity Data.'
    raw_g = data[:,2]

    print '-> Extracting Time Elapsed Data.'
    time = data[:,3]

    print '-> Extracting Relevant Height Data'
    rel_h = data[:,4]
    lat = deg2rad(lat)
    ### Do calculations

    # observed g
    #g_o = raw_g - (((time * (config.base2 - config.base1)) / config.total_time) + config.base1)
    g_o = raw_g - (((time * (base2 - base1)) / total_time) + base1)

    # Latitude Correction
    g_l = (0.000812 * np.sin(lat *2)) * y

    #Free Air Correction
    #g_fa = 0.3086 * (rel_h - config.base_height)
    g_fa = 0.3086 * (rel_h - base_height)

    # Bouguer Correction
    g_b = (0.0000419 * (rel_h - base_height *avg_density))

    final = g_o - g_l + g_fa - g_b

    ###
    print "-> Attaching All Data."
    final = np.stack((x, y, raw_g, time, rel_h, final), axis=-1)

    print "-> Saving Corrected Grav Data to: %s" % output_file
    np.savetxt(output_file, final, newline='\n', fmt='%.6f', header="x\t\t\ty\t\traw_g\t\ttime\t\trel_h\t\tGB")


print "-> Reading Configuration File."
config = ReadConfig('config.txt',
                    'data_file',
                    'output_file',
                    'latitude',
                    'avg_density',
                    'base1',
                    'base2',
                    'base_height',
                    'total_time')

main(config.options_from_config['data_file'])
