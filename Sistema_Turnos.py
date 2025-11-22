class Cliente:
   def __init__(self, nombre, dni, email, telefono):
       self.nombre = nombre
       self.dni = dni
       self.email = email
       self.telefono = telefono


   def __str__(self):
       return f"Cliente: {self.nombre} | DNI: {self.dni} | Email: {self.email} | Teléfono: {self.telefono}"




class Mascota:
   def __init__(self, nombre, especie, edad, dueño):
       self.nombre = nombre
       self.especie = especie
       self.edad = edad
       self.dueño = dueño
   def __str__(self):
       return f"Mascota: {self.nombre} ({self.especie}, {self.edad} años) | Dueño: {self.dueño.nombre}"




class Veterinario:
   def __init__(self, nombre, especialidad):
       self.nombre = nombre
       self.especialidad = especialidad


   def __str__(self):
       return f"Veterinario: {self.nombre} | Especialidad: {self.especialidad}"




class Turno:
   def __init__(self, mascota, veterinario, fecha, hora, motivo):
       self.mascota = mascota
       self.veterinario = veterinario
       self.fecha = fecha
       self.hora = hora
       self.motivo = motivo


   def __str__(self):
       return (f"Turno para {self.mascota.nombre} con {self.veterinario.nombre} "
               f"el {self.fecha} a las {self.hora} | Motivo: {self.motivo}")


class SistemaTurnos:
   def __init__(self):
       self.clientes = []
       self.mascotas = []
       self.veterinarios = []
       self.turnos = []


   def agregar_cliente(self, cliente):
       # evitar registro duplicado por DNI
       for c in self.clientes:
           if c.dni == cliente.dni:
               print("Ya existe un cliente con ese DNI.")
               return
       self.clientes.append(cliente)
       print(f"Cliente {cliente.nombre} registrado")


   def agregar_mascota(self, mascota):
       self.mascotas.append(mascota)
       print(f"Mascota {mascota.nombre} registrada")


   def agregar_veterinario(self, veterinario):
       self.veterinarios.append(veterinario)


   def asignar_turno(self, turno):
       # Validar que no exista turno duplicado
       for t in self.turnos:
           if (t.veterinario == turno.veterinario and
               t.fecha == turno.fecha and
               t.hora == turno.hora):
               print("Ese veterinario ya tiene un turno en ese horario.")
               return


       self.turnos.append(turno)
       print(f"Turno registrado para {turno.mascota.nombre}")


   def mostrar_turnos(self):
       if not self.turnos:
           print("No hay turnos registrados.")
       else:
           print("\n=== TURNOS REGISTRADOS ===")
           for t in self.turnos:
               print(t)


if __name__ == "__main__":


   sistema = SistemaTurnos()


   # cargamos veterinarios
   sistema.agregar_veterinario(Veterinario("Dr. Ramírez", "Clínica general"))
   sistema.agregar_veterinario(Veterinario("Dra. López", "Dermatología"))
   sistema.agregar_veterinario(Veterinario("Dr. Gómez", "Cirugía"))


   while True:
       print("\n=== MENÚ PRINCIPAL PETCARE ===")
       print("1. Registrar cliente")
       print("2. Registrar mascota")
       print("3. Asignar turno")
       print("4. Ver turnos registrados")
       print("5. Salir")


       opcion = input("Seleccioná una opción: ")


       if opcion == "1":
           nombre = input("Nombre: ")
           dni = input("DNI: ")
           email = input("Email: ")
           telefono = input("Teléfono: ")
           sistema.agregar_cliente(Cliente(nombre, dni, email, telefono))


       elif opcion == "2":
           if not sistema.clientes:
               print("Primero registrá un cliente")
           else:
               print("\nClientes:")
               for i, c in enumerate(sistema.clientes):
                   print(f"{i+1}. {c.nombre}")


               indice = int(input("Seleccione dueño: ")) - 1
               dueño = sistema.clientes[indice]


               nombre = input("Nombre mascota: ")
               especie = input("Especie: ")
               edad = input("Edad: ")
               sistema.agregar_mascota(Mascota(nombre, especie, edad, dueño))


       elif opcion == "3":
           if not sistema.mascotas:
               print("Primero registrá una mascota")
           else:
               print("\nMascotas:")
               for i, m in enumerate(sistema.mascotas):
                   print(f"{i+1}. {m.nombre}")
               im = int(input("Seleccione mascota: ")) - 1


               print("\nVeterinarios:")
               for i, v in enumerate(sistema.veterinarios):
                   print(f"{i+1}. {v.nombre}")
               iv = int(input("Seleccione veterinario: ")) - 1


               fecha = input("Fecha (dd/mm/aaaa): ")
               hora = input("Hora: ")
               motivo = input("Motivo: ")


               sistema.asignar_turno(Turno(
                   sistema.mascotas[im],
                   sistema.veterinarios[iv],
                   fecha, hora, motivo
               ))


       elif opcion == "4":
           sistema.mostrar_turnos()


       elif opcion == "5":
           print("Gracias por usar PetCare")
           break


       else:
           print("Opción inválida")
