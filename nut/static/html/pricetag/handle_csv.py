import json
import io

def handle_file(filename=None):
    if filename is None:
        raise  Exception('can not find file None')

    product_list = []
    with open(filename, 'r') as fd:
        lines = fd.readlines()
        for line in lines[2:]:

            items = line.split(',')
            if len(items[9]) < 4 :
                continue
            product_list.append([
                items[1],
                items[2],
                items[5],
                items[7],
                items[9]
            ])




    with open('data.js', 'w') as wfd:
        wfd.write('var tag_list = [')
        for product in product_list:
            json.dump(product, wfd ,indent=4, separators=(',', ': '))
            wfd.write(',')
        wfd.write('];')


    print 'done'




if __name__ == '__main__':
    handle_file('new_data.csv')