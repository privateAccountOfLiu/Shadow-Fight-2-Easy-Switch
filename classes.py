from values import *
from matrix import Matrix, Vector, solve
from struct import unpack, pack
import os


class Obj:  # .obj模型文件的类
    def __init__(self, file: str):
        with open(file, 'r') as f:
            self.text = f.readlines()
            self.data = {'v ': [], 'f ': [], 'l ': []}
            self.get_data()

    def get_data(self) -> None:  # 筛选出v,f,l数据
        for line in self.text:
            try:
                match line[:2]:
                    case 'v ':
                        self.data['v '].append(list(map(eval, line.split()[1:])))
                    case 'f ' | 'l ':
                        self.data[line[:2]].append(line.split()[1:])
            except Exception as e:
                print(error_mes_2.format(type(e), e))
                continue

    def standardize_0(self) -> None:  # 将多边形切割成三角形，保证每个f数据都为3个点
        for index, i in enumerate(self.data['f ']):
            if len(i) == 3:
                pass
            elif len(i) > 3:
                self.data['f '].extend((i[0], i[j-1], i[j]) for j in range(2, len(i)))
                self.data['f '][index] = [None] * 3
            else:
                raise ValueError(error_mes_1 % i)
        self.clean()

    def standardize_1(self) -> None:   # 处理obj f数据中含有/的情况
        for index, lst in enumerate(self.data['f ']):
            if "/" in lst[0]:
                result = []
                for char in lst:
                    part = [i for i in char.replace('/', ' ').split(' ') if i != ''][0]
                    result.append(part)
                self.data['f '][index] = result
        self.clean()

    def clean(self) -> None:    # 清除f数据列表中的None
        while [None] * 3 in self.data['f ']:
            self.data['f '].remove([None] * 3)

    def rotate(self, method: str = 'xyz') -> None:  # 实现坐标旋转
        dic = {'x': 0, 'y': 1, 'z': 2}
        for i in range(len(self.data['v '])):
            self.data['v '][i] = list(self.data['v '][i][dic[j]] for j in method)

    def zoom(self, vec_c: list) -> list:  # 对模型数据进行缩放
        args = []
        extr = [[min(self.data['v '], key=lambda x: x[i])[i],
                 max(self.data['v '], key=lambda x: x[i])[i]] for i in range(3)]
        for index, i in enumerate(extr):
            args.append(solve(Matrix([i, [1, 1]]).transpose, Vector(vec_c[index])))
        for index, node in enumerate(self.data['v ']):
            self.data['v '][index] = [node[i] * args[i][0] + args[i][1] for i in range(3)]
        return args

    def pre_formate_to_bin(self) -> list:  # 转变一帧的数据为lst
        output, tar = [len(self.data['v ']), ], self.data['v '][-8:]
        del self.data['v '][-8:]
        for index, content in enumerate(tar):
            self.data['v '].insert(19 + index, content)
        output.append([tuple(node) for node in self.data['v ']])
        return output


class Node:  # 在.xml模型中的Node类
    def __init__(self, x, y, z, model_type="weapon", node_id=1):
        self.x, self.y, self.z = x, y, z
        self.id, self.type = node_id, model_type
        self.lcc2, self.lcc3, self.lcc4 = self.count_lcc().transpose[0]
        self.lcc1 = 1 - (self.lcc2 + self.lcc3 + self.lcc4)

    def __add__(self, other):   # 定义加法
        if isinstance(other, Node):
            self.x, self.y, self.z = self.x + other.x, self.y + other.y, self.z + other.z
            return self
        if isinstance(other, int) or isinstance(other, float):
            self.x, self.y, self.z = self.x + other, self.y + other, self.z + other
            return self
        else:
            assert TypeError(error_mes_4)

    def __mul__(self, other):   # 定义乘法
        if isinstance(other, Node):
            return self.x * other.x + self.y * other.y + self.z * other.z
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            self.z *= other
            return self
        else:
            assert TypeError(error_mes_4)

    def __str__(self):  # 定义节点的字符串表现形式
        return node_msg.format(self.type, self.id, self.x, self.y, self.z,
                               *type_child_node[self.type].values(),
                               self.lcc1, self.lcc2, self.lcc3, self.lcc4)

    def count_lcc(self) -> Vector:   # 计算lcc向量
        vector = Vector([self.x, self.y, self.z]) - node_lcc_ori[self.type]
        basis = node_lcc_basis[self.type] - Matrix([i * 3 for i in node_lcc_ori[self.type]])
        lcc = basis.inv * vector
        return lcc


class Triangle:  # 在.xml模型中的三角形Triangle类
    def __init__(self, nodes, model_type='weapon', tri_id=1):
        self.nodes, self.type, self.id = nodes, model_type, tri_id

    def __str__(self):  # 返回triangle数据
        return triangle_msg.format(self.type, *self.nodes, self.id)


class Edge(Triangle):  # 在.xml模型中的连线Edge类
    def __init__(self, nodes, model_type='weapon', edge_id=1, radius=(3, 3), is_draw=False):
        super().__init__(nodes, model_type, edge_id)
        self.radius, self.mode = radius, is_draw

    def __str__(self):  # 返回edge数据
        return edge_msg_0.format(self.type, *self.nodes, self.id, self.radius[0])

    @property
    def draw(self) -> str:  # 返回<Figures>区的edge连线（如果你想将他画出来）
        if self.mode:
            return edge_msg_1.format(self.type, self.id, *self.radius)
        else:
            return ''


class Frame:
    def __init__(self, length: int, points_lst: list):
        self.length = length
        self.points = points_lst

    def shape(self, num: int | float):
        self.points = [tuple([j * num for j in i]) for i in self.points]

    def __str__(self):
        return bin_frame_text.format(self.length, self.points)


class MoveBin:
    def __init__(self, f_bin: str):
        self.bin_file = open(f_bin, 'rb')
        self.bin_data = self.bin_read()
        self.frames_num = len(self.bin_data)

    @staticmethod
    def bin_decode(lst: list) -> list:
        result, i = [], 0
        while i < len(lst):
            if not i:
                i += 5
            else:
                num, frame = lst[i], Frame(lst[i], [])
                i += 4
                for n in range(num):
                    node, coordination = [], []
                    for m in range(12):
                        coordination.append(lst[i])
                        if not (m + 1) % 4:
                            node.append(unpack('f', pack('4B', *coordination))[0])
                            coordination = []
                        i += 1
                    frame.points.append(tuple(node))
                i += 1
                result.append(frame)
        return result

    def bin_read(self) -> list:
        with self.bin_file as f:
            size_file, nums = os.path.getsize(f.name), []
            for i in range(size_file):
                data = unpack('B', f.read(1))
                nums.append(data[0])
            return self.bin_decode(nums)

    def shape(self, num: int | float = 1) -> None:
        for i, frame in enumerate(self.bin_data):
            frame.shape(num)
