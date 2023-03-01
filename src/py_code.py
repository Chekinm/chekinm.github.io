from src.lzw import compress_lzw, decompress_lzw
from js import document


# class definitions.

class comp_gen_obj():

    def __init__(self):
        self.flag = 0
        self.generator = None
        self.dict_to_decode = []
        self.code = []
    
    def reset (self, string):
        self.generator = compress_lzw(string)


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
        self.generator = decompress_lzw(compressed_arr, dict_lzw_inv)




def compress(res):  # action on click  button in compress

    if res.flag == 0:
        res.reset(Element("manual-inp").value)
        res.flag = 1
        Element('manual-write').element.innerHTML = ""  # clear output for new string compression
        

    Element('compress').element.innerText = "Next step"
    try:
        output = next(res.generator)
        if output[5] == None: 
            Element("manual-write").write(output, append=True)
        else:
            Element("manual-write").write(output, append=True)
            res.dict_to_decode = output[4]
            res.code = output[5]
            if not Element("override-inp").element.checked:
                Element("dict").element.value = (','.join(str(i) for i in output[4]))
                Element("code").element.value = (','.join(str(i) for i in output[5]))
                Element('decompress').remove_class ('disable')
            
    except StopIteration as e:
        Element("manual-write").write('we did it', append=True)
        #Element("manual-write").element.innerText = "we did it"
        Element('compress').element.innerText = "Try Again"
        res.flag = 0 
           
    return res

    
def decompress(res):   # action on click button in decompress
    """all action performas on click decompress button
    dependind on  ovveride-inp checkbox state."""

    if decomp.flag == 0:  # need this to reloop action, without refreshing page  
        if Element("override-inp").element.checked:   # check if we are in manual mode
            cd = Element("code").value
            Element("manual-write2").write (cd, append=True)
            inp_code = [int(k) for k in Element("code").value.split(',')]   # process input string
            inp_dict = Element("dict").value.split(',')   
            decomp.reset(inp_code, inp_dict,)  #initilize with inputed values
        
        else:
            decomp.reset(res.code.copy(), res.dict_to_decode.copy())   # get values from compressed pricedure
        decomp.flag = 1
        Element('manual-write2').element.innerHTML = ""  # clear output table
    
    try: 
        decomp.out_str = next(decomp.generator)
        Element("manual-write2").write (decomp.out_str, append=True)
        
    except StopIteration as e:
        Element("manual-write2").write ('Here you are!', append=True)
        decomp.flag = 0   
      
    return decomp


def check_box_action():
    if Element("override-inp").element.checked:
        Element("dict").remove_class ('disable')
        Element("code").remove_class ('disable')
        Element("decompress").remove_class ('disable')
        

    else:
        Element("dict").add_class ('disable')
        Element("code").add_class ('disable')
        Element("decompress").add_class ('disable')

def print_table_row(out_str):
    """construct nice css formated outout for our function"""
    out_str = (3, 'bb', 1, '0,1', None, None)
    step_num = out_str[1]
    curr_sub



    

# don't actally do without action on page. Just initialize objects in case somebody thouch buutons

# default object for dial with  compress 
res = comp_gen_obj()
res.reset(Element("manual-inp").value)


# default object to dial with decompress
decomp = decomp_gen_obj()
decomp.reset(res.code, res.dict_to_decode)



