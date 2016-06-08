import numpy

def exposure_time(input_data, input_data_time, threshold):

    dt = input_data_time[2]-input_data_time[1];
    delta = 0;
    

    #for i in range(1,len(input_data)):
    #    if input_data[i]>threshold:
    #        delta +=dt;
    mask = input_data > threshold;
    delta = numpy.sum(mask)*dt;

    print "There was "+str(delta/1e3)+" ms of plasma"
    
    final = delta/1e3;

    return final;

