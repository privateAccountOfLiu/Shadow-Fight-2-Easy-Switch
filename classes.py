from values import *
from matrix import Matrix, Vector, solve


class Obj:
    def __init__(self, file: str):
        with open(file, 'r') as f:
            self.text = f.readlines()
            self.data = {'v ': [], 'f ': [], 'l ': []}
            self.get_data()

    def get_data(self):  # 筛选出v,f,l数据
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

    def standardize_0(self):  # 将多边形切割成三角形，保证每个f数据都为3个点
        for index, i in enumerate(self.data['f ']):
            if len(i) == 3:
                pass
            elif len(i) > 3:
                self.data['f '].extend((i[0], i[j-1], i[j]) for j in range(2, len(i)))
                self.data['f '][index] = [None] * 3
            else:
                raise ValueError(error_mes_1 % i)
        self.clean()

    def standardize_1(self):   # 处理obj f数据中含有/的情况
        for index, lst in enumerate(self.data['f ']):
            if "/" in lst[0]:
                result = []
                for char in lst:
                    part = [i for i in char.replace('/', ' ').split(' ') if i != '']
                    result.append(part)
                self.data['f '].extend(Matrix(result).transpose.value)
                self.data['f '][index] = [None] * 3
        self.clean()

    def clean(self):    # 清除f数据列表中的None
        while [None] * 3 in self.data['f ']:
            self.data['f '].remove([None] * 3)

    def rotate(self, method='xyz'):  # 实现坐标旋转
        dic = {'x': 0, 'y': 1, 'z': 2}
        for i in range(len(self.data['v '])):
            self.data['v '][i] = list(self.data['v '][i][dic[j]] for j in method)

    def zoom(self, vec_c):  # 对模型数据进行缩放
        args = []
        extr = [[min(self.data['v '], key=lambda x: x[i])[i],
                 max(self.data['v '], key=lambda x: x[i])[i]] for i in range(3)]
        for index, i in enumerate(extr):
            args.append(solve(Matrix([i, [1, 1]]).transpose, Vector(vec_c[index])))
        for index, node in enumerate(self.data['v ']):
            self.data['v '][index] = [node[i] * args[i][0] + args[i][1] for i in range(3)]
        return args


class Node:
    def __init__(self, x, y, z, model_type="weapon", node_id=1):
        self.x, self.y, self.z = x, y, z
        self.id, self.type = node_id, model_type
        self.lcc2, self.lcc3, self.lcc4 = self.count_lcc().transpose[0]
        self.lcc1 = 1 - (self.lcc2 + self.lcc3 + self.lcc4)

    def __add__(self, other):   # 定义加法
        if isinstance(other, Node):
            self.x, self.y, self.z = self.x + other.x, self.y + other.y, self.z + other.z
        if isinstance(other, int) or isinstance(other, float):
            self.x, self.y, self.z = self.x + other, self.y + other, self.z + other
        return self

    def __mul__(self, other):   # 定义乘法
        if isinstance(other, Node):
            return self.x*other.x+self.y*other.y+self.z*other.z
        if isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            self.z *= other
            return self

    def __str__(self):  # 定义节点的字符串表现形式
        return node_msg.format(self.type, self.id, self.x, self.y, self.z,
                               *type_child_node[self.type].values(),
                               self.lcc1, self.lcc2, self.lcc3, self.lcc4)

    def count_lcc(self):   # 计算lcc向量
        vector = Vector([self.x, self.y, self.z]) - node_lcc_ori[self.type]
        basis = node_lcc_basis[self.type] - Matrix([i * 3 for i in node_lcc_ori[self.type]])
        lcc = basis.inv * vector
        return lcc


class Triangle:
    def __init__(self, nodes, model_type='weapon', tri_id=1):
        self.nodes, self.type, self.id = nodes, model_type, tri_id

    def __str__(self):  # 返回triangle数据
        return triangle_msg.format(self.type, *self.nodes, self.id)


class Edge(Triangle):
    def __init__(self, nodes, model_type='weapon', edge_id=1, radius=(3, 3), is_draw=False):
        super().__init__(nodes, model_type, edge_id)
        self.radius, self.mode = radius, is_draw

    def __str__(self):  # 返回edge数据
        return edge_msg_0.format(self.type, *self.nodes, self.id, self.radius[0])

    @property
    def draw(self):  # 返回<Figures>区的edge连线（如果你想将他画出来）
        if self.mode:
            return edge_msg_1.format(self.type, self.id, *self.radius)
        else:
            return ''


class BinDec:
    def __init__(self, file: str):
        self.file = open(file, 'a+')

    def write(self, data: list):  # 写入一帧
        string = f'[{len(data)}]'
        for node in data:
            string += '{' + '{},{},{}'.format(*node) + '}'
        string += 'END\n'
        self.file.write(string)

    def close(self):
        self.file.close()
