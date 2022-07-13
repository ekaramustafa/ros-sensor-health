#!/usr/bin/env python
import time
import rospy
from rostopic import ROSTopicHz

def main():

    rospy.init_node('sensor_health', anonymous=True)
   
    #static final params
    WINDOWS_SIZE=-1 
    FILTER_EXPR=None
  
    #list for topics from launch file
    selected_topics = []

    #list for desired hzs
    threshs = []

    #temp lists
    hz = []
    subs = []
    rts = []

    ##TO-DO 
    #add ros time instead of python time

    #getting all topics and desired hzs
    params = rospy.get_param("/sensor_health/topics").strip()
    params = params.split(",")

    for i in range(len(params)):
        temp_param = params[i].split(":")

        temp_topic = temp_param[0].strip()
        selected_topics.append(temp_topic)
        
        temp_thresh = temp_param[1].strip()
        threshs.append(float(temp_thresh))

    while not rospy.is_shutdown():

        #time could be added as a info  
        tim = time.localtime()
        current_time = time.strftime("%H:%M:%S", tim)

                        
        #i = counter, j = selected_topics[i]
        for i,j in enumerate(selected_topics):
            
            i = ROSTopicHz(WINDOWS_SIZE,FILTER_EXPR)    
            rts.append(i)
           
            i = rospy.Subscriber(j, rospy.AnyMsg, i.callback_hz)  
            subs.append(i) 
        
        rospy.sleep(1)
        
        for l in range(len(selected_topics)):
           
            #ret = rate,min_delta,max_delta,std_dev,window 
            ret = rts[l].get_hz()

            if ret is None:
                rospy.logerr(f"No new messages from {selected_topics[l]}")
                hz.append(0) # 0 means no messages received
            else:
                #ret = rate,min_delta,max_delta,std_dev,window 
                rate = ret[0]
                hz.append(rate)

        for n in range(len(hz)):
            
            #unregister to prevent hz accumulation 
            subs[n].unregister()

            #validate hz of topics

            if hz[n] < threshs[n] and hz[n]:
                rospy.logerr(f"Topic {selected_topics[n]} is under threshold rate: {round(hz[n],3)}hz threshold: {threshs[n]} at {current_time}")
        print()       

        ##clear all lists
        hz.clear()
        subs.clear()
        rts.clear()

    rospy.spin()

if __name__ == '__main__':
    main()

