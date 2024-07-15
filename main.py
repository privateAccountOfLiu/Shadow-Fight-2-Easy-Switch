from functions import *
from values import *

if __name__ == '__main__':
    try:
        config = get_config()
        obj = edit_obj_data(config)
        if config['is_to_bin_dec']:
            write_bin_dec(obj)
        if config['is_to_xml']:
            write_xml(config, obj)
    except TypeError and ValueError and NameError and SyntaxError as e:
        print(error_mes_0.format(e))
        with open('log.txt', 'a+') as log:
            log.write(str(e) + '\n')
