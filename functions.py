from classes import *
import sys
import importlib.util
import os


def get_dir(path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, path)


def get_config(file: str = 'config.txt') -> dict:  # 获取配置
    with open(file, 'r') as f_in:
        set_config = eval(f_in.read())
    return set_config


def make_dir() -> None:
    _dirs = ['./bin', './objs_to_bin', './xml']
    for d in _dirs:
        if not os.path.exists(d):
            os.mkdir(d)


def edit_obj_data(set_config: dict, file_name='./xml/input.obj') -> Obj:    # 对obj获取到的数据进行处理
    obj_p = Obj(file_name)
    obj_p.standardize_0()
    obj_p.standardize_1()
    obj_p.rotate(set_config['rotate_method'])
    if set_config.get('is_zoom', False):
        obj_p.zoom([set_config['x'], set_config['y'], set_config['z']])
    return obj_p


def edit_bin_data(set_config: dict, file_name='./bin/input.bin') -> MoveBin:
    obj_bin = MoveBin(file_name)
    obj_bin.shape(set_config['bin_shape_arg'])
    return obj_bin


def print_lim_and_ask(obj_p: Obj) -> None:
    data_node = obj_p.data['v ']
    for tar in range(3):
        min_data, max_data = min(data_node, key=lambda x: x[tar])[tar], max(data_node, key=lambda x: x[tar])[tar]
        print(round(min_data, 2), round(max_data, 2), sep='\t')
    if input(common_mes_1) != 'y':
        exit(0)


def write_py_bin(set_config: dict, file_name: str = (a := './objs_to_bin/') + (b := 'output.py')) -> None:
    tar = os.listdir(a)
    if b in tar:
        tar.remove(b)
        print(error_mes_3)
    with open(file_name, 'w') as f_decode:
        f_decode.write(bin_head_text.format(len(tar)))
        f_decode.write('fdata = [\n')
        for obj_name in tar:
            obj_p = edit_obj_data(set_config, a + obj_name)
            f_decode.write(str(obj_p.pre_formate_to_bin()) + ',\n')
        f_decode.write(']')


def write_xml(set_config: dict, obj_p: Obj, file_name='./xml/output.xml') -> None:
    with open(file_name, 'w') as f_xml:
        f_xml.write(gap_msg_0)
        f_xml.writelines([str(Node(*node, model_type=set_config['type'], node_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['v '])])  # 写入Node数据
        f_xml.write(gap_msg_1)
        f_xml.writelines([str(Edge(node, model_type=set_config['type'], edge_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['l '])])  # 写入Edge数据
        f_xml.write(gap_msg_2)
        f_xml.writelines([Edge(node, model_type=set_config['type'],
                               edge_id=index+1, is_draw=set_config.get('is_draw_edge', False)).draw + '\n'
                          for index, node in enumerate(obj_p.data['l '])])  # 写入Edge的<Figures>区数据
        f_xml.writelines([str(Triangle(node, model_type=set_config['type'], tri_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['f '])])  # 写入Triangle数据
        f_xml.write(gap_msg_3)


def bin_decode(obj_bin: MoveBin, file_name: str = './bin/decode_bin.py') -> None:
    with open(file_name, 'w') as f:
        f.write(bin_head_text.format(obj_bin.frames_num))
        str_data = f'fdata = [\n\t\t'
        for i, frame in enumerate(obj_bin.bin_data):
            str_data += str(frame) + ', \n\t\t'
        str_data += ']'
        f.write(str_data)


def bin_encode(filein_name: str = './bin/input.bin', fileout_name: str = './bin/encode_bin.bin') -> None:
    spec = importlib.util.spec_from_file_location("filein", filein_name)
    filein = importlib.util.module_from_spec(spec)
    sys.modules["filein"] = filein
    spec.loader.exec_module(filein)
    data, num = filein.fdata, filein.the_num_of_frames
    with open(fileout_name, 'wb') as bin_f:
        bin_f.write(pack('5B', num, 0, 0, 0, 1))
        for frame in data:
            bin_f.write(pack('4B', frame[0], 0, 0, 0))
            for point in frame[1]:
                bin_f.write(pack('<3f', *point))
            bin_f.write(pack('B', 1))
