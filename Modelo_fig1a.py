import pandapower as pp
import pandapower.plotting.plotly as pplot
import matplotlib.pyplot as plt
import numpy as np

# Crear una red vacía
net = pp.create_empty_network()

# Crear un nuevo tipo de línea
line_data = {"r_ohm_per_km": 0.02, "x_ohm_per_km": 0.115, "c_nf_per_km": 19.1, "max_i_ka": 1., "type": "line"}
pp.create_std_type(net, line_data, "linea")

# Crear barras (buses)
b1 = pp.create_bus(net, vn_kv=500.)
b2 = pp.create_bus(net, vn_kv=500.)

# Crear una línea utilizando el nuevo tipo de línea
linea1 = pp.create_line(net, from_bus=b1, to_bus=b2, length_km=500., std_type="linea", name="linea1", parallel=2)

# Crear una barra externa
pp.create_ext_grid(net, bus=b1, vm_pu=1., name="barra_ext")

# Valores nominales de carga (puedes ajustarlos según sea necesario)
p_nom = 1080  # MW
q_nom = 522.3   # MVAR

# Crear carga inicial
pp.create_load(net, bus=b2, p_mw=p_nom, q_mvar=q_nom, name="carga1")
pplot.simple_plotly(net, bus_size=1, line_width=2, filename="fig1a.html")