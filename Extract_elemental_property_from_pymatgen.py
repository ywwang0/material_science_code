# composition.py, periodic_table.py
import pandas as pd
import pymatgen as pmg

df = pd.read_excel('raw.xlsx')
# Extract elemental property from pymatgen
Element = []
atomic_mass = []
melting_point = []
boiling_point = []
atomic_radius = []
average_ionic_radius = []
average_cationic_radius = []
average_anionic_radius = []
full_electronic_structure = []

for i in set(df['Ele']):
    ele = pmg.Element(i)
    Element.append(i)
    atomic_mass.append(ele.atomic_mass)
    melting_point.append(ele.melting_point)
    boiling_point.append(ele.boiling_point)
    atomic_radius.append(ele.atomic_radius)
    average_ionic_radius.append(ele.average_ionic_radius)
    average_cationic_radius.append(ele.average_cationic_radius)
    average_anionic_radius.append(ele.average_anionic_radius)
    full_electronic_structure.append(ele.full_electronic_structure)

f = pd.DataFrame(data = list(zip(Element,atomic_mass,melting_point,boiling_point,atomic_radius,average_ionic_radius,
                                average_cationic_radius,average_anionic_radius,full_electronic_structure)),
                 columns=['Element','atomic_mass','melting_point','boiling_point','atomic_radius','average_ionic_radius',
                                'average_cationic_radius','average_anionic_radius','full_electronic_structure'])
f.to_csv('Element_property.csv',index=False)

# Extract compound property from pymatgen
compound = []
weight = []
MR = []

'''
comp = pmg.Composition("Fe2O3")
comp.average_electroneg
comp.weight
comp.get_atomic_fraction('Fe')
comp.get_wt_fraction('Fe')
'''
for i in df['Compunds']:
    comp = pmg.Composition(i)
    compound.append(i)
    weight.append(comp.weight)
    MR.append(comp.get_atomic_fraction('Mg'))
f = pd.DataFrame(data=list(zip(compound,weight,MR)),columns=['compound','weight','MR'])
f.to_csv('compounds_property.csv',index=False)
