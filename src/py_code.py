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
        self.flag = 0


class decomp_gen_obj():

    def __init__(self):
        self.dict_to_decode = []
        self.code = []
        self.flag = 0
        self.fin_str = ''
        self.generator = None

    def reset(self, compressed_arr, dict_lzw_inv):
        self.flag = 0
        self.dict_to_decode = dict_lzw_inv
        self.code = compressed_arr
        self.generator = decompress_lzw(compressed_arr, dict_lzw_inv)


class comp_output_table:

    def __init__(self, table_ind=0, parent=''):
        self.table_ind = table_ind
        self.parent = parent
        
    
    def reset(self, table_ind=0, parent=''):
        self.table_ind = table_ind
        self.parent = parent

class decomp_output_table:

    def __init__(self, table_ind=0, parent=''):
        self.table_ind = table_ind
        self.parent = parent
        
    
    def reset(self, table_ind=0, parent=''):
        self.table_ind = table_ind
        self.parent = parent


def compress(res):  
    """perform action associated with button in compress section
    it calls compress generator from lzw module and give result to the print table function"""

    if res.flag == 0:
        res.reset(Element("manual-inp").value)
        res.flag = 1
        output_table_counter.reset(parent="compress-output")
        document.getElementById('compress-output').textContent = ''  # clear output table if we want to compres something new
        

    Element('compress').element.innerText = "Next step"
    try:
        output = next(res.generator)
        if output[6] == None: 
            print_comp_table_row(output, output_table_counter)
            
        else:
            print_last_strings(output, output_table_counter)
           # Element("manual-write").write(output, append=True)
            res.dict_to_decode = output[5]
            res.code = output[6]
            if not Element("override-inp").element.checked:
                Element("dict").element.value = (','.join(str(i) for i in output[5]))
                Element("code").element.value = (','.join(str(i) for i in output[6]))
                Element('decompress').remove_class ('disable')
            
    except StopIteration as e:

        Element('compress').element.innerText = "We did it! Try Again"
        res.flag = 0 
           
    return res

    
def decompress(res):     
    """perform action associated with button in decompress section
    it calls decompress generator from lzw module and give result to the print table function
    
    all action performas on click decompress button
    
    results depends dependind on  ovveride-inp checkbox state."""

    if decomp.flag == 0:    # need this to reloop action, without refreshing page  
        if Element("override-inp").element.checked:   # check if we are in manual mode
            inp_code = [int(k) for k in Element("code").value.split(',')]   # parse input string
            inp_dict = Element("dict").value.split(',')   
            decomp.reset(inp_code, inp_dict)  #initilize with inputed values
        
        else:
            decomp.reset(res.code.copy(), res.dict_to_decode.copy())   # get values from compressed pricedure
        decomp.flag = 1
        document.getElementById('decompress-output').textContent = ''  # clear output table
        decomp_table_counter.reset(0, 'decompress-output')
    try: 
        decomp.out_str = next(decomp.generator)
        if decomp.out_str[2] != None:             # check if we are not on the last step                
            print_comp_table_row(decomp.out_str, decomp_table_counter)
        else:
            print_last_decomp_output(decomp.out_str, decomp_table_counter)

    except StopIteration as e:
        decomp.flag = 0         
    return decomp


def check_box_action():
    """disable/enable input contols in decompress section"""

    if Element("override-inp").element.checked:
        Element("dict").remove_class ('disable')
        Element("code").remove_class ('disable')
        Element("decompress").remove_class ('disable')
        
    else:
        Element("dict").add_class ('disable')
        Element("code").add_class ('disable')
        Element("decompress").add_class ('disable')


def print_comp_table_row(out_str, table_counter):
    """construct nice css formated outout for our function
    out_srt indexes
    [0] current symbol
    [1] current substring
    [2] code to append
    [3] new dict record
    [4] it's code
    [5] short dict to decompress appears only in the end. type - list
    [6] compressed string code appears only in the end,  type - list """
    
    ind = table_counter.table_ind
    parent = table_counter.parent

    for i in range(ind, ind + 5):
        td = document.createElement('div')
        document.getElementById(parent).appendChild(td)
        td.id = "tc-" + parent + str(i)
        td.classList.add("table-cell")
        Element("tc-" + parent + str(i)).write ('-' if out_str[i % 5] == None else out_str[i % 5])

    table_counter.reset(ind + 5, parent) 


def print_last_strings(out_str, output_table_counter):
    """"print resulting tow string in compress section"""

    ind = output_table_counter.table_ind
    parent = output_table_counter.parent
    
    td = document.createElement('div')
    document.getElementById(parent).appendChild(td)
    td.id = "tc-"+str(ind)
    td.classList.add("table-cell-last")
    Element("tc-"+str(ind)).write ("Dictinary to decode: " + ','.join(str(i) for i in out_str[5]))

    td = document.createElement('div')
    document.getElementById(parent).appendChild(td)
    td.id = "tc-"+str(ind+1)
    td.classList.add("table-cell-last")
    Element("tc-"+str(ind+1)).write ("Encoded string: " + ','.join(str(i) for i in out_str[6]))

    output_table_counter.reset(ind+2) 


def print_last_decomp_output(out_str, table_counter):
    """print last string in decompres section"""
    
    ind = table_counter.table_ind
    parent = table_counter.parent
    
    td = document.createElement('div')
    document.getElementById(parent).appendChild(td)
    td.id = "tc-"+parent+str(ind)
    td.classList.add("table-cell-last")
    Element("tc-"+parent+str(ind)).write ("Original string: " + out_str[0])

    output_table_counter.reset(ind+1) 







    



    

# don't actally do anyting without action on page. Just initialize some objects in case somebody thouch buutons

# default object for dial with  compress 
res = comp_gen_obj()
res.reset(Element("manual-inp").value)


# default object to dial with decompress
decomp = decomp_gen_obj()
decomp.reset(res.code, res.dict_to_decode)

# counters for print functions
output_table_counter = comp_output_table(0, 'compress-output')

# counters for print functions
decomp_table_counter = decomp_output_table(0, 'decompress-output')  


