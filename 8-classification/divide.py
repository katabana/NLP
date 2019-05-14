import os
import regex

    
def main():
    dir_path = 'ustawy'
    dir_change = 'zmiana'
    dir_other = 'inne'
    os.makedirs(dir_path, exist_ok=True) 
    os.makedirs(dir_change, exist_ok=True) 
    os.makedirs(dir_other, exist_ok=True) 

    for filename in os.listdir(dir_path):
        name = filename[:-4]
        with open(dir_path + '/' + filename, 'r') as bill_file:
            bill = bill_file.read() 
            bill = regex.sub(r'[\t\p{Zs}\xA0\n][\n]+', '', bill) 
            a = regex.findall(r'(o[\t\p{Zs}\xA0\n]+zmianie[\t\p{Zs}\xA0\n]+(ustaw|niektórych))', bill)  # find text that may contain more types of white spaces
            content = regex.findall(r'\X*?(Art.\X*)', bill)

            if len(content) > 0:
                content = content[0]

                if len(a) > 0:
                    with open('{}/{}'.format(dir_change, filename), 'w+') as f: 
                        f.write(content)
                else:
                    with open('{}/{}'.format(dir_other, filename), 'w+') as f: 
                        f.write(content)

main()

