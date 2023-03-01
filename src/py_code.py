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


class comp_output_table:

    def __init__(self, table_ind=0):
        self.table_ind = table_ind
        
    
    def reset(self, table_ind=0):
        self.table_ind = table_ind






def compress(res):  # action on click  button in compress

    if res.flag == 0:
        res.reset(Element("manual-inp").value)
        res.flag = 1
        output_table_counter.reset()
        document.getElementById('compress-output').textContent = ''  # clear output for new string compression
        

    Element('compress').element.innerText = "Next step"
    try:
        output = next(res.generator)
        if output[6] == None: 
            print_comp_table_row(output, output_table_counter)
            
        else:
            print_last_Strings(output, output_table_counter)
           # Element("manual-write").write(output, append=True)
            res.dict_to_decode = output[5]
            res.code = output[6]
            if not Element("override-inp").element.checked:
                Element("dict").element.value = (','.join(str(i) for i in output[5]))
                Element("code").element.value = (','.join(str(i) for i in output[6]))
                Element('decompress').remove_class ('disable')
            
    except StopIteration as e:
        Element("manual-write").write('we did it', append=True)
        #Element("manual-write").element.innerText = "we did it"
        Element('compress').element.innerText = "We did it! Try Again"
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




def print_comp_table_row(out_str, output_table_counter):
    """construct nice css formated outout for our function
    out_srt indexes
    [0] current symbol
    [1] current substring
    [2] code to append
    [3] new dict record
    [4] it's code
    [5] short dict to decompress appears only in the end. type - list
    [6] compressed string code appears only in the end,  type - list """
    
    ind = output_table_counter.table_ind

    for i in range(ind, ind + 5):
        td = document.createElement('div')
        document.getElementById("compress-output").appendChild(td)
        td.id = "tc-"+str(i)
        td.classList.add("table-cell")
        Element("tc-"+str(i)).write ('-' if out_str[i%5]==None else out_str[i%5])

    output_table_counter.reset(ind+5) 


def print_last_Strings(out_str, output_table_counter):

    ind = output_table_counter.table_ind
    
    td = document.createElement('div')
    document.getElementById("compress-output").appendChild(td)
    td.id = "tc-"+str(ind)
    td.classList.add("table-cell-last")
    Element("tc-"+str(ind)).write ("Dictinary to decode: " + ','.join(str(i) for i in out_str[5]))

    td = document.createElement('div')
    document.getElementById("compress-output").appendChild(td)
    td.id = "tc-"+str(ind+1)
    td.classList.add("table-cell-last")
    Element("tc-"+str(ind+1)).write ("Encoded string:" + ','.join(str(i) for i in out_str[6]))

    output_table_counter.reset(ind+2) 



    



    

# don't actally do anyting without action on page. Just initialize some objects in case somebody thouch buutons

# default object for dial with  compress 
res = comp_gen_obj()
res.reset(Element("manual-inp").value)


# default object to dial with decompress
decomp = decomp_gen_obj()
decomp.reset(res.code, res.dict_to_decode)

# counters for print functions
output_table_counter = comp_output_table(0)  


