class ClassVerilogBundle:
    def __init__(self,bundle):
        self.bundle_name = bundle['output']
        self.min_width = bundle['min_width']
        self.elements = []
        self.width = []        
        for ifin in bundle['element']:
            self.elements.append(ifin['input'])
            self.width.append(ifin['width'])
        self.start_pos = [0 for _ in range(len(self.elements))]
        for i in range(len(self.start_pos)):
            if(i!=0):
                self.start_pos[i] = self.width[i-1] + self.start_pos[i-1]
        self.stop_pos = [iwidth+istart_pos-1 for iwidth,istart_pos in zip(self.width,self.start_pos)]
        self.zero_pad_width = 0
        self.bundle_width = 0
        if(self.stop_pos[-1]+1 > self.min_width):
            print("Warning: bundle width exceeds min_width")
            self.bundle_width = self.stop_pos[-1]+1
            self.zero_pad_width = 0
        else:
            self.bundle_width = self.min_width
            self.zero_pad_width = self.min_width - self.stop_pos[-1] - 1
        
        
    def printClass(self):
        print('bundle_name = ',self.bundle_name)
        print('min_width = ',self.min_width)
        print('elements = ',self.elements)
        print('width = ', self.width)
        print('start_pos = ', self.start_pos)
        print('stop_pos = ', self.stop_pos)
        print('zero_pad_width = ', self.zero_pad_width)
        print('bundle_width = ', self.bundle_width)
        
    
