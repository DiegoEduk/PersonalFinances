
CREATE DATABASE personal_finances CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE personal_finances;

-- Para tener en cuenta en BackEnd
-- un cliente solo puede insertar y editar transacciones propias.
-- cualquier usuario puede registrarse como cliente.
-- cualquier usuario puede modificar su propia información.

CREATE TABLE roles (
    rol_name VARCHAR(15) PRIMARY KEY
);

CREATE TABLE modules (
    module_name VARCHAR(15) PRIMARY KEY
);

CREATE TABLE permissions(
    rol_name VARCHAR(15),   
    module_name VARCHAR(15),
    p_select TINYINT(1) DEFAULT 1,
    p_insert TINYINT(1) DEFAULT 1,
    p_update TINYINT(1) DEFAULT 1,
    p_delete TINYINT(1) DEFAULT 1,
    PRIMARY KEY (rol_name, module_name),
    FOREIGN KEY (rol_name) REFERENCES roles(rol_name),
    FOREIGN KEY (module_name) REFERENCES modules(module_name)
);

CREATE TABLE users (
    user_id CHAR(30) PRIMARY KEY,
    full_name VARCHAR(80),
    mail VARCHAR(100) UNIQUE, -- user_name
    passhash VARCHAR(140),
    user_role VARCHAR(15),
    user_status TINYINT(1) DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_role) REFERENCES roles (rol_name)
);

CREATE TABLE category (
    category_id SMALLINT(3) AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50),
    category_description VARCHAR(120),
    category_status TINYINT(1) DEFAULT 1
);

CREATE TABLE transactions (
    transactions_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(30),
    category_id SMALLINT(3),
    amount FLOAT(10,2), 
    t_description VARCHAR(120),
    t_type ENUM('revenue','expenses'),
    t_date DATE,
    FOREIGN KEY (user_id) REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES category (category_id)
);

INSERT INTO roles(rol_name) VALUES ('SuperAdmin');
INSERT INTO roles(rol_name) VALUES ('Admin');
INSERT INTO roles(rol_name) VALUES ('Cliente');

INSERT INTO modules VALUES ('roles');
INSERT INTO modules VALUES ('usuarios');
INSERT INTO modules VALUES ('transacciones');

INSERT INTO permissions VALUES ('SuperAdmin', 'roles', 1, 1, 1, 1);
INSERT INTO permissions VALUES ('SuperAdmin', 'usuarios', 1, 1, 1, 1);
INSERT INTO permissions VALUES ('SuperAdmin', 'transacciones', 1, 1, 0, 0);
INSERT INTO permissions VALUES ('Admin', 'roles', 0, 0, 0, 0);
INSERT INTO permissions VALUES ('Admin', 'usuarios', 1, 1, 0, 0);
INSERT INTO permissions VALUES ('Admin', 'transacciones', 1, 1, 0, 0);
INSERT INTO permissions VALUES ('Cliente', 'roles', 0, 0, 0, 0);
INSERT INTO permissions VALUES ('Cliente', 'usuarios', 0, 0, 0, 0);
INSERT INTO permissions VALUES ('Cliente', 'transacciones', 1, 1, 1, 1);

INSERT INTO category(category_name,category_description)
VALUES('Salario','Mi salario mensual en mi trabajo');
INSERT INTO category(category_name,category_description)
VALUES('Arriendo','Pago por servicios de arriendo');


app.include_router(users.router, prefix="/users", tags=["users"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Permitir estos métodos HTTP
    allow_headers=["*"],  # Permitir cualquier encabezado en las solicitudes
)