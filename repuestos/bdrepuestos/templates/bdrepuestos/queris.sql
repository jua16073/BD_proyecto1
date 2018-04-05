UPDATE bdrepuestos_cliente SET nombre = 'Filomeno Martinez', telefono = '8899775566', dpi = '423322440101', correo = 'fmart@hotmail.com', tipo = 'A', direccion = 'dll 2da Calle, 24 avenida Lote 88', nit = '424521-8', twitter = '@holiwixd', fecha_de_comienzo = '2018-03-21'::date WHERE bdrepuestos_cliente.id = 6
INSERT INTO bdrepuestos_cliente (nombre, telefono, dpi, correo, tipo, direccion, nit, twitter, fecha_de_comienzo) VALUES ('Joaquin Rodriguez', '75223651', '887895120101', 'jrodriguez@outlook.com', 'B', '3ra Calle', '778855-8', 'lmaoCD', '2018-03-22'::date) RETURNING bdrepuestos_cliente.id

INSERT INTO bdrepuestos_producto (nombre, categoria, precioA, precioB, precioC, disponibilidad, marca, id_Proveedor_id) VALUES ('Filtro de Aire FF3088', 'Filtros', 50.0, 45.0, 40.0, 5, 'Froam', 1) RETURNING bdrepuestos_producto.id

INSERT INTO bdrepuestos_proveedor (nombre) VALUES ('Repuestos cajita de carton') RETURNING bdrepuestos_proveedor.id

INSERT INTO bdrepuestos_venta (fecha_de_venta, cliente_id, total, vendedor_id) VALUES ('2018-04-05'::date, 5, 200.0, 1) RETURNING bdrepuestos_venta.id

DELETE FROM bdrepuestos_cliente WHERE bdrepuestos_cliente.id = x
