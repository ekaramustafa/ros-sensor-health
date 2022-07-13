# ROS SENSOR HEALTH
This ROS-Noetic package is basically code-implementation of `rostopic hz /topic1_name /topic2_name ...`.
It is helpful to check whether given topics are published and if their hz values are above the given threshold value

## Implementation
In `sensor_health.launch` file, modify value of `topics` param in accordance with the following format:
>`/topic1_name:threshold1,topic2_name:threshold2 ...`

After starting `roscore` type the following in new terminal:
>`roslaunch sensor_health sensor_health.launch`

Then you should be able to see if any undesirable issue occurs
