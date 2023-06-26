import ctypes

clibrary = ctypes.CDLL("C:/Programacion/projects/ArmonicApp/algorithm/cpplibrary.so")

clibrary.square(25)