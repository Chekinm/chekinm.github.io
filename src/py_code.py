from src.lzw import compress_lzv, decompress_lzv

class comp_gen_obj():

    def __init__(self):
        self.flag = 0
        self.generator = None
        self.dict_to_decode = []
        self.code = []
    
    def reset (self, string):
        self.generator = compress_lzv(string)


class decomp_gen_obj():

    def __init__(self):
        self.dict_to_decode = []
        self.code = []
        self.flag = 0
        self.fin_str = ''
        self.generator = None

    def reset(self, compressed_arr, dict_lzw_inv):
        self.dict_to_decode = dict_lzw_inv
        self.code = compressed_arr
        self.generator = decompress_lzv(compressed_arr, dict_lzw_inv)



res = comp_gen_obj()
res.reset(Element("manual-inp").value)



def compress(res):

    if res.flag == 0:
        res.reset(Element("manual-inp").value)
        res.flag = 1


    Element('compress').element.innerText = "Next step"
    try:
        output = next(res.generator)
        if output[5] == None: 
            Element("manual-write").write(output, append=True)
        else:
            Element("manual-write").write(output, append=True)
            res.dict_to_decode = output[4]
            res.code = output[5]
            Element("dict").element.value = (''.join(str(i) for i in output[4]))
            Element("code").element.value = (''.join(str(i) for i in output[5]))
            Element('compress').innerText = "Try Again"
            Element('decompress').remove_class ('disable')

       
        
    except StopIteration as e:

        Element("manual-write1").element.innerText = "we did it"
        Element('compress').element.innerText = "Try Again"
        button = document.getElementById("compress")
        # button.style.backgroundColor  = 'blue'
        res.flag = 0
       
        document.getElementById('manual-write').innerHTML = ""
            
    return res


decomp = decomp_gen_obj()
decomp.reset(res.code, res.dict_to_decode)
    
def decompress(res):
    if decomp.flag == 0:
        decomp.reset(res.code, res.dict_to_decode)
        decomp.flag = 1
    
    try:
        decomp.fin_str = next(decomp.generator)

        Element("manual-write2").write (decomp.fin_str, append=True)
    
    except StopIteration as e:
        pass    
        
        
    return decomp
    
    
