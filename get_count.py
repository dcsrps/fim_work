from pathlib import Path
import re
import sys

def get_pattern_lengths(i_file):
  ret = {}
  #print(i_file)
  for i, pattern in enumerate([r'length_1', r'length_2', r'length_3', r'length_4']):
    f = open(i_file, 'r')
    strings = re.findall(pattern, f.read())
    #print(pattern)
    #print(strings)
    ret['d'+str(i+1)] = len(strings)
    f.close()
  return ret




path='../patterns/'

output = {}

for filename in Path(path).glob('*/*'):
  fname = str(filename)
  support=fname.split('/')[2].split('_')[1]
  label=fname.split('/')[3]
  try:
    output[support][label] = {}
  except KeyError:
    output[support] = {}
  except:
    print(sys.exc_info())
  
  #if fname.find('others') >= 0:
  #  pass
  #else:
  output[support][label] = get_pattern_lengths(fname)
  


#print(output)
for k,v in output.items():
  print("Support: {}".format(k))
  for ik in v.keys():
    if ik == 'others':
      print(" {}, value: {}".format(ik, sum(v[ik].values())))
    else:
      print(" {}, value: {}, {}".format(ik, sum(v[ik].values()), v[ik] ))
