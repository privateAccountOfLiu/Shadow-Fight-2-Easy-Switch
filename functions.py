from classes import *
import sys
import ast
import os
import csv
import struct


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


def write_csv_bin(set_config: dict, file_name: str = (a := './objs_to_bin/') + (b := 'output.csv')) -> None:
    tar = os.listdir(a)
    if b in tar:
        tar.remove(b)
    with open(file_name, 'w', newline='') as f_decode:
        _writer = csv.writer(f_decode)
        for obj_name in tar:
            if obj_name[-4:] == '.obj':
                obj_p = edit_obj_data(set_config, a + obj_name)
                _writer.writerow(str(_i) for _i in obj_p.pre_formate_to_bin()[1])


def write_xml(set_config: dict, obj_p: Obj, file_name='./xml/output.xml') -> None:
    with open(file_name, 'w') as f_xml:
        f_xml.write(gap_msg_0)
        f_xml.writelines([str(Node(*node, model_type=set_config['type'], node_id=index + set_config['begin_id'])) + '\n'
                          for index, node in enumerate(obj_p.data['v '])])  # 写入Node数据
        f_xml.write(gap_msg_1)
        f_xml.write(gap_msg_2)
        f_xml.writelines([str(Triangle(node, model_type=set_config['type'], tri_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['f '])])  # 写入Triangle数据
        f_xml.write(gap_msg_3)


def bin_decode(obj_bin: MoveBin, file_name: str = './bin/decode_bin.csv') -> None:
    with open(file_name, 'w', newline='') as f:
        _writer = csv.writer(f)
        for i, frame in enumerate(obj_bin.bin_data):
            _writer.writerow(str(_i) for _i in frame.points)


def bin_encode(filein_name: str = './bin/input.csv', fileout_name: str = './bin/encode_bin.bin') -> None:
    _output_lst = b''
    header_struct, frame_header_struct, point_struct, end_byte = (
        struct.Struct('I'), struct.Struct('4B'),
        struct.Struct('<3f'), struct.pack('B', 1))
    with open(filein_name, 'r') as csv_in:
        _reader, data, num = csv.reader(csv_in), [], 0
        for row in _reader:
            data.append([len(row), [ast.literal_eval(_i) for _i in row]])
            num += 1
    with open(fileout_name, 'wb') as bin_f:
        bin_f.write(header_struct.pack(num))
        bin_f.write(end_byte)
        for frame in data:
            bin_f.write(frame_header_struct.pack(frame[0], 0, 0, 0))
            points_data = b''.join(
                point_struct.pack(*point) for point in frame[1]
            )
            bin_f.write(points_data)
            bin_f.write(end_byte)

