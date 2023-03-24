from pathlib import Path
home = str(Path.home())
param_file_path = home + "/catkin_ws/src/turtlebot3/turtlebot3_navigation/param/dwa_local_planner_params_waffle_pi.yaml"

def rewrite_file(params_to_use_path):
    with open(params_to_use_path,"r") as params_to_use, open(param_file_path,"w") as param_file:
        params_to_use.seek(0)
        param_file.seek(0)
        for line in params_to_use:
            param_file.write(line)
        param_file.truncate()