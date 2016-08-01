import numpy as np
import ConfigUtils

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
config = ConfigUtils.ReadConfig('config.txt',
                                'data_file',
                                'output_file',
                                'latitude',
                                'avg_density',
                                'base1',
                                'base2',
                                'base_height',
                                'total_time')

main(config.options_from_config['data_file'])
