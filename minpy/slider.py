import math

class Slider:
    
    def __init__(self, size : int, extras : int, radix : int) -> None:
        
        self.WIN_BITS   : int = math.ceil(math.log2(size))
        self.EXT_BITS   : int = math.ceil(radix / 2) + extras
        self.WORD_BITS  : int = 2 * self.WIN_BITS + self.EXT_BITS
        self.WIN_MASK   : int = size - 1
        self.SRC_MASK   : int = radix - 1
        self.SLIDE_RATE : int = math.ceil(radix / 2)

    def slide(self, word : int, col : int) -> int:
        return (word >> (self.WORD_BITS - col * self.SLIDE_RATE - self.WIN_BITS)) & self.WIN_MASK

    def concat(self, begin : int, middle : int, end : int) -> int:
        return end | (middle << self.WIN_BITS) | (begin << (self.WIN_BITS + self.EXT_BITS))

    def source(self, word : int, col : int) -> int:
        return (word >> (self.WORD_BITS - col * self.SLIDE_RATE)) & self.SRC_MASK