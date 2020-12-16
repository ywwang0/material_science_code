from pymatgen.core.surface import Slab, SlabGenerator, generate_all_slabs, Structure, Lattice, ReconstructionGenerator, get_symmetrically_distinct_miller_indices
from pymatgen.core.structure import Structure
from pymatgen.io.vasp.sets import MPStaticSet,MPRelaxSet,MPNonSCFSet,MITMDSet
from pymatgen.ext.matproj import MPRester
from pymatgen.io.vasp.inputs import Poscar
from pymatgen import Structure, Lattice, MPRester, Molecule
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
import os
import shutil

"""
Author: Yaowei Wang

Data:2020-12-16

Function: cleave the surface based on pymatgen

"""

# 导入头文件并且定义文件夹位置
mpr = MPRester('Bw7HdCARiXvzEWJK')
path = '/Users/wangyaowei/Desktop/codes/ml_cathode'

# 读取.vasp文件,此文件需要经过晶格参数优化
struct = Structure.from_file("lamg.POSCAR.vasp")
struct = SpacegroupAnalyzer(struct).get_conventional_standard_structure()
formula = struct.composition.reduced_formula
size = 3
print(f"正在生成{formula}的slab文件，松开表面上下{size}A的原子")

# 建立以化合物名称的名字的文件夹；将.vasp文件移入
os.mkdir(formula)
os.chdir(formula)
ls = get_symmetrically_distinct_miller_indices(struct, 1, return_hkil=False)
for i in ls:
    slab = SlabGenerator(struct, miller_index=i, min_slab_size=25,min_vacuum_size=15.0, lll_reduce=True, center_slab=True)

    for n, slabs in enumerate(slab.get_slabs(bonds=None, ftol=0.1, tol=0.1, max_broken_bonds=0,symmetrize=True,repair=False)):
        slabs.make_supercell([[1,0,0],[0,1,0],[0,0,1]])
        name = str(i).split(',')[0][1]+str(i).split(',')[1][1]+str(i).split(',')[2][1]
        open(formula+'_'+name +'_' + str(n+1) + '.vasp', 'w').write(str(Poscar(slabs)))
        
# 生成vasp输入
for d in os.listdir():
    if d[-5:] == ".vasp" and d[0] != ".":
        dir_name = d.split(".")[0]
        os.makedirs(dir_name)
        shutil.move(d, dir_name)
        os.chdir(dir_name)
        os.rename(d, 'POSCAR')
        
        struct = Structure.from_file('POSCAR')
        vis=MPRelaxSet(struct)
        vis.write_input('.')
        # 根据需求写自己的INCAR文件
        os.remove('INCAR')
        with open ('/Users/wangyaowei/Desktop/codes/opt/INCAR_opt_slab') as f:
            incar = f.readlines()
        with open('INCAR','w') as f:
            for para in incar:
                f.write(para)
                
        # 更改POSCAR，加上“Selective dynamics”，去掉原子位置后的元素符号（否则计算报错），中间原子固定
        with open("POSCAR") as f:
            poscar = f.read().splitlines()
        poscar.insert(7,"Selective dynamics")
        slab_height = eval(poscar[4].split()[-1])
        c = size/slab_height

        atom_pos = []
        poscar_without_element = []
        for p in poscar[9:]:
            poscar_without_element.append(p.split()[0]+" "+p.split()[1]+" "+p.split()[2])
            atom_pos.append(eval(p.split()[2]))
        new_poscar = poscar[:9]+poscar_without_element
        max_pos, min_pos = max(atom_pos), min(atom_pos)

        atom_pos_tf = []
        for pos in new_poscar[9:]:
            p = eval(pos.split()[2])
            if ((max_pos-p) < c) or ((p-min_pos) < c):
                atom_pos_tf.append(pos+" T T T")
            else:
                atom_pos_tf.append(pos+" F F F")

        new_poscar = poscar[:9]+atom_pos_tf

        os.rename('POSCAR', 'POSCAR_ori')
        with open('POSCAR','w') as f:
            for i in new_poscar:
                f.write(i+"\n")               
        os.chdir("../")

a = [i for i in os.listdir() if i[0] != "."]
print(f"{formula}生成文件结束，共有{len(a)}种不同的表面")
print("-"*34)
os.chdir(path)
