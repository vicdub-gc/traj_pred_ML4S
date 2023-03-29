[Last update: 2022/11/11]
The data is part of pNEUMA dataset(https://open-traffic.epfl.ch/) pre-processed for lane-changing study. 
(!!) Please do not share this data in public without permission (!!)

The folder includes...
	1. trajectory data of only for the vehicles that travels between OD gates (DAY_Dx_TIME_OD_trajectories.csv)
	2. OD statistics of vehicles (DAY_Dx_TIME_OD_stat.csv)
	3. scheme of the OD (OD_scheme_Dx.png)

The trajectory data contains...
  - x[m], y[m] : Vehicle's location (in UTM format) at time T
  - Speed [km/h] : Vehicle's instantaneous speed at time T
  - Tan. Acc. [ms-2] : Logitudinal acceleration of vehicle at time T
  - Lat. Acc. [ms-2] : Lateral acceleration of vehicle at time T
  - Time [s] : Timestep of the trajectory	
  - Angle [rad] : Vehicle's headings at time T
  - Traffic Regions(list) : A list of traffic region(lane in this case) where vehicle is at. 
			    If empty, vehicle is on the edge of two lane and it can be interpolated based on the regions from the neighboring timesteps.


In case of any question, please contact Sohyeong KIM (sohyeong.kim@epfl.ch). 


[Note1] Date <--> Day
  - 20181029 Monday
  - 20181030 Tuesday
  - 20181024 Wednesday
  - 20181101 Thursday