import numpy

def period_counter(input_data, threshold, tester = numpy.append(numpy.ones(200),numpy.zeros(1))):
    count = 0
    #tester = numpy.append(numpy.ones(200),numpy.zeros(1));
    s = ''
    
    mask = input_data > threshold; 
    
    for i in range(len(mask[250:])-len(tester)):
        if numpy.sum(numpy.equal(mask[250+i:250+i+len(tester)],tester))==len(tester):
	        count+=1
	        #~ s+=str(1)
        #~ else :
			#~ s+=str(0)
        #~ if i % 2 == 0 :
			#~ s+=' '
    
    return count,s;
