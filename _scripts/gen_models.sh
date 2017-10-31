# Generate 3D model listings

rm ../_packages3d/*.md
python gen_3dmodel_info.py ~/kicad/share/kicad-library/modules/packages3d/*.3dshapes --output ../packages3d