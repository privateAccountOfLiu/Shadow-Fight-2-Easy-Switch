from functions import *
from values import *

if __name__ == '__main__':
    try:
        config = get_config()
        make_dir()
        obj = edit_obj_data(config)
        if config.get('is_to_bin_dec', False):
            write_bin_dec(config)
        if config.get('is_to_xml', False):
            write_xml(config, obj)
    except Exception as e:
        print(error_mes_0.format(type(e), e))
        with open('log.txt', 'a+') as log:
            log.write(str(e) + '\n')
    finally:
        input(common_mes)
