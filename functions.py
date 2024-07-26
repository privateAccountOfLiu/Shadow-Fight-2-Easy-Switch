from classes import *
from sys import exit
import os


def notice() -> None:
    print('作者privateAccountOfLiu,本程序未经授权严禁用于商业活动')


def get_config(file='config.txt') -> dict:  # 获取配置
    with open(file, 'r') as f_in:
        set_config = eval(f_in.read())
    return set_config


def make_dir() -> None:
    if not os.path.exists('./bin_dec'):
        os.mkdir('./bin_dec')
    if not os.path.exists('./xml'):
        os.mkdir('./xml')


def edit_obj_data(set_config, file='./xml/input.obj') -> Obj:    # 对obj获取到的数据进行处理
    obj_p = Obj(file)
    obj_p.standardize_0()
    obj_p.standardize_1()
    obj_p.rotate(set_config['rotate_method'])
    if set_config.get('is_zoom', False):
        obj_p.zoom([set_config['x'], set_config['y'], set_config['z']])
    return obj_p


def print_lim_and_ask(obj_p) -> None:
    data_node = obj_p.data['v ']
    for tar in range(3):
        min_data, max_data = min(data_node, key=lambda x: x[tar])[tar], max(data_node, key=lambda x: x[tar])[tar]
        print(round(min_data, 2), round(max_data, 2), sep='\t')
    if input(common_mes_1) != 'y':
        exit(0)


def write_bin_dec_part(obj_p, file='./bin_dec/output.bindec') -> None:    # 写入至.bindec文件
    bin_dec = BinDec(file)
    bin_dec.write(obj_p.data['v '])
    bin_dec.close()


def write_bin_dec(set_config, file=(a := './bin_dec/') + (b := 'output.bindec')) -> None:
    tar = os.listdir(a)
    if b in tar:
        tar.remove(b)
        print(error_mes_3)
    for obj_name in tar:
        obj_p = edit_obj_data(set_config, a + obj_name)
        write_bin_dec_part(obj_p, file)


def write_xml(set_config, obj_p, file='./xml/output.xml') -> None:
    with open(file, 'w') as f_xml:
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
