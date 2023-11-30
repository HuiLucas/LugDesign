import numpy
f_in_planex = 2
f_in_planez = 5
f_in_planey = 7
P_i = numpy.sqrt(f_in_planex**2+f_in_planez**2+f_in_planey**2)
D2 = 1
t2 = 3
sigmabrm = 2000
sigmabr = P_i / (D2 * t2)
if sigmabr <= sigmabrm:
    print("No Failure so weight can be reduced")

else:
    print("Failure, add more fasteners or increase the thickness")

    