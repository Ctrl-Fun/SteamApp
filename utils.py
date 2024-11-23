import json

def saveJSON(data: dict, name: str = "data.json"):
    file_path = f"./src/{name}"

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 para una salida más legible


def ApiMethodsList(publicFilePath: str, privateFilePath: str):
     # Abrir y cargar los datos públicos
    with open(publicFilePath) as f:
        publicData = json.load(f)
    
    # Abrir y cargar los datos privados
    with open(privateFilePath) as f:
        privateData = json.load(f)

    publicData = publicData["apilist"]["interfaces"]
    privateData = privateData["apilist"]["interfaces"]

    # print(privateData)

    data = dict(
        public = dict(),
        private = dict()
    )

    for interface in publicData:
        intName = interface["name"]
        methodArr = []
        for method in interface["methods"]:
            methName = method["name"]
            methodArr.append(methName)
        data["public"][intName] = methodArr

    for interface in privateData:
        intName = interface["name"]
        methodArr = []
        # Obtener los métodos públicos correspondientes (si existen)
        publicMethods = data["public"].get(intName, [])
        for method in interface["methods"]:
            methName = method["name"]
            # Añadir el método solo si no está en los métodos públicos
            if methName not in publicMethods:
                methodArr.append(methName)

        # for method in interface["methods"]:
        #     methName = method["name"]
        #     methodArr.append(methName)
        if(methodArr):
            data["private"][intName] = methodArr

    saveJSON(data, "interfacesAndMethods.json")
    


