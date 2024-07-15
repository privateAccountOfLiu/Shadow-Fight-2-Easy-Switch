from matrix import Matrix, Vector

gap_msg_1 = '<Scene>\n<Nodes>\n'
gap_msg_2 = '</Nodes>\n<Edges>\n'
gap_msg_3 = '</Edges>\n<Figures>\n'
gap_msg_4 = '</Figures>\n</Scene>\n'

error_mes_0 = 'something_wrong:{}'
error_mes_1 = 'the iter length must >= 3 but length %d'

node_msg = ('<MN{}{} Type="MacroNode" '
            'X="{:.5f}" Y="{:.5f}" Z="{:.5f}" Fixed="0" '
            'Visible="1"  NodesCount="4" '
            'ChildNode1="{}" ChildNode2="{}" ChildNode3="{}" ChildNode4="{}" '
            'LCC1="{:.5f}" LCC2="{:.5f}" LCC3="{:.5f}" LCC4="{:.5f}" />')

edge_msg_0 = ('<MN_Edge-{0}{3} Type="Edge"  Length="1"  WithSign="0"  Fixed="0"  Visible="1"  Selectable="1"  '
              'Node1="MN{0}{1}"  Node2="MN{0}{2}"  Force="100"  SubNodesCount="0"  '
              'End1="MN{0}{1}"  End2="MN{0}{2}" '
              'Radius="{4}" Margin1="0" Margin2="0"/>')
edge_msg_1 = ('<MN_capsule{1} Type="Capsule"  Edge="MN_Edge-{0}{1}"  '
              'Radius1="{2}"  Radius2="{3}"  Margin1="0"  Margin2="0" />')

triangle_msg = '<Triangle{4} Type="Triangle" DoubleSided="-1" Node1="MN{0}{1}" Node2="MN{0}{2}" Node3="MN{0}{3}"/>'

type_child_node = {"weapon": {"ChildNode1": "Weapon-Node4_1",
                              "ChildNode2": "Weapon-Node3_1",
                              "ChildNode3": "Weapon-Node2_1",
                              "ChildNode4": "Weapon-Node1_1"},
                   "helm": {"ChildNode1": "NHeadS_1",
                            "ChildNode2": "NHeadS_2",
                            "ChildNode3": "NTop",
                            "ChildNode4": "NHeadF"},
                   "ranged": {"ChildNode1": "Weapon-Node4_1",
                              "ChildNode2": "Weapon-Node3_1",
                              "ChildNode3": "Weapon-Node2_1",
                              "ChildNode4": "Weapon-Node1_1"}
                   }

node_msgs = {"Weapon-Node4_1": (78.1888046264648, 204.833297729492, 49.7735557556152),
             "Weapon-Node3_1": (22.1369762420654, 196.383895874023, 92.044059753418),
             "Weapon-Node2_1": (29.3087463378906, 214.682815551758, 46.0688629150391),
             "Weapon-Node1_1": (44.7105293273926, 305.636322021484, 84.6726913452148),
             "NHeadS_1": (-10.0914621353149, 261.223541259766, 6.32387971878052),
             "NHeadS_2": (-32.0835800170898, 261.797760009766, 6.20270729064941),
             "NTop": (-20.5197906494141, 283.477600097656, 7.33019399642944),
             "NHeadF": (-21.1619281768799, 260.979034423828, 17.2502841949463),
             "Ranged-Node4_1": (78.1888046264648, 204.833297729492, 49.7735557556152),
             "Ranged-Node3_1": (22.1369762420654, 196.383895874023, 92.044059753418),
             "Ranged-Node2_1": (29.3087463378906, 214.682815551758, 46.0688629150391),
             "Ranged-Node1_1": (44.7105293273926, 305.636322021484, 84.6726913452148)
             }

node_lcc_basis = {"weapon": Matrix([[-100, -150, -150],
                                   [150, 150, 250],
                                   [0, 0, 0]]),
                  "helm": Matrix([[11.4526, 0.5962, 0.3581],
                                 [213.3688, 235.4395, 213.3591],
                                 [54.4456, 54.3514, 43.5192]]),
                  "ranged": Matrix([[-100, -150, -150],
                                   [150, 150, 250],
                                   [0, 0, 0]])}
node_lcc_ori = {"weapon": Vector([-150, 150, -50]),
                "helm": Vector([-10.55, 213.5138, 54.5787]),
                "ranged": Vector([-150, 150, -50])}
