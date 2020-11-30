# 从pymatgen取出一共102个元素
from pymatgen.core.periodic_table import Element
ele = {}
for i in range(1,103):
    ele[str(i)] = str(Element.from_Z(i))
# 去掉惰性气体
for noble in [2,10,18,36,54,86]:
    del ele[str(noble)]
