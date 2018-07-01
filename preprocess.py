
_STATUS = {
    'S': '0', # single
    'B': '1', # begin
    'M': '2', # middle
    'E': '3'  # end
}

def load_data(fname, seq_char='  '):
    with open(fname, 'r', encoding='utf-8') as f:
        for l in f.readlines():
            l = l.strip()
            l = l.split(seq_char)
            yield l

def label_data(data):
    def labeling(line):
        res = ''
        for s in line:
            lens = len(s)
            if lens == 1:
                res += _STATUS['S']
            elif lens == 2:
                res += (_STATUS['B'] + _STATUS['E'])
            else:
                res += (_STATUS['B'] + (_STATUS['M'] * (lens-2)) +  _STATUS['E'])
        return res
    for line in data:
        yield labeling(line)
    
def segment(line, sentence):
    
    lens = len(sentence)
    tmp = ''
    res = []
    i = 0
    while i < lens:
        if line[i] == '0':
            res.append(sentence[i])
            tmp = ''
        elif line[i] != '3':            
            while i < lens:
                tmp += sentence[i]
                if line[i] == '3':
                    res.append(tmp)
                    tmp = ''
                    break
                i += 1
        else:
            tmp += sentence[i]
            res.append(tmp)
            tmp = ''
        i+=1
    res.append(tmp)
    return ' '.join(res)
    
def save_data(data, fname):
    with open(fname, 'w', encoding='utf-8') as f:
        for line in data:
            f.write(line + '\n')

