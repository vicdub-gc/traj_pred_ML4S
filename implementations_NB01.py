import csv
import numpy as np
import re

"""
1) Reading CSV files | Line 10
2) Data Handling | Line 30
"""

################## Reading CSV files ##################

def read_traj_csv(csv_traj_entry):
    """Generates a header file and a str with all the lines of a csv file.         
    Args:
        csv_traj_entry: path to the csv file we want to read  
    Returns:
        header : title of each column
        lines : all the lines of the csv stored in a single list of str 
    """
    with open(csv_traj_entry, newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        header = header[0].split(';')
        lines = []
        for row in reader:
            lines.append(row)
        f.close()
    return header, lines

################## Data Handling ##################

def fill_no_lanes(info_measured_veh): #no need to call this function, already implemented in infos_vehicule_i
    '''Fills in the empty lanes of a vehicule, copies the last known lane until another one is detected. Fills the last empty lanes with LaneOut.
    Args: 
        info_measured_veh: all the measured informations of a vehicule
    '''
    empty_lane = '"'
    LaneOut = "Lane Out"
    LaneIn = "Lane In"
    ind = 0
    if(info_measured_veh[0,7]==empty_lane):
        info_measured_veh[0,7]=LaneIn #first element as LaneIn for now
    while(info_measured_veh[-ind-1,7] == empty_lane):
        info_measured_veh[-ind-1,7] = LaneOut #last elements as LaneOut -> outside the measured region
        ind = ind + 1
    for ind in range(len(info_measured_veh[:,7])):
        if (info_measured_veh[ind,7] == empty_lane):
            info_measured_veh[ind,7]=info_measured_veh[ind-1,7] #fills the empty lanes with the last known lane
    nbr_LaneIn = np.sum(info_measured_veh[:,7]=='Lane In')
    info_measured_veh[0:nbr_LaneIn,7] = info_measured_veh[nbr_LaneIn+1,7] #Replaces the first LaneIn with the first known Lane
    return

def infos_vehicule_i(lines_str,indice):
    """
    Generate all the informations for a track ID .      
    Args:
        lines_str: list with informations of all the vehicules (all_lines)
        indice : track ID     
    Returns:
        info_init : general info about the vehicule
        info_measured : all the measured informations 
    """
    full_array = np.asarray(lines_str[indice][0].split(';'))
    info_init = np.asarray(full_array[0:8],dtype=object)
    for ind in [3,5,6,7]:
        info_init[ind] = float(info_init[ind])
    info_init[0] = int(info_init[0])
    info_measured = np.asarray(full_array[8:-1],dtype=object)
    info_measured = np.reshape(info_measured,(-1,8))
    info_measured[:,:-1]=info_measured[:,:-1].astype(float)
    fill_no_lanes(info_measured)
    return info_init, info_measured

def update_track_id(all_lines): 
    '''Updates the track ID to int between 0 and 2032
    Args: 
        all_lines : list with all info from csv
    '''
    for ind in range(len(all_lines)):
        all_lines[ind][0] = all_lines[ind][0].replace(re.search(r'\d+', all_lines[ind][0][0:4]).group(),str(ind),1)
    return


def compute_chgmnt_ID_i(all_lines,track_id):
    """Computes the number of lane changes for a track ID.     
    Args:
        all_lines : list with info of all vehicules
        track_id: track id of vehicule
    Returns:
        chgmnt_ID_i: nbr of lane change for track ID i
    """

    info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, track_id)
    nbr_chgmnt = 0 ;
    for ind in range(len(info_measured_veh[:,7])-1):
        if (info_measured_veh[ind,7] != info_measured_veh[ind+1,7]):
            nbr_chgmnt = nbr_chgmnt+1
    nbr_chgmnt = nbr_chgmnt-1 #Last change to LaneOut not wanted
    return nbr_chgmnt


def compute_dist_last_lane_ID_i(all_lines,track_ID):
    """Computes the distance parcoured on the last lane.     
    Args:
        all_lines : list with info of all vehicules
        track_id: track id of vehicule
    Returns:
        dist: distance in meters
    """
    info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, track_ID)
    #Check if vehicule has MC
    if ((info_init_veh[4]==' Destination 3') or ((info_init_veh[4]==' Destination 1') and (info_measured_veh[0,7]==' "Lane 3"'))):
        dist = 0
    else:
        t_out = 0 #Note : not really a time, since we measure every .4s I think
        last_t = 0
        for t in range(len(info_measured_veh[:,7])):
            if info_measured_veh[len(info_measured_veh[:,7])-1-t,7] != "Lane Out":
                t_out = len(info_measured_veh[:,7])-t-1 #Last mesure before Lane Out
                break
        last_lane = info_measured_veh[t_out,7]
        for t in np.arange(t_out,0,-1):
            if info_measured_veh[t,7] != last_lane:
                last_t = t
                break

        x_entry = info_measured_veh[last_t+1,0]
        y_entry = info_measured_veh[last_t+1,1]
        x_out = info_measured_veh[t_out,0]
        y_out = info_measured_veh[t_out,1]
        dist = np.sqrt((x_entry-x_out)**2+(y_entry-y_out)**2)
    return dist