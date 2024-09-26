from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from appv1.models.base_class import Base  

# Modelo de la tabla Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    tipo_doc = Column(String(20), nullable=False)
    num_doc = Column(String(15), nullable=False)
    nombres = Column(String(50), nullable=False)
    apellidos = Column(String(120), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(14), nullable=True)

    # Relación con ComprobantePago
    comprobantes = relationship("ComprobantePago", back_populates="usuario")

# Modelo de la tabla ComprobantePago
class ComprobantePago(Base):
    __tablename__ = "comprobantes_pago"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    url_comprobante_pago = Column(String(255), nullable=False)

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="comprobantes")