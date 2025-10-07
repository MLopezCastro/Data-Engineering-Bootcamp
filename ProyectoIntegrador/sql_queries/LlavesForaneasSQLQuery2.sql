ALTER TABLE dbo.ventas
  ADD CONSTRAINT FK_ventas_clientes  FOREIGN KEY (cliente_id)  REFERENCES dbo.clientes(cliente_id),
      CONSTRAINT FK_ventas_productos FOREIGN KEY (producto_id) REFERENCES dbo.productos(producto_id),
      CONSTRAINT CK_ventas_cantidad  CHECK (cantidad > 0),
      CONSTRAINT CK_ventas_desc      CHECK (descuento BETWEEN 0 AND 100);
