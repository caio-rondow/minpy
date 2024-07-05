from math import log, ceil, pow
from .slider import Slider
import numpy as np

class Omega:
    def __init__(self, n : int, extras : int = 0, radix : int = 4) -> None:
        
        self.size       : int = n
        self.extras     : int = extras
        self.radix      : int = radix
        self.stages     : int = ceil(log(n, radix)) + extras
        self.num_extras : int = ceil(pow(radix, extras))

        self.window : Slider = Slider(n, extras, radix)

        self.__min    : np.ndarray = None
        self.__swt    : np.ndarray = None

        self.__routed : dict = None

        self.clear()
    
    def route(self, input : int, output : int) -> bool:

        assert 0 <= input  < self.size, f"input must be in between [0,{self.size})"
        assert 0 <= output < self.size, f"output must be in between [0,{self.size}"

        for extra in range(self.num_extras):

            found_path : bool = True
            path       : bool = self.window.concat(input, extra, output)

            for stage in range(self.stages):

                row : int = self.window.slide(path, stage+1)

                if not self.__is_path_available(path, row, stage):
                    found_path = False
                    break
            
            if found_path:
                self.__send_message(path)
                return True
            
        return False
    
    def unroute(self, output):

        assert 0 <= output < self.size, f"output must be in between [0,{self.size}"

        if output in self.__routed:
            return False

        path : int = self.__routed[output]

        for stage in range(self.stages):

            row : int = self.window.slide(path, stage+1)
            idx : int = row * self.stages + stage

            self.__min[idx] = max(0, self.__min[idx])

            if self.__min[idx] == 0:
                self.__swt[idx] = -1

        return True

    def __is_path_available(self, path, row, col) -> bool:

        is_path_free : bool = self.__min[ row * self.stages + col ] == 0
        is_multicast : bool = self.__swt[ row * self.stages + col ] == self.window.source(path, col+1)

        return is_path_free or is_multicast

    def __send_message(self, path) -> None:

        for stage in range(self.stages):

            row : int = self.window.slide(path, stage+1)

            self.__min[ row * self.stages + stage] += 1
            self.__swt[ row * self.stages + stage]  = self.window.source(path, stage+1)

    def clear(self) -> None:
        self.__min    = np.zeros(self.size * self.stages, dtype=int)
        self.__swt    = np.zeros(self.size * self.stages, dtype=int) - 1
        self.__routed = {}

    def show(self) -> None:
        for i in range(self.size):
            for j in range(self.stages):
                print(self.__min[ i * self.stages + j], end=' ')
            print() 
