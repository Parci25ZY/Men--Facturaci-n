import json
class JsonFile:
    def __init__(self, filename):
        self.filename = filename

    def save(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def read(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        return data
     
    def find(self, atributo, buscado):
        try:
            with open(self.filename, 'r') as file:
                datas = json.load(file)
                data = [item for item in datas if item[atributo] == buscado]
        except FileNotFoundError:
            data = []
        return data

    def update(self, atributo, buscado, updated_data):
        try:
            with open(self.filename, 'r+') as file:
                datas = json.load(file)
                for item in datas:
                    if item[atributo] == buscado:
                        item.update(updated_data)  # Actualiza los datos del cliente
                        file.seek(0)  # Vuelve al principio del archivo
                        json.dump(datas, file, indent=4)  # Escribe los datos actualizados
                        file.truncate()  # Trunca el archivo si es necesario
                        break
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al actualizar el archivo: {e}")

    def delete(self, atributo, buscado):
        try:
            with open(self.filename, 'r+') as file:
                datas = json.load(file)
                new_datas = []
                for item in datas:
                    if item[atributo] != buscado:
                        new_datas.append(item)
                file.seek(0)
                json.dump(new_datas, file, indent=4)
                file.truncate()
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al actualizar el archivo: {e}")


