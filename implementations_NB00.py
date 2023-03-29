import csv
import numpy as np
import re
import matplotlib.pyplot as plt

"""
1) Plots | Line 12
2) Reading CSV files | Line 46
3) Data Handling | Line 110
"""

################## Plots ##################

def plot_average_traj_t0_tf(csv_stat_entry,title):
    """Plots the average trajectories for each destination between t0 and tf.       
    Args:
        csv_traj_entry: path to the stat csv file we want to read
    """
    headers_stat, measured_22to23_t0_tf, measured_22to24_t0_tf, measured_22to25_t0_tf, infos22to23_t0_tf, infos22to24_t0_tf, infos22to25_t0_tf = open_stat_csv(
    csv_stat_entry
    )
    plt.figure()
    plt.plot(measured_22to23_t0_tf[:,0],measured_22to23_t0_tf[:,1],measured_22to24_t0_tf[:,0],measured_22to24_t0_tf[:,1],measured_22to25_t0_tf[:,0],measured_22to25_t0_tf[:,1])
    plt.title(title, fontweight="bold",y=1.06)
    plt.legend(["Destination 1","Destination 2","Destination 3"])
    plt.grid()
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.show()

def plot_traj_ID_i(all_lines,track_id):
    """Plots the trajectory for a certain track ID.     
    Args:
        track_id: track ID we want to plot  
        all_lines : list with info of all vehicules
    """
    info_init_ID ,info_measured_ID = infos_vehicule_i(all_lines, track_id)
    plt.figure()
    plt.plot(info_measured_ID[:,0],info_measured_ID[:,1])
    plt.title(f'Trajectory of vehicule {track_id}', fontweight="bold",y=1.06)
    plt.grid()
    plt.xlabel("x coordinate")
    plt.ylabel("y coordinate")
    plt.show()

################## Reading CSV files ##################

def open_stat_csv(csv_stat_entry):
    """Reads the informations in a csv_stat file         
    Args:
        csv_traj_entry: path to the stat csv file we want to read
    Returns:
        headers : title of each column
        3x - measured_22toX_t0_tf : x,y,t data between 22 to X
        3x - infos22toX : general infos between 22 to X
    """
    with open(csv_stat_entry, newline='') as f:
        reader = csv.reader(f)
        header = next(reader) 
        from22to23 = next(f) ; from22to24 = next(f) ; from22to25 = next(f) 
    f.close()
    headers = header[0].split(';')

    from22to23_list = from22to23.split(';') #separe a chaque ; en une liste de str
    #convert les valeurs en float (sauf premieres valeures de moyennes etc)
    values22to23 = [float(x) for x in from22to23_list[10:(len(from22to23_list)-1)]]
    values22to23 = np.asarray(values22to23) #passe en numpy array
    infos22to23 = from22to23_list[0:10] #les infos initiales (vitesses moyennes etc)

    from22to24_list = from22to24.split(';')
    values22to24 = [float(x) for x in from22to24_list[10:(len(from22to24_list)-1)]]
    values22to24 = np.asarray(values22to24)
    infos22to24 = from22to24_list[0:10]

    from22to25_list = from22to25.split(';')
    values22to25 = [float(x) for x in from22to25_list[10:(len(from22to25_list)-1)]]
    values22to25 = np.asarray(values22to25)
    infos22to25 = from22to25_list[0:10]

    x_22to23_t0_tf = values22to23[::3] ; y_22to23_t0_tf = values22to23[1::3] ; t_22to23_t0_tf = values22to23[2::3]
    x_22to23_t0_tf.shape = (x_22to23_t0_tf.shape[0],1) ; y_22to23_t0_tf.shape = (y_22to23_t0_tf.shape[0],1) ; t_22to23_t0_tf.shape = (t_22to23_t0_tf.shape[0],1) ; 
    measured_22to23_t0_tf = np.concatenate((x_22to23_t0_tf,y_22to23_t0_tf,t_22to23_t0_tf),axis=1)
    x_22to24_t0_tf = values22to24[::3] ; y_22to24_t0_tf = values22to24[1::3] ; t_22to24_t0_tf = values22to24[2::3]
    x_22to24_t0_tf.shape = (x_22to24_t0_tf.shape[0],1) ; y_22to24_t0_tf.shape = (y_22to24_t0_tf.shape[0],1) ; t_22to24_t0_tf.shape = (t_22to24_t0_tf.shape[0],1) ; 
    measured_22to24_t0_tf = np.concatenate((x_22to24_t0_tf,y_22to24_t0_tf,t_22to24_t0_tf),axis=1)
    x_22to25_t0_tf = values22to25[::3] ; y_22to25_t0_tf = values22to25[1::3] ; t_22to25_t0_tf = values22to25[2::3]
    x_22to25_t0_tf.shape = (x_22to25_t0_tf.shape[0],1) ; y_22to25_t0_tf.shape = (y_22to25_t0_tf.shape[0],1) ; t_22to25_t0_tf.shape = (t_22to25_t0_tf.shape[0],1) ; 
    measured_22to25_t0_tf = np.concatenate((x_22to25_t0_tf,y_22to25_t0_tf,t_22to25_t0_tf),axis=1)
    return headers, measured_22to23_t0_tf, measured_22to24_t0_tf, measured_22to25_t0_tf, infos22to23, infos22to24, infos22to25


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
    '''Updates the track ID to unique int 
    Args: 
        all_lines : list with all info from csv
    '''
    for ind in range(len(all_lines)):
        all_lines[ind][0] = all_lines[ind][0].replace(re.search(r'\d+', all_lines[ind][0][0:4]).group(),str(ind),1)
    return

def compute_chgmnt_di_olx(all_lines,di_olx):
    """Computes the number of lane changes for each vehicule.     
    Args:
        all_lines : list with info of all vehicules
        di_olx: numpy array with track id for vehicule going to i from lane x  
    Returns:
        chgmnt_di_olx: numpy array with track IDs and nbr of lane changes 
    """
    chgmnt_di_olx = np.empty((len(di_olx),2))
    i = 0
    for veh in di_olx:
        info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, veh)
        nbr_chgmnt = 0 ;
        for ind in range(len(info_measured_veh[:,7])-1):
            if (info_measured_veh[ind,7] != info_measured_veh[ind+1,7]):
                nbr_chgmnt = nbr_chgmnt+1
        nbr_chgmnt = nbr_chgmnt-1 #dernier changement vers LaneOut pas compté ?
        chgmnt_di_olx[i,0]=veh
        chgmnt_di_olx[i,1]=nbr_chgmnt
        i = i+1
    return chgmnt_di_olx

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

###### DESTINATION 1

def spot_mandatory_changes_d1_ol2(all_lines, destination_origin):
    '''
    Args: 
    destination_origin: list of track ids for the classification defined before : dX_olY
                        with X = destination 1
                        with Y = Original lane 2
    Output: 
    mandatory_changes: Dictionnary with as key the track id, 
                        then 4 values as outputs: 
                        vehicle type
                        position at the lane change x and y 
                        time at the lane change
    '''
    mandatory_changes={} # Dict structure : vehicle track id : [type,x,y,t]
    
    for veh in destination_origin: 
        info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, veh)
        num_lanes_info = info_measured_veh.shape[0]
        changes_23=list()
        count_l2=0
        for i in range(num_lanes_info):
            if info_measured_veh[i][7]== ' "Lane 1"':
                count_l2+=1
            if info_measured_veh[i][7]== ' "Lane 2"':
                count_l2+=1
                if info_measured_veh[i+1][7]==' "Lane 3"':
                    change_23=count_l2
                    changes_23.append(change_23)
        mandatory_changes[veh]=list()
        mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
        mandatory_changes[veh].append(info_measured_veh[changes_23[0]][0]) #get the x info
        mandatory_changes[veh].append(info_measured_veh[changes_23[0]][1]) #get the y info
        mandatory_changes[veh].append(info_measured_veh[changes_23[0]][5]) #get the time info                
    return mandatory_changes


def spot_mandatory_changes_d1_ol1(all_lines,destination_origin):
    '''
    Args: 
    destination_origin: list of track ids for the classification defined before : dX_olY
                        with X = destination 1
                        with Y = Original lane 1
    Output: 
    mandatory_changes: Dictionnary with as key the track id, 
                        then 4 values as outputs: 
                        vehicle type
                        position at the lane change x and y 
                        time at the lane change
    '''
    mandatory_changes={} # Dict structure : vehicle track id : [type,x,y,t]
    
    for veh in destination_origin: 
        info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, veh)
        num_lanes_info = info_measured_veh.shape[0]
        count_l1=0
        count_l2=0
        changes_12= list()
        changes_23= list()
        for i in range(num_lanes_info):
            if info_measured_veh[i][7]== ' "Lane 1"':
                count_l1 +=1
                count_l2 +=1
                if info_measured_veh[i+1][7]==' "Lane 2"':
                    change_12=count_l1
                    changes_12.append(change_12)
            if info_measured_veh[i][7]== ' "Lane 2"':
                count_l2+=1
                if info_measured_veh[i+1][7]==' "Lane 3"':
                    change_23=count_l2
                    changes_23.append(change_23)

        mandatory_changes[veh]=list()
        if info_measured_veh[changes_12[0]][7]== ' "Lane 2"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_12[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_12[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_12[0]][5]) #get the time info
        if info_measured_veh[changes_23[0]][7]== ' "Lane 3"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][5]) #get the time info    
                
    return mandatory_changes

    
###### DESTINATION 2 
def spot_mandatory_changes_d2_ol3(all_lines, destination_origin):
    '''
    Args: 
    destination_origin: list of track ids for the classification defined before : dX_olY
                        with X = destination 2
                        with Y = Original lane 3
    Output: 
    mandatory_changes: Dictionnary with as key the track id, 
                        then 4 values as outputs: 
                        vehicle type
                        position at the lane change x and y 
                        time at the lane change
    '''
    mandatory_changes={} # Dict structure : vehicle track id : [type,x,y,t]
    
    for veh in destination_origin: 
        info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, veh)
        num_lanes_info = info_measured_veh.shape[0]
        changes_34=list()
        count_l3=0
        for i in range(num_lanes_info):
            if info_measured_veh[i][7]== ' "Lane 1"':
                count_l3+=1
            if info_measured_veh[i][7]== ' "Lane 2"':
                count_l3+=1
            if info_measured_veh[i][7]== ' "Lane 3"':
                count_l3+=1
                if info_measured_veh[i+1][7]==' "Lane 4"':
                    change_34=count_l3
                    changes_34.append(change_34)
        mandatory_changes[veh]=list()
        mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
        mandatory_changes[veh].append(info_measured_veh[changes_34[0]][0]) #get the x info
        mandatory_changes[veh].append(info_measured_veh[changes_34[0]][1]) #get the y info
        mandatory_changes[veh].append(info_measured_veh[changes_34[0]][5]) #get the time info                
    return mandatory_changes


def spot_mandatory_changes_d2_ol2(all_lines, destination_origin):
    '''
    Args: 
    destination_origin: list of track ids for the classification defined before : dX_olY
                        with X = destination 2
                        with Y = Original lane 2
    Output: 
    mandatory_changes: Dictionnary with as key the track id, 
                        then 4 values as outputs: 
                        vehicle type
                        position at the lane change x and y 
                        time at the lane change
    '''
    mandatory_changes={} # Dict structure : vehicle track id : [type,x,y,t]
    
    for veh in destination_origin: 
        info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, veh)
        num_lanes_info = info_measured_veh.shape[0]
        count_l2=0
        count_l3=0
        changes_23= list()
        changes_34= list()
        for i in range(num_lanes_info):
            if info_measured_veh[i][7]== ' "Lane 1"':
                count_l2 +=1
                count_l3 +=1
            if info_measured_veh[i][7]== ' "Lane 2"':
                count_l2 +=1
                count_l3 +=1
                if info_measured_veh[i+1][7]==' "Lane 3"':
                    change_23=count_l2
                    changes_23.append(change_23)
            if info_measured_veh[i][7]== ' "Lane 3"':
                count_l3+=1
                if info_measured_veh[i+1][7]==' "Lane 4"':
                    change_34=count_l3
                    changes_34.append(change_34)

        mandatory_changes[veh]=list()
        if info_measured_veh[changes_23[0]][7]== ' "Lane 3"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][5]) #get the time info
        if info_measured_veh[changes_34[0]][7]== ' "Lane 4"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_34[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_34[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_34[0]][5]) #get the time info    
                
    return mandatory_changes   

def spot_mandatory_changes_d2_ol1(all_lines, destination_origin):
    '''
    Args: 
    destination_origin: list of track ids for the classification defined before : dX_olY
                        with X = destination 2
                        with Y = Original lane 2
    Output: 
    mandatory_changes: Dictionnary with as key the track id, 
                        then 4 values as outputs: 
                        vehicle type
                        position at the lane change x and y 
                        time at the lane change
    '''
    mandatory_changes={} # Dict structure : vehicle track id : [type,x,y,t]
    
    for veh in destination_origin: 
        info_init_veh ,info_measured_veh = infos_vehicule_i(all_lines, veh)
        num_lanes_info = info_measured_veh.shape[0]
        count_l1=0
        count_l2=0
        count_l3=0
        changes_12= list()
        changes_23= list()
        changes_34= list()
        for i in range(num_lanes_info):
            if info_measured_veh[i][7]== ' "Lane 1"':
                count_l1 +=1
                count_l2 +=1
                count_l3 +=1
                if info_measured_veh[i+1][7]==' "Lane 2"':
                    change_12=count_l1
                    changes_12.append(change_12)
            if info_measured_veh[i][7]== ' "Lane 2"':
                count_l2 +=1
                count_l3 +=1
                if info_measured_veh[i+1][7]==' "Lane 3"':
                    change_23=count_l2
                    changes_23.append(change_23)
            if info_measured_veh[i][7]== ' "Lane 3"':
                count_l3+=1
                if info_measured_veh[i+1][7]==' "Lane 4"':
                    change_34=count_l3
                    changes_34.append(change_34)

        mandatory_changes[veh]=list()
        if info_measured_veh[changes_12[0]][7]== ' "Lane 2"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_12[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_12[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_12[0]][5]) #get the time info
        if info_measured_veh[changes_23[0]][7]== ' "Lane 3"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_23[0]][5]) #get the time info
        if info_measured_veh[changes_34[0]][7]== ' "Lane 4"':
            mandatory_changes[veh].append(info_init_veh[1]) #add the type of vehicule 
            mandatory_changes[veh].append(info_measured_veh[changes_34[0]][0]) #get the x info
            mandatory_changes[veh].append(info_measured_veh[changes_34[0]][1]) #get the y info
            mandatory_changes[veh].append(info_measured_veh[changes_34[0]][5]) #get the time info    
                
    return mandatory_changes  