# Modelo Criptográfico Actual

Este documento describe la arquitectura, el flujo y los mecanismos criptográficos implementados actualmente en el proyecto.

## Arquitectura

El sistema está compuesto por cuatro servicios:

- **Registraduría**
- **Wallet**
- **Establecimiento**
- **DIAN**

```text
                   ┌────────────────────┐
                   │   Registraduría    │
                   └─────────┬──────────┘
                             │
                 Credencial firmada
                             │
                             ▼
                   ┌────────────────────┐
                   │       Wallet       │
                   └─────────┬──────────┘
                             │
      Token Fiscal cifrado para la DIAN
                             │
                             ▼
                   ┌────────────────────┐
                   │   Establecimiento  │
                   └─────────┬──────────┘
                             │
          Factura firmada digitalmente
                             │
                             ▼
                   ┌────────────────────┐
                   │        DIAN        │
                   └────────────────────┘
```

---

# Flujo del sistema

## 1. Inicialización

### Registraduría

Genera (o carga) un par de claves **Ed25519**.

- SK_REG (clave privada)
- PK_REG (clave pública)

**Propósito**

- Firmar credenciales de identidad.

---

### DIAN

Genera (o carga) un par de claves **RSA-2048**.

- SK_DIAN
- PK_DIAN

**Propósito**

- Descifrar el Token Fiscal enviado por la Wallet.

---

### Establecimiento

Genera (o carga) un par de claves **Ed25519**.

- SK_EMPRESA
- PK_EMPRESA

**Propósito**

- Firmar digitalmente las facturas.

---

### Wallet

Actualmente no posee un par de claves propio.

---

## 2. Registro del comercio

El establecimiento publica su clave pública.

Posteriormente un administrador registra el comercio en la DIAN enviando:

- NIT
- Clave pública Ed25519

La DIAN almacena:

```text
NIT
 ↓
Clave pública del comercio
```

En esta etapa no existe cifrado; únicamente se intercambian claves públicas.

---

## 3. Emisión de la credencial

La Wallet solicita una credencial enviando:

- Cédula
- Nombre

La Registraduría construye la credencial y la firma utilizando **Ed25519**.

La Wallet recibe:

- Credencial
- Firma digital

---

## 4. Verificación de la credencial

La Wallet verifica la firma utilizando la clave pública de la Registraduría.

Si la firma no es válida, la credencial es descartada.

---

## 5. Generación del Token Fiscal

La Wallet solicita la clave pública RSA de la DIAN.

Posteriormente cifra únicamente la cédula utilizando:

- RSA-2048
- OAEP
- SHA-256

```text
TokenFiscal = RSA(PK_DIAN, Cedula)
```

Solo la DIAN puede recuperar la cédula.

---

## 6. Compra

La Wallet entrega al establecimiento únicamente:

- Token Fiscal

El establecimiento nunca recibe:

- Cédula
- Nombre
- Correo
- Teléfono

---

## 7. Construcción de la factura

El establecimiento genera una factura que contiene:

- Token Fiscal
- Productos
- Total

---

## 8. Firma digital

La factura se serializa de forma determinística y se firma utilizando **Ed25519**.

La firma garantiza:

- Integridad
- Autenticidad
- No repudio

---

## 9. Envío a la DIAN

Se envía:

- NIT
- Factura
- Firma digital

---

## 10. Verificación de la firma

La DIAN obtiene la clave pública asociada al NIT y verifica la firma.

Si la firma es inválida, la factura es rechazada.

---

## 11. Resolución del Token Fiscal

La DIAN utiliza su clave privada RSA para descifrar:

```text
Cedula = RSA_Decrypt(SK_DIAN, TokenFiscal)
```

Así obtiene la identidad real del comprador.

---

## 12. Registro

Finalmente la DIAN puede asociar:

- Cédula
- Productos
- Valor
- Fecha
- Comercio

sin que el establecimiento haya conocido la identidad del comprador.

---

# Algoritmos utilizados

| Componente | Algoritmo | Propósito |
|------------|-----------|-----------|
| Registraduría | Ed25519 | Firmar credenciales |
| Wallet | Ed25519 | Verificar credenciales |
| Wallet | RSA-OAEP + SHA-256 | Cifrar la cédula |
| Establecimiento | Ed25519 | Firmar facturas |
| DIAN | Ed25519 | Verificar firmas |
| DIAN | RSA-OAEP + SHA-256 | Descifrar el Token Fiscal |

---

# Propiedades de seguridad

| Propiedad | Mecanismo |
|-----------|-----------|
| Confidencialidad | RSA-OAEP |
| Integridad | Ed25519 |
| Autenticidad | Ed25519 |
| No repudio | Ed25519 |

---

# Estado actual del proyecto

Actualmente el sistema implementa:

- Criptografía asimétrica para confidencialidad mediante RSA.
- Firmas digitales mediante Ed25519.
- Un modelo simplificado de infraestructura de clave pública (PKI).
- Persistencia de claves criptográficas entre reinicios.

## Trabajo futuro

La siguiente evolución del proyecto será sustituir el Token Fiscal cifrado mediante RSA por un esquema basado en **Zero-Knowledge Proofs (ZKP)**, permitiendo demostrar propiedades del comprador sin revelar directamente su identidad al establecimiento.
