from sqlalchemy.orm import Session
from appv1.models.prueba import Usuario
from appv1.models.prueba import ComprobantePago

def insertar_usuario(db: Session, tipo_doc: str, num_doc:str, nombres: str, apellidos: str,  correo: str,  telefono: str = None):
    # Crear un nuevo objeto Usuario
    nuevo_usuario = Usuario(
        tipo_doc=tipo_doc,
        num_doc=num_doc,
        nombres=nombres,
        apellidos=apellidos,
        correo=correo,
        telefono=telefono
    )
    # Añadir el usuario a la sesión
    db.add(nuevo_usuario)
    # Confirmar la transacción
    db.commit()
    # Refrescar la instancia para obtener el ID generado por la base de datos
    db.refresh(nuevo_usuario)
    return nuevo_usuario

def insertar_comprobante_pago(db: Session, usuario_id: int, url_comprobante_pago: str):
    # Crear un nuevo objeto ComprobantePago
    nuevo_comprobante = ComprobantePago(
        usuario_id=usuario_id,
        url_comprobante_pago=url_comprobante_pago
    )
    # Añadir el comprobante a la sesión
    db.add(nuevo_comprobante)
    # Confirmar la transacción
    db.commit()
    # Refrescar la instancia para obtener el ID generado por la base de datos
    db.refresh(nuevo_comprobante)
    return nuevo_comprobante
