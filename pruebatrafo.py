# Inicializar listas para almacenar las pérdidas en la línea
losses_with_compensation = []
losses_without_compensation = []

# Para cada valor en el rango de variación de la carga
for p, q in zip(p_range, q_range):
    # Actualizar la carga en la red
    net.load.at[0, 'p_mw'] = p
    net.load.at[0, 'q_mvar'] = q

    # Ejecutar el flujo de potencia
    pp.runpp(net)

    # Calcular las pérdidas en la línea y almacenarlas en la lista sin compensación
    losses_without_compensation.append(net.res_line.p_from_mw[0] - net.res_line.p_to_mw[0])

    # Ajustar la susceptancia shunt
    while True:
        # Ejecutar el flujo de potencia
        pp.runpp(net)

        # Obtener el valor de tensión en la barra b2
        v = net.res_bus.vm_pu[1]

        # Verificar las condiciones de tensión
        if v > 1.03:
            # Si la tensión es demasiado alta, aumentar la susceptancia shunt (compensación capacitiva)
            b += 1
        elif v < 0.97:
            # Si la tensión es demasiado baja, disminuir la susceptancia shunt (compensación inductiva)
            b -= 1
        else:
            # Si las condiciones de tensión se cumplen, salir del bucle
            break

        # Actualizar la susceptancia shunt en la red
        net.shunt.at[shunt, 'q_mvar'] = b * v**2

    # Calcular las pérdidas en la línea y almacenarlas en la lista con compensación
    losses_with_compensation.append(net.res_line.p_from_mw[0] - net.res_line.p_to_mw[0])

# Crear la figura
plt.figure(figsize=(10, 6))
plt.plot(loads, losses_without_compensation, label='Pérdidas sin compensación')
plt.plot(loads, losses_with_compensation, label='Pérdidas con compensación')
plt.xlabel('Potencia en la carga (MW)')
plt.ylabel('Pérdidas en la línea (MW)')
plt.title('Pérdidas en la línea vs Potencia en la carga')
plt.legend()
plt.grid()
plt.show()