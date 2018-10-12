# -*- coding: utf-8 -*-
import json

def stat_timeline_memory(json_file_name):
    with open(json_file_name,'r') as trace_file:
        parsed_json = json.load(trace_file)
        count = 0
        for e in parsed_json['traceEvents']:
            if e['ph'] == "O" and e['cat'] == "Tensor" and e['pid'] == 4:
                tensor_desc = e['args']['snapshot']['tensor_description']
                alloc_bytes = 'allocated_bytes: '
                alloc_name = 'allocator_name: '
                pos = tensor_desc.find(alloc_bytes)
                if pos >= 0:
                    alloc_bytes_val = tensor_desc[pos + len(alloc_bytes):]
                    alloc_bytes_val = alloc_bytes_val[:alloc_bytes_val.find('\n')]
                    count += int(alloc_bytes_val)
                    '''
                    pos = tensor_desc.find(alloc_name)
                    if pos >= 0:
                        alloc_name_val = tensor_desc[pos + len(alloc_name):]
                        alloc_name_val = alloc_name_val[:alloc_name_val.find('\n')]
                        print(alloc_name_val)
                    '''
        return count
       
