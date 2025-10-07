USE ProyectoBootcamp;
GO

IF OBJECT_ID('dbo.ventas','U')    IS NOT NULL DROP TABLE dbo.ventas;
IF OBJECT_ID('dbo.clientes','U')  IS NOT NULL DROP TABLE dbo.clientes;
IF OBJECT_ID('dbo.productos','U') IS NOT NULL DROP TABLE dbo.productos;
GO

CREATE TABLE dbo.productos(
  producto_id INT PRIMARY KEY,
  nombre      NVARCHAR(200) NOT NULL,
  categoria   NVARCHAR(100) NULL,
  precio      DECIMAL(18,2) NOT NULL
);

CREATE TABLE dbo.clientes(
  cliente_id  INT PRIMARY KEY,
  nombre      NVARCHAR(200) NOT NULL,
  email       NVARCHAR(200) NOT NULL,
  ciudad      NVARCHAR(100) NOT NULL,
  fecha_alta  DATE          NOT NULL
);

CREATE TABLE dbo.ventas(
  venta_id     INT PRIMARY KEY,
  cliente_id   INT NOT NULL,
  producto_id  INT NOT NULL,
  fecha_venta  DATE NOT NULL,
  cantidad     INT  NOT NULL,
  descuento    DECIMAL(5,2) NOT NULL
);
GO

BULK INSERT dbo.productos
FROM 'C:\Temp\week3\productos_clean.csv'
WITH (FIRSTROW=2, FIELDTERMINATOR=',', ROWTERMINATOR='0x0d0a', CODEPAGE='65001');

BULK INSERT dbo.clientes
FROM 'C:\Temp\week3\clientes_clean.csv'
WITH (FIRSTROW=2, FIELDTERMINATOR=',', ROWTERMINATOR='0x0d0a', CODEPAGE='65001');

BULK INSERT dbo.ventas
FROM 'C:\Temp\week3\ventas_clean.csv'
WITH (FIRSTROW=2, FIELDTERMINATOR=',', ROWTERMINATOR='0x0d0a', CODEPAGE='65001');

SELECT COUNT(*) productos FROM dbo.productos;
SELECT COUNT(*) clientes  FROM dbo.clientes;
SELECT COUNT(*) ventas    FROM dbo.ventas;
