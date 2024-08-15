import json

class CuentaBancaria:
    def __init__(self, numero_cuenta, saldo, titular):
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo
        self.titular = titular

    def depositar(self, monto):
        if monto > 0:
            self.saldo += monto
        else:
            raise ValueError("El monto de depósito debe ser positivo.")

    def retirar(self, monto):
        if 0 < monto <= self.saldo:
            self.saldo -= monto
        else:
            raise ValueError("Monto de retiro inválido o saldo insuficiente.")

    def obtener_info(self):
        return {
            "numero_cuenta": self.numero_cuenta,
            "saldo": self.saldo,
            "titular": self.titular
        }

    def to_dict(self):
        return self.obtener_info()

class CuentaBancariaCorriente(CuentaBancaria):
    def __init__(self, numero_cuenta, saldo, titular, descubierto):
        super().__init__(numero_cuenta, saldo, titular)
        self.descubierto = descubierto

    def retirar(self, monto):
        if 0 < monto <= self.saldo + self.descubierto:
            self.saldo -= monto
        else:
            raise ValueError("Monto de retiro inválido o saldo insuficiente.")

    def obtener_info(self):
        info = super().obtener_info()
        info["descubierto"] = self.descubierto
        return info

class CuentaBancariaAhorro(CuentaBancaria):
    def __init__(self, numero_cuenta, saldo, titular, tasa_interes):
        super().__init__(numero_cuenta, saldo, titular)
        self.tasa_interes = tasa_interes

    def aplicar_interes(self):
        self.saldo += self.saldo * (self.tasa_interes / 100)

    def obtener_info(self):
        info = super().obtener_info()
        info["tasa_interes"] = self.tasa_interes
        return info

class GestionCuentas:
    def __init__(self, archivo='cuentas.json'):
        self.archivo = archivo
        self.cuentas = self.cargar_datos()

    def guardar_datos(self):
        with open(self.archivo, 'w') as f:
            json.dump([c.to_dict() for c in self.cuentas], f)

    def cargar_datos(self):
        try:
            with open(self.archivo, 'r') as f:
                data = json.load(f)
                return self.crear_cuentas_desde_datos(data)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def crear_cuentas_desde_datos(self, data):
        cuentas = []
        for item in data:
            if 'descubierto' in item:
                cuentas.append(CuentaBancariaCorriente(item['numero_cuenta'], item['saldo'], item['titular'], item['descubierto']))
            elif 'tasa_interes' in item:
                cuentas.append(CuentaBancariaAhorro(item['numero_cuenta'], item['saldo'], item['titular'], item['tasa_interes']))
            else:
                cuentas.append(CuentaBancaria(item['numero_cuenta'], item['saldo'], item['titular']))
        return cuentas

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)
        self.guardar_datos()

    def eliminar_cuenta(self, numero_cuenta):
        self.cuentas = [c for c in self.cuentas if c.numero_cuenta != numero_cuenta]
        self.guardar_datos()

    def obtener_cuenta(self, numero_cuenta):
        for cuenta in self.cuentas:
            if cuenta.numero_cuenta == numero_cuenta:
                return cuenta
        return None

    def actualizar_cuenta(self, numero_cuenta, saldo=None, titular=None):
        cuenta = self.obtener_cuenta(numero_cuenta)
        if cuenta:
            if saldo is not None:
                cuenta.saldo = saldo
            if titular is not None:
                cuenta.titular = titular
            self.guardar_datos()
