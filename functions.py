from classes import *


def get_config(file='config.txt'):  # 获取配置
    with open(file, 'r') as f_in:
        set_config = eval(f_in.read())
    return set_config


def edit_obj_data(set_config, file='input.obj'):    # 对obj获取到的数据进行处理
    obj_p = Obj(file)
    obj_p.standardize()
    obj_p.rotate(set_config['rotate_method'])
    obj_p.zoom([set_config['x'], set_config['y'], set_config['z']])
    return obj_p


def write_bin_dec(obj_p, file='output.bindec'):    # 写入至.bindec文件
    bin_dec = BinDec(file)
    bin_dec.write(obj_p.data['v '])
    bin_dec.close()


def write_xml(set_config, obj_p, file='output.xml'):
    with open(file, 'w') as f_xml:
        f_xml.write(gap_msg_1)
        f_xml.writelines([str(Node(*node, model_type=set_config['type'], node_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['v '])])  # 写入Node数据
        f_xml.write(gap_msg_2)
        f_xml.writelines([str(Edge(node, model_type=set_config['type'], edge_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['l '])])  # 写入Edge数据
        f_xml.write(gap_msg_3)
        f_xml.writelines([Edge(node, model_type=set_config['type'],
                               edge_id=index+1, is_draw=set_config['is_draw_edge']).draw + '\n'
                          for index, node in enumerate(obj_p.data['l '])])  # 写入Edge的<Figures>区数据
        f_xml.writelines([str(Triangle(node, model_type=set_config['type'], tri_id=index+1)) + '\n'
                          for index, node in enumerate(obj_p.data['f '])])  # 写入Triangle数据
        f_xml.write(gap_msg_4)

