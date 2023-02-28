def compress_lzv (string_to_compress):
    """this funciton perform LZV compression of the specified string using LZV algorithm.
    it returns compressed string.
    it supposed that string_to_compress is a finite string, not a generator, as we need to create alphabet
    for infinite stream of symbols it's better to use fixed alphabet valerian of the algorithm"""

    # create alphabet, it should include all the simbols from string_to_compress in order of appearance
    # it will be the predicate of the compressed string, as we need it to decode message back
    lzw_dict = {}
    dict_index = 0
    for i in string_to_compress:
        if i not in lzw_dict:
            lzw_dict[i] = dict_index
            yield (lzw_dict[i], i, '', '', None, None)
            dict_index += 1
    dict_to_decode = list(lzw_dict)  # we need a separate copy of the alphabet to send, better to have it as list


    # algrith LZW
    compressed_string = []  # will be a list of decimal numbers calculated using LZW method
    current_sub_string = ''
    code_to_write = None

    for i in string_to_compress:
        current_sub_string += i
        if current_sub_string in lzw_dict:
            code_to_write = lzw_dict[current_sub_string]
        else:
            compressed_string.append(code_to_write)
            lzw_dict[current_sub_string] = dict_index
            yield (dict_index, current_sub_string, code_to_write, ','.join(str(i) for i in compressed_string),None,None)
            dict_index += 1
            current_sub_string = i
            code_to_write = lzw_dict[current_sub_string]
    compressed_string.append(code_to_write)   # add last portion of information
    yield (dict_index, current_sub_string, code_to_write, ','.join(str(i) for i in compressed_string),dict_to_decode,compressed_string)


    #return compress_lzv
    #return ''.join(dict_to_decode), ''.join(str(i) for i in compressed_string)

  
def decompress_lzv (compressed_arr, dict_lzw_inv):
    """this function perform decompression of the specified compressed package using LZV algorithm"""

    dcmp_string = ''
    right_index = 0  # index on decompressed string
    left_index = 0   # lagging index on decompressed string to restore dictionary
    i = 0            # index on compressed array
    current_sub_string = ''

    while i < len(compressed_arr):
        if left_index == right_index:
            if compressed_arr[i] < len(dict_lzw_inv):
                dcmp_string += dict_lzw_inv[compressed_arr[i]]
                right_index = len(dcmp_string)
                i += 1
            else:  # worst case, we don't have needed part of dict yet, but we know why, and can reconstruct it
                dcmp_string += dict_lzw_inv[compressed_arr[i - 1]] + dict_lzw_inv[compressed_arr[i - 1]][0]
                right_index = len(dcmp_string)
                i += 1
        current_sub_string += dcmp_string[left_index]
        if current_sub_string not in dict_lzw_inv:
            dict_lzw_inv.append(current_sub_string)
            current_sub_string = dcmp_string[left_index]
        left_index += 1
        yield (len(dict_lzw_inv), dict_lzw_inv[-1], dcmp_string, current_sub_string )
    yield dcmp_string
