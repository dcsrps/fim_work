from pyfpgrowth_updated import find_frequent_patterns
import pandas as pd
import argparse
import os

def fill_the_patterns(i_itemset, i_cols):
    ret_patterns= []
    template_pattern = {}
    for pattern in i_itemset: #self._final_itemset[i_flow_dir]:
            
        template_pattern = {}
        for i in i_cols:
            template_pattern[i]='  *  '

        for value in pattern:
            val = value.split('_')
            if val[0] in i_cols:
                template_pattern[val[0]] = val[1]
                    
        #print(pattern, template_pattern)
        ret_patterns.append(template_pattern.values())

    return template_pattern.keys(),ret_patterns

 
class itemset_process():
    def __init__(self, i_input_file, i_pattern_last,  i_pattern_start = 1, i_support = 2):
        self._i_file = i_input_file
        self._i_cols = None
        self._i_data_col = None
        self._support = i_support
        
    def run(self):
        l_df = pd.read_csv(self._i_file, dtype=str)
        self._i_cols = l_df.columns.tolist()
        
        self._i_data_col  = self._i_cols.copy()
        self._i_data_col.remove('dir')
        #self._i_data_col.remove('label')
          
        for col in self._i_data_col:
            l_df[col] = l_df[col].apply(lambda x: col+'_'+str(x))

        for flow_dir in ['0', '1']:
            print('Direction: {}'.format(flow_dir))
            df_entries = l_df[l_df['dir']==flow_dir][self._i_data_col]#.values.tolist()
            #print(df_entries, len(df_entries))
            if len(df_entries) > 0:
                self.run_FIM_fpg(df_entries, flow_dir) 
    

    def run_FIM_fpg(self, i_entries, i_flow_dir):
        some_output = {}
        
        l_items = find_frequent_patterns(i_entries.values.tolist(), self._support)
        for i in l_items.keys():
            try:
                some_output[len(i)].append(i)
            except:
                some_output[len(i)] = [i]
       
        for k in some_output.keys():
          print('Itemset length: {}, count: {}'.format(k, len(some_output[k])))
          hdr, vals = fill_the_patterns(some_output[k], self._i_data_col)
          df_w = pd.DataFrame(vals, columns=hdr)
          l_dir = os.path.join(self._i_file.split('/')[1].split('.')[0], 'support_'+str(self._support), 'length_'+str(k))

          if not os.path.exists(l_dir):
                os.makedirs(l_dir)

          file_to_write = os.path.join(l_dir, 'dir_'+str(i_flow_dir))
          df_w.to_csv(file_to_write, index=False, mode='w', sep='\t') 

parser = argparse.ArgumentParser(description='Alert processing using FIM.')
parser.add_argument('-f', action="store", dest="file_name", type=str)
parser.add_argument('-s', action="store", dest="max_support", type=int)
parser.add_argument('-l', action="store", dest="max_len", type=int)

inp = parser.parse_args()


for support in range(2, inp.max_support+2, 2):
    print('Running with support {}'.format(support))
    inst = itemset_process(inp.file_name, i_pattern_last = inp.max_len, i_support=support)
    inst.run()
