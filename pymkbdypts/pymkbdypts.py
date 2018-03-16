from numpy import *
import pylab as pl
import netCDF4
import argparse
import logging
import sys
# Get the version
from pkg_resources import Requirement, resource_filename


def main():
    filename = resource_filename(Requirement.parse('pymkbdypts'),'pymkbdypts/VERSION')
    with open(filename) as version_file:
            version = version_file.read().strip()

    bdy_help = 'Boundary info file, this is typically called bdyinfo.dat'
    topo_help = 'Topography (bathymetry) file, this is typically called topo.nc'
    output_help = 'Name of the output file'
    format_help = 'Output format, valid values are "points" [default], "numbdy": Saves the locations and the boundary number, "tides" and "conv"'
    figure_help = 'Saving a figure of the boundaries, e.g. --figure map.png, or -fig map.pdf (pdf format may take long and can be inefficient as it has to save a pcolor matrix)'

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    logger = logging.getLogger('pymkbdypts:')


    logger.info('This is pymkbdypts (Version: ' + str(version) + ')')  

    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count')

    parser.add_argument('--bdyinfo', '-b', nargs = 1, default = None, help=bdy_help)
    parser.add_argument('--topo', '-t', nargs = 1, default = None, help=topo_help)
    parser.add_argument('--output', '-o', nargs = 1, default = None, help=output_help)
    parser.add_argument('--format', '-f', nargs = 1, default = None, help=format_help)
    parser.add_argument('--figure', '-fig', nargs = '*', default = None, help=figure_help)
    args = parser.parse_args()

    plot_map = True
    #
    # Set logging level
    #

    if(args.verbose == None):
        #logger.info('logging level: CRITICAL')
        #logging_level = logging.CRITICAL
        logger.info('logging level: DEBUG ')    
        logging_level = logging.DEBUG    
    elif(args.verbose == 1):
        logger.info('logging level: INFO ')        
        logging_level = logging.INFO
    elif(args.verbose >= 2):
        logger.info('logging level: DEBUG ')
        logging_level = logging.DEBUG
    else:
        logger.info('logging level: DEBUG ')    
        logging_level = logging.DEBUG

    logger.setLevel(logging_level)

    #
    # Read boundary info
    #

    if(args.bdyinfo == None):
        # No file given, try to find a bdyinfo.dat in current directory
        logger.info('No boundary file defined, trying to find one in current directory.')
        bdy_file = './bdyinfo.dat'
    else:
        logger.info('Will open boundary file:' + args.bdyinfo[0])
        bdy_file = args.bdyinfo[0]


    try:
        bdyf = open(bdy_file)
        logger.info('Opened file:' + bdy_file)
    except:
        logger.critical('Could not open file:' + bdy_file)
        logger.critical('Aborting ...')
        exit()


    #
    # Read topo file
    #

    if(args.topo == None):
        # No file given, try to find a topo.nc in current directory
        logger.info('No topo file defined, trying to find one in current directory.')
        topo_file = './topo.nc'

    else:
        logger.info('Will open topography file:' + args.topo[0])
        topo_file = args.topo[0]


    try:
        topo_nc = netCDF4.Dataset(topo_file)
        logger.info('Opened file:' + topo_file)
    except:
        logger.critical('Could not open file:' + topo_file)
        logger.critical('Aborting ...')
        exit()


    if(args.output == None):
        # No file given, try to find a bdyinfo.dat in current directory
        logger.critical('No output file defined')
        result_file = None
    else:
        logger.info('Will use result file:' + str(args.output[0]))
        result_file = args.output[0]
        if(args.format == None):
            file_format = 'points'
        elif(args.format[0] == 'tides'):
            file_format = 'tides' #
        elif(args.format[0] == 'numbdy'):
            file_format = 'numbdy' #        
        elif(args.format[0] == 'conv'):
            file_format = 'conv'  #

        logger.info('File format:' + file_format)


    # Check if we want to plot
    # None: No plotting
    # Empty: standard file
    # otherwise filename 
    if(args.figure == None):
        plot_map = False
    else:
        if(len(args.figure) == 0):
            figname='./pymkbdypts.png'
        else:
            figname = args.figure[0]



    #bdy_file = '/home/holterma/tools/mossco/setups/sns/bdyinfo.dat'
    #topo_file = '/home/holterma/tools/mossco/setups/sns/topo.nc'
    #result_file = '/home/holterma/tools/mossco/setups/sns_peter/bdy_pts_tide.txt'



    grid_type = int(topo_nc.variables['grid_type'][:])

    logger.info('Grid_type: ' + str(grid_type))

    #
    # 
    #
    if(grid_type == 4):
        logger.info('Spherical curvilinear grid type')
        LAT  = topo_nc.variables['latx']
        LON  = topo_nc.variables['lonx']
        conv = topo_nc.variables['convx']
        b_pl = topo_nc.variables['bathymetry']
        X_pl = LON
        Y_pl = LAT    
    elif(grid_type == 3):
        logger.info('Curvilinear grid type')
        try:
            LAT  = topo_nc.variables['latx']
        except:
            logger.debug('no lat defined, using yx')
            LAT  = topo_nc.variables['yx']

        try:
            LON  = topo_nc.variables['lonx']
        except:
            logger.debug('no lon defined, using xx')        
            LON  = topo_nc.variables['xx']

        conv = topo_nc.variables['convx']
        b_pl = topo_nc.variables['bathymetry']    
        X_pl = topo_nc.variables['xx']
        Y_pl = topo_nc.variables['yx']
    elif(grid_type == 2):
        logger.info('Spherical grid type')
        lat  = topo_nc.variables['lat']
        lon  = topo_nc.variables['lon']
        LON,LAT = meshgrid(lon,lat)
        b_pl = topo_nc.variables['bathymetry']    
        X_pl = LON
        Y_pl = LAT
    elif(grid_type == 1):
        logger.info('Cartesian grid type')
        lon  = topo_nc.variables['x']
        lat  = topo_nc.variables['y']
        LON,LAT = meshgrid(lon,lat)
        b_pl = topo_nc.variables['bathymetry']    
        X_pl = LON
        Y_pl = LAT





    #
    BDY_DIR = 0 # 0: west, 1: north, 2: east, 3: south
    STR_BDY_DIR = ['west', 'north', 'east', 'south']
    ind_bdy_points = []
    num_bdy_points = []
    num_bdy = 0

    while(True):
        line = bdyf.readline()
        #print(line)
        if(len(line) > 0):
            if((line[0] == '#') or (line[0] == '!')): # comment
                pass
            else:
                try:
                    NUM_OPEN_BDY = int(line)
                except:
                    NUM_OPEN_BDY = None

                if(NUM_OPEN_BDY != None):
                    FLAG_BDY = False
                    logger.debug('Will read ' + str(NUM_OPEN_BDY) + ' for ' + STR_BDY_DIR[BDY_DIR])
                    for i in range(NUM_OPEN_BDY):
                        line = bdyf.readline()
                        logger.debug(line)
                        lsplit = line.split(' ')
                        logger.debug(lsplit)
                        num_bdy += 1 # Count the number of boundaries
                        if((BDY_DIR == 0) or (BDY_DIR == 2)): # west or east bdy
                            ind_x = int(lsplit[0])
                            ind_y1 = int(lsplit[1])
                            ind_y2 = int(lsplit[2])
                            for j in range(ind_y1,ind_y2+1):
                                ind_bdy_points.append((ind_x,j))
                                num_bdy_points.append(num_bdy)


                        else:
                            ind_y = int(lsplit[0])
                            ind_x1 = int(lsplit[1])
                            ind_x2 = int(lsplit[2])
                            for j in range(ind_x1,ind_x2+1):
                                ind_bdy_points.append((j,ind_y))
                                num_bdy_points.append(num_bdy)

                    BDY_DIR += 1



        else:
            break


    #print(ind_bdy_points)
    #print(len(ind_bdy_points))


    #
    # Get lat lon for the indices
    #

    lonbdy = []
    latbdy = []
    x_bdy_pl = []
    y_bdy_pl = []

    if((grid_type == 3) or (grid_type == 4)):
        convbdy = []

    for i,p in enumerate(ind_bdy_points):
        ind_x = p[0] - 1
        ind_y = p[1] - 1
        # Average over the 4 points of the T-cell
        if((grid_type == 3) or (grid_type == 4)):
            lontmp = LON[ind_y:ind_y+2,ind_x:ind_x+2].mean()
            lattmp = LAT[ind_y:ind_y+2,ind_x:ind_x+2].mean()

            lonbdy.append(lontmp)
            latbdy.append(lattmp)

            convtmp = conv[ind_y:ind_y+2,ind_x:ind_x+2].mean()
            convbdy.append(convtmp)

            xtmp = X_pl[ind_y:ind_y+2,ind_x:ind_x+2].mean()
            ytmp = Y_pl[ind_y:ind_y+2,ind_x:ind_x+2].mean()

            x_bdy_pl.append(xtmp)
            y_bdy_pl.append(ytmp)                
        else:
            lonbdy.append(LON[ind_y,ind_x])
            latbdy.append(LAT[ind_y,ind_x])
            x_bdy_pl.append(LON[ind_y,ind_x])
            y_bdy_pl.append(LAT[ind_y,ind_x])



    #
    # Write the data to a file
    #

    if(result_file != None):
        f = open(result_file,'w')

        if(file_format == 'tides'):
            f.write(str(len(lonbdy)) + '\n')

        for i,p in enumerate(lonbdy):
            if(file_format == 'tides'):
                pstr = str(latbdy[i]) + ' ' + str(lonbdy[i]) + '\n'
            elif(file_format == 'conv'):
                pstr = str(i) + ' ' + str(latbdy[i]) + ' ' + str(lonbdy[i]) + ' ' + str(convbdy[i]) + '\n'
            elif(file_format == 'numbdy'):
                pstr = str(lonbdy[i]) + ' ' + str(latbdy[i]) + ' ' + str(num_bdy_points[i]) + '\n'
            else:
                pstr = str(lonbdy[i]) + ' ' + str(latbdy[i]) + '\n'

            f.write(pstr)


        f.close()

    # Lets plot the map with the boundaries
    if(plot_map):
        logger.info('Plotting figure')
        pl.figure(1)
        pl.clf()

        pl.pcolormesh(X_pl,Y_pl,b_pl,cmap=pl.cm.viridis_r)
        col = pl.colorbar()
        col.set_label(b_pl.units)
        pl.plot(x_bdy_pl,y_bdy_pl,'or')
        logger.info('Saving map into figure: ' + figname)
        pl.savefig(figname)

        pl.draw()
        pl.show()
    
    



