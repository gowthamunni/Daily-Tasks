from msehandler import MSEHandler
import numpy as np

#maybe pass this value as a parameter like acceptable value
# or everything within a class
def compareresults(onnxresult, kerasresult):
    mse = np.mean(np.square(kerasresult - onnxresult.tranpose([0,2,3,1])))

    if mse < 1e-10:
        MSEHandler.mselesserthan1raisedminus10(mse)
    
    elif (1e-5 > mse > 1e-10):
        MSEHandler.msebetweeen1raisedminus5andminus10(mse)
    elif mse > 1e-5:
        MSEHandler.msegreaterthan1raisedtominus5(mse)






