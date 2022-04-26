import subprocess
import os
from datetime import datetime

import numpy as np
import pandas as pd


class LibRadPy:
    # default constructor
    def __init__(self, path):
        self.path = path

    def setup(self):
        os.chdir(self.path)
        result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
        if result.stderr is "":
            ls_list = result.stdout.split('\n')
            ls_list = [line.split(' ')[-1] for line in ls_list]
            # for ii in range(1,len(ls_list)) #second index by purpose
        if 'auto_io_files' not in ls_list:
            os.mkdir('auto_io_files')

    def example_mie_uvspec(self):
        wavelength = 350
        sza = 48
        umu = [-1, -0.5, -0.1]
        phi = [0, 30, 60, 90]
        r_eff = 1
        wavelength_vec = [345, 355]
        wavelength_res = 0.1
        self.generate_mie_input(r_eff, wavelength_vec, wavelength_res)
        self.generate_uvspec_mie_input(wavelength, sza, umu, phi)

    def generate_mie_input(self, r_eff, wavelength, wavelength_res, dist_gamma=7, n_stokes=4, n_lagandre=129):
        os.chdir(self.path + '/auto_io_files')
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('MIE_AUTO.INP', 'w') as f:
            f.write('# Auto generated Mie input for phase function and lagandre parameters\n')
            f.write('# time: ' + date_str + '\n')
            f.write('mie_program MIEV0\n')
            f.write('refrac water\n')  # Use refractive index of water
            f.write('r_eff  ' + str(r_eff) + '\n')  # Specify effective radius grid
            f.write('distribution gamma ' + str(dist_gamma) + '\n')  # Specify gamma size distribution (alpha=7)
            f.write('wavelength   ' + str(wavelength[0]) + ' ' + str(wavelength[1]) + '\n')  # Define wavelength
            f.write('wavelength_step ' + str(wavelength_res) + '\n')  # Define wavelength
            f.write('nstokes ' + str(n_stokes) + '\n')  # Calculate all phase matrix elements
            f.write('nmom_netcdf ' + str(
                n_lagandre) + '\n')  # Number of Legendre terms to be stored innetcdf file, must be > number_of_streams
            f.write('nthetamax 500\n')  # Maximum number of scattering angles to be used to store the phase matrix
            f.write('output_user netcdf\n')  # Write output to netcdf file
            f.write('verbose\n')  # Print verbose output
        os.chdir(self.path)

    def generate_uvspec_mie_input(self, wavelength, sza, umu, phi):
        os.chdir(self.path + '/auto_io_files')
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('UVSPEC_MIE_AUTO.INP', 'w') as f:
            f.write('# Auto generated uvpsec input from the Mie simulation\n')
            f.write('# time: ' + date_str + '\n')
            f.write('data_files_path ../data/\n')
            f.write('atmosphere_file          ../data/atmmod/afglms.dat\n')  # Use refractive index of water
            f.write('wavelength ' + str(wavelength) + '\n')  # Specify effective radius grid
            f.write('sza ' + str(sza) + '\n')  # Specify gamma size distribution (alpha=7)
            f.write('zout boa\n')
            f.write('umu ' + array_to_str(umu) + '\n')  # Define wavelength
            f.write('phi ' + array_to_str(phi) + '\n')  # Calculate all phase matrix elements
            f.write(
                'wc_file 1D ../auto_io_files/WC.DAT\n')  # Number of Legendre terms to be stored innetcdf file, must be > number_of_streams
            f.write('wc_properties wc.gamma_007.0.mie.cdf interpolate\n')  # Maximum number of scattering angles to be used to store the phase matrix
            f.write('number_of_streams  4\n')
            f.write('rte_solver polradtran\n')
            f.write('polradtran nstokes 3\n')
            f.write('quiet\n')  # Print verbose output
        os.chdir(self.path)

    def generate_uvspec_aerosol_input(self, wavelength, sza, umu, phi):
        os.chdir(self.path + '/auto_io_files')
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('UVSPEC_AEROSOL_AUTO.INP', 'w') as f:
            f.write('# Auto generated uvpsec input from the Mie simulation\n')
            f.write('# time: ' + date_str + '\n')
            f.write('atmosphere_file ../data/atmmod/afglus.dat\n')
            f.write('albedo 0.2\n')
            f.write('sza ' + str(sza) + '\n')  # Specify gamma size distribution (alpha=7)
            f.write('wavelength ' + str(wavelength) + '\n')  # Specify effective radius grid
            f.write('phi0 30                  # Solar azimuth angle\n')
            f.write('phi ' + array_to_str(phi) + '\n')  # Calculate all phase matrix elements
            f.write('umu ' + array_to_str(umu) + '\n')
            # f.write('disort_intcor moments\n') #add aerosol
            # f.write('zout 0 1.5 2.5 4 100.0\n') #add aerosol
            # f.write('polradtran_nstokes 4     # Number of Stokes parameters\n')
            # f.write('rte_solver polradtran\n')
            f.write('rte_solver disort        # Radiative transfer equation solver\n')
            f.write('aerosol_default          # switch on aerosol\n')
            # f.write('aerosol_species_file     continental_average	\n')
            f.write('aerosol_file moments wc.gamma_007.0.mie.cdf\n')
            f.write('quiet')
        os.chdir(self.path)

    def generate_uvspec_aerosol_custom_input(self, wavelength, sza, umu, phi):
        os.chdir(self.path + '/auto_io_files')
        now = datetime.now()
        date_str = now.strftime("%m/%d/%Y, %H:%M:%S")
        with open('UVSPEC_AEROSOL_AUTO.INP', 'w') as f:
            f.write('# Auto generated uvpsec input from the Mie simulation\n')
            f.write('# time: ' + date_str + '\n')
            f.write('atmosphere_file ../data/atmmod/afglus.dat\n')
            f.write('source solar ../data/solar_flux/atlas_plus_modtran\n')
            f.write('mol_modify O3 300. DU    # Set ozone column\n')
            f.write('day_of_year 170          # Correct for Earth-Sun distance\n')
            f.write('albedo 0.2\n')
            f.write('sza ' + str(sza) + '\n')  # Specify gamma size distribution (alpha=7)
            f.write('rte_solver disort        # Radiative transfer equation solver\n')
            f.write('number_of_streams  6     # Number of streams\n')
            f.write('wavelength ' + str(wavelength) + '\n')  # Specify effective radius grid
            f.write('slit_function_file ../examples/TRI_SLIT.DAT\n')
            # f.write('spline 300 340 1         # Interpolate from first to last in step')
            #params from aerosol moments file
            f.write('aerosol_vulcan 1          # Aerosol type above 2km\n')
            f.write('aerosol_haze 6            # Aerosol type below 2km\n')
            f.write('aerosol_season 1          # Summer season\n')
            f.write('aerosol_visibility 50.0   # Visibility\n')
            f.write('aerosol_angstrom 1.1 0.07 # Scale aerosol optical depth \n')
            f.write('aerosol_modify gg set 0.70       # Set the asymmetry factor\n')
            f.write('aerosol_file tau ../examples/AERO_TAU.DAT\n')
            f.write('aerosol_file moments ../examples/AERO_MOMENTS.DAT\n')
            f.write('disort_intcor moments\n')
            f.write('phi0 30                  # Solar azimuth angle\n')
            f.write('phi ' + array_to_str(phi) + '\n')  # Calculate all phase matrix elements
            f.write('umu ' + array_to_str(umu) + '\n')
            # f.write('disort_intcor moments\n') #add aerosol
            # f.write('zout 0 1.5 2.5 4 100.0\n') #add aerosol
            # f.write('polradtran_nstokes 4     # Number of Stokes parameters\n')
            # f.write('rte_solver polradtran\n')
            # f.write('aerosol_default          # switch on aerosol\n')
            # # f.write('aerosol_species_file     continental_average	\n')
            # f.write('aerosol_file moments wc.gamma_007.0.mie.cdf\n')
            # f.write('quiet')
        os.chdir(self.path)

    def run_mie(self, file_name='MIE_AUTO.INP'):
        os.chdir(self.path + '/auto_io_files')
        # name of output file is meaningless since cdf is saved
        cmd = '../bin/mie <' + file_name + '> temp.out'
        so = os.popen(cmd).read()
        print(so)

    def run_uvspec(self, file_name='UVSPEC_MIE_AUTO.INP'):
        os.chdir(self.path + '/auto_io_files')
        # name of output file is meaningless since cdf is saved
        cmd = '../bin/uvspec <' + file_name + '> uvspec_output.out'
        so = os.popen(cmd).read()
        print(so)

    def read_output_polarized(self, umu_vec, phi_vec, file_name='uvspec_output.out'):  # ,
        os.chdir(self.path + '/auto_io_files')
        N = len(umu_vec)
        M = len(phi_vec)
        radiance_mat = np.zeros([4, N, M])
        with open(file_name) as f:
            lines = f.readlines()
            stokes_header_ind = []
            for ind, str_line in enumerate(lines):
                if str_line[0:6] == 'Stokes':
                    stokes_header_ind.append(ind)
            # Read I Values
            for jj in range(0, 2):
                cord_lines = lines[(stokes_header_ind[jj] + 1):stokes_header_ind[jj + 1]]
                for ii in range(0, len(cord_lines)):
                    cord_lines_c = cord_lines[ii].split(' ')
                    cord_lines_c = [float(x) for x in cord_lines_c if len(x) > 2]
                    radiance_mat[jj, ii, :] = cord_lines_c[2:]
            cord_lines = lines[(stokes_header_ind[2] + 1):]
            for ii in range(0, len(cord_lines)):
                cord_lines_c = cord_lines[ii].split(' ')
                cord_lines_c = [float(x) for x in cord_lines_c if len(x) > 2]
                radiance_mat[2, ii, :] = cord_lines_c[2:]
        return radiance_mat

    def read_output_intensity(self, umu_vec, phi_vec, file_name='uvspec_output.out'):  # ,
        os.chdir(self.path + '/auto_io_files')
        N = len(umu_vec)
        M = len(phi_vec)
        radiance_mat = np.zeros([N, M])
        output_df = pd.read_table(file_name, header = None)
        radiance_values = output_df.values
        for ii in range(0, len(radiance_values) - 2):
            #rows first is header second is angle values
            current_row = radiance_values[ii + 2, 0].split(" ")
            radiance_mat[ii, :] = [float(x) for x in current_row if len(x) > 2][2:] #first index is angle second is a summation
        return radiance_mat


def array_to_str(num_arr):
    return_str = ""
    for num in num_arr:
        #TODO add precision
        return_str += str(round(num, 9)) + " "
    return return_str


