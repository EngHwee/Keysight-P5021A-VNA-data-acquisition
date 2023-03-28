import time
import pyvisa
import serial
import math
import numpy as np
import csv
from itertools import zip_longest

rm = pyvisa.ResourceManager()

#set instrument address and variables
VISA_Addr = 'TCPIP0::localhost::hislip_PXI10_CHASSIS1_SLOT1_INDEX0::INSTR'

#establish VISA connection
vna = rm.open_resource(VISA_Addr)
print(vna.query('*IDN?'))
print("Connection for VNA established")

#set format of instrument to return
vna.write('FORMat REAL,64')

#set byte order to swapped (little-endian) format
vna.write('FORMat:BORDer SWAP')

arduino = serial.Serial('COM6')
arduino.baudrate = 9600
arduino.timeout = 5
arduino.bytesize = 8
arduino.parity = 'N'
arduino.stopbits = 1
time.sleep(3)

counter = 1
msg = b'b'

while counter < 102:

    if msg == b'b':
        print('Received b from Arduino')
        print("Interval:%d" %(counter))
        percentage1 = 100
        percentage2 = 100
        percentage3 = 100
        percentage4 = 100
        starttime = time.time()

        while (percentage1 > 1) or (percentage2 > 10) or (percentage3 > 10) or (percentage4 > 1):
            #request and read trace measurement data from instrument
            data = vna.query_binary_values('CALC:DATA:MSD? "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"', datatype='d')
            print(data)
            #split data based on their traces
            TR1 = data[:len(data)//16]
            TR2 = data[len(data)//16:len(data)//16*2]
            TR3 = data[len(data)//16*2:len(data)//16*3]
            TR4 = data[len(data)//16*3:len(data)//16*4]
            TR5 = data[len(data)//16*4:len(data)//16*5]
            TR6 = data[len(data)//16*5:len(data)//16*6]
            TR7 = data[len(data)//16*6:len(data)//16*7]
            TR8 = data[len(data)//16*7:len(data)//16*8]
            TR9 = data[len(data)//16*8:len(data)//16*9]
            TR10 = data[len(data)//16*9:len(data)//16*10]
            TR11 = data[len(data)//16*10:len(data)//16*11]
            TR12 = data[len(data)//16*11:len(data)//16*12]
            TR13 = data[len(data)//16*12:len(data)//16*13]
            TR14 = data[len(data)//16*13:len(data)//16*14]
            TR15 = data[len(data)//16*14:len(data)//16*15]
            TR16 = data[len(data)//16*15:]

            #split data into real and imaginary
            TR1r = TR1[::2]
            TR1i = TR1[1::2]
            TR2r = TR2[::2]
            TR2i = TR2[1::2]
            TR3r = TR3[::2]
            TR3i = TR3[1::2]
            TR4r = TR4[::2]
            TR4i = TR4[1::2]
            TR5r = TR5[::2]
            TR5i = TR5[1::2]
            TR6r = TR6[::2]
            TR6i = TR6[1::2]
            TR7r = TR7[::2]
            TR7i = TR7[1::2]
            TR8r = TR8[::2]
            TR8i = TR8[1::2]
            TR9r = TR9[::2]
            TR9i = TR9[1::2]
            TR10r = TR10[::2]
            TR10i = TR10[1::2]
            TR11r = TR11[::2]
            TR11i = TR11[1::2]
            TR12r = TR12[::2]
            TR12i = TR12[1::2]
            TR13r = TR13[::2]
            TR13i = TR13[1::2]
            TR14r = TR14[::2]
            TR14i = TR14[1::2]
            TR15r = TR15[::2]
            TR15i = TR15[1::2]
            TR16r = TR16[::2]
            TR16i = TR16[1::2]
            
            magnitude1 = np.sqrt(np.square(TR1r)+np.square(TR1i))
            magnitude2 = np.sqrt(np.square(TR2r)+np.square(TR2i))
            magnitude3 = np.sqrt(np.square(TR5r)+np.square(TR5i))
            magnitude4 = np.sqrt(np.square(TR6r)+np.square(TR6i))

            time.sleep(3)

            dataX = vna.query_binary_values('CALC:DATA:MSD? "1,2,5,6"', datatype='d')
            print(dataX)
            #split data based on their traces
            TR1X = dataX[:len(dataX)//4]
            TR2X = dataX[len(dataX)//4:len(dataX)//4*2]
            TR3X = dataX[len(dataX)//4*2:len(dataX)//4*3]
            TR4X = dataX[len(dataX)//4*3:]
            #split data into real and imaginary
            TR1rX = TR1X[::2]
            TR1iX = TR1X[1::2]
            TR2rX = TR2X[::2]
            TR2iX = TR2X[1::2]
            TR3rX = TR3X[::2]
            TR3iX = TR3X[1::2]
            TR4rX = TR4X[::2]
            TR4iX = TR4X[1::2]
            magnitude1X = np.sqrt(np.square(TR1rX)+ np.square(TR1iX))
            magnitude2X = np.sqrt(np.square(TR2rX)+ np.square(TR2iX))
            magnitude3X = np.sqrt(np.square(TR3rX)+ np.square(TR3iX))
            magnitude4X = np.sqrt(np.square(TR4rX)+ np.square(TR4iX))

            MSE1 = np.square(np.subtract(magnitude1,magnitude1X)).mean()
            RMSE1 = math.sqrt(MSE1)
            percentage1 = RMSE1/np.average(magnitude1)*100
            MSE2 = np.square(np.subtract(magnitude2,magnitude2X)).mean()
            RMSE2 = math.sqrt(MSE2)
            percentage2 = RMSE2/np.average(magnitude2)*100
            MSE3 = np.square(np.subtract(magnitude3,magnitude3X)).mean()
            RMSE3 = math.sqrt(MSE3)
            percentage3 = RMSE3/np.average(magnitude3)*100
            MSE4 = np.square(np.subtract(magnitude4,magnitude4X)).mean()
            RMSE4 = math.sqrt(MSE4)
            percentage4 = RMSE4/np.average(magnitude4)*100

            print("RMSE1:%f" %RMSE1)
            print("Percentage1:%.2f" %percentage1)
            print("RMSE2:%f" %RMSE2)
            print("Percentage2:%.2f" %percentage2)
            print("RMSE3:%f" %RMSE3)
            print("Percentage3:%.2f" %percentage3)
            print("RMSE4:%f" %RMSE4)
            print("Percentage4:%.2f" %percentage4)

        endtime = time.time()
        print("Time taken for data to stablise:%.2f seconds" %(endtime - starttime))

        #write data into csv
        data = [TR1r, TR1i, TR2r, TR2i, TR3r, TR3i, TR4r, TR4i, TR5r, TR5i, TR6r, TR6i, TR7r, TR7i, TR8r, TR8i, TR9r, TR9i, TR10r, TR10i, TR11r, TR11i, TR12r, TR12i, TR13r, TR13i, TR14r, TR14i, TR15r, TR15i, TR16r, TR16i]
        export_data = zip_longest(*data, fillvalue='')
        with open('%d.csv' %counter, 'w', encoding="ISO-8859-1", newline='') as file:
            write = csv.writer(file)
            write.writerows(export_data)
        file.close()

        counter = counter + 2

        if counter < 102:
            msg = b'a'
            arduino.write(msg)
            print('Sending a to Arduino')
            time.sleep(5)

    msg = arduino.read()

msg = b'c'
arduino.write(msg)
print('Sending c to Arduino')
time.sleep(2)
arduino.close()
