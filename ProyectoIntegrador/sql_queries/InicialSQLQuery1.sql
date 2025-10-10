USE ProyectoBootcamp;
GO
SET NOCOUNT ON;

IF OBJECT_ID('dbo.ventas','U')    IS NOT NULL DROP TABLE dbo.ventas;
IF OBJECT_ID('dbo.clientes','U')  IS NOT NULL DROP TABLE dbo.clientes;
IF OBJECT_ID('dbo.productos','U') IS NOT NULL DROP TABLE dbo.productos;
GO

CREATE TABLE dbo.productos(
  producto_id INT NOT NULL,
  nombre      NVARCHAR(200) NOT NULL,
  categoria   NVARCHAR(100) NULL,
  precio      DECIMAL(18,2) NOT NULL
);

CREATE TABLE dbo.clientes(
  cliente_id  INT NOT NULL,
  nombre      NVARCHAR(200) NOT NULL,
  email       NVARCHAR(200) NOT NULL,
  ciudad      NVARCHAR(100) NOT NULL,
  fecha_alta  DATE          NOT NULL
);

CREATE TABLE dbo.ventas(
  venta_id     INT NOT NULL,
  cliente_id   INT NOT NULL,
  producto_id  INT NOT NULL,
  fecha_venta  DATE NOT NULL,
  cantidad     INT  NOT NULL,
  descuento    DECIMAL(5,2) NOT NULL
);
GO

-- BULK con formato CSV + UTF-8 + comillas, CRLF
BULK INSERT dbo.productos
FROM 'C:\Temp\week3\productos_clean.csv'
WITH (
  FORMAT = 'CSV',
  FIRSTROW = 2,
  FIELDQUOTE = '"',
  ROWTERMINATOR = '0x0d0a',
  CODEPAGE = '65001',
  TABLOCK
);

BULK INSERT dbo.clientes
FROM 'C:\Temp\week3\clientes_clean.csv'
WITH (
  FORMAT = 'CSV',
  FIRSTROW = 2,
  FIELDQUOTE = '"',
  ROWTERMINATOR = '0x0d0a',
  CODEPAGE = '65001',
  TABLOCK
);

BULK INSERT dbo.ventas
FROM 'C:\Temp\week3\ventas_clean.csv'
WITH (
  FORMAT = 'CSV',
  FIRSTROW = 2,
  FIELDQUOTE = '"',
  ROWTERMINATOR = '0x0d0a',
  CODEPAGE = '65001',
  TABLOCK
);
GO

-- Claves primarias (puedes dejarlas antes si preferís)
ALTER TABLE dbo.productos ADD CONSTRAINT PK_productos PRIMARY KEY (producto_id);
ALTER TABLE dbo.clientes  ADD CONSTRAINT PK_clientes  PRIMARY KEY (cliente_id);
ALTER TABLE dbo.ventas    ADD CONSTRAINT PK_ventas    PRIMARY KEY (venta_id);

-- Checks y FKs (como en tu segundo script)
ALTER TABLE dbo.ventas ADD CONSTRAINT CK_ventas_cantidad_pos     CHECK (cantidad > 0);
ALTER TABLE dbo.ventas ADD CONSTRAINT CK_ventas_descuento_rango  CHECK (descuento >= 0 AND descuento <= 100);

ALTER TABLE dbo.ventas ADD CONSTRAINT FK_ventas_clientes
  FOREIGN KEY (cliente_id)  REFERENCES dbo.clientes(cliente_id);
ALTER TABLE dbo.ventas ADD CONSTRAINT FK_ventas_productos
  FOREIGN KEY (producto_id) REFERENCES dbo.productos(producto_id);

-- Conteos
SELECT 'productos' AS tabla, COUNT(*) AS filas FROM dbo.productos
UNION ALL SELECT 'clientes', COUNT(*) FROM dbo.clientes
UNION ALL SELECT 'ventas'  , COUNT(*) FROM dbo.ventas;

