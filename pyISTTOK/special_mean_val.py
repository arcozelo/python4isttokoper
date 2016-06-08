import numpy
def special_mean_val(input_data, threshold):

    mask = input_data > threshold;
 
    temp=numpy.extract(mask,input_data)
    final = numpy.mean(temp)        
    
#    print "Mean value was "+str(final)
    
    return final;

