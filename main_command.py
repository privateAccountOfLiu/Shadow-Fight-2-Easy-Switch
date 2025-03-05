from functions import *
from values import *

if __name__ == '__main__':
    try:
        config = get_config()
        make_dir()
        obj = edit_obj_data(config)
        move_bin = edit_bin_data(config)
        print_lim_and_ask(obj)
        if config.get('is_to_bin_dec', False):
            write_csv_bin(config)
        if config.get('is_to_xml', False):
            write_xml(config, obj)
        if config.get('is_decode_bin', False):
            bin_decode(move_bin)
        if config.get('is_encode_bin', False):
            bin_encode()
    except Exception as e:
        print(error_mes_0.format(type(e), e))
        with open('log.txt', 'a+') as log:
            log.write(str(e) + '\n')
    finally:
        input(common_mes_0)
