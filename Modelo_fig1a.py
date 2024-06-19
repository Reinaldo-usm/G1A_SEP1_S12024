import pandapower as pp
import pandapower.plotting as plot 
import pandapower.plotting.plotly as pplot
net = pp.create_empty_network()
# Crear un nuevo tipo de línea
line_data = {"r_ohm_per_km": 0.02, "x_ohm_per_km": 0.115, "c_nf_per_km": 19.1, "max_i_ka": 1, "type": "line"}
pp.create_std_type(net, line_data, "linea")
b1 = pp.create_bus(net, vn_kv=500.)
b2 = pp.create_bus(net, vn_kv=500.)
# Crear una línea utilizando el nuevo tipo de línea
pp.create_line(net, from_bus=b1, to_bus=b2, length_km=500, std_type="linea")
pp.create_line(net, from_bus=b1, to_bus=b2, length_km=500, std_type="linea")   
pp.create_ext_grid(net, bus=b1)
s_mva=1200
pf=0.9
p_mw=s_mva*pf
q_mvar=s_mva*(1-pf)
pp.create_load(net, bus=b2, p_mw=p_mw, q_mvar=q_mvar)
pp.runpp(net)
pplot.simple_plotly(net)