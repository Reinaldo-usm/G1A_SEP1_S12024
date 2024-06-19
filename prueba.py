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
p_nom = 100  # MW
q_nom = 50   # MVAR

# Crear carga inicial
pp.create_load(net, bus=b2, p_mw=p_nom, q_mvar=q_nom, name="carga1")

# Inicializar listas para almacenar resultados
loads = []
voltages = []

# Rango de variación de la carga (-50% a +50%)
p_range = np.linspace(0.5 * p_nom, 1.5 * p_nom, 20)
q_range = np.linspace(0.5 * q_nom, 1.5 * q_nom, 20)

# Ejecutar flujo de potencia para cada valor de carga en el rango
for p in p_range:
    for q in q_range:
        # Actualizar la carga en la red
        net.load.at[0, 'p_mw'] = p
        net.load.at[0, 'q_mvar'] = q
        
        # Ejecutar el flujo de potencia
        pp.runpp(net)
        
        # Almacenar los resultados
        loads.append(p)
        voltages.append(net.res_bus.vm_pu[1])

# Crear el gráfico
plt.figure(figsize=(10, 6))
plt.scatter(loads, voltages, c='b', marker='o')
plt.plot(loads, voltages, label='Variación de la Tensión')
plt.xlabel('Carga (MW)')
plt.ylabel('Tensión (pu)')
plt.title('Variación de la Tensión vs Potencia Demandada')
plt.legend()
plt.grid()
plt.show()
