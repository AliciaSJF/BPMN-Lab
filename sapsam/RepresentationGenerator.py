import json
import requests
import logging
from sapsam.conf import system_instance
from sapsam.SignavioAuthenticator import SignavioAuthenticator

# Configuración de logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class RepresentationGenerator:
    """
    Class that generates images based on JSON or XML representations
    """

    def _delete_diagram(self, id: str):
        """Elimina un diagrama en SAP Signavio Process Manager por su ID"""
        auth_data = SignavioAuthenticator.authenticate()
        model_url = system_instance + '/p/model'
        # model_url = system_instance + '/spm/v1/model'
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id': auth_data['auth_token']}
        
        logging.info(f'🗑️ Deleting model {id} at {model_url}/{id}')
        
        response = requests.delete(f'{model_url}/{id}', cookies=cookies, headers=headers)
        
        logging.info(f'🔍 DELETE Response: {response.status_code} - {response.text}')

    def _get_dir_id(self, meta_request):
        """Obtiene el ID del directorio donde se almacenará la carpeta 'SAP-SAM'"""
        logging.info(f'📂 Retrieving directory ID from response...')
        
        json_data = meta_request.json()
        logging.debug(f'🔍 Directory JSON Response: {json_data}')
        
        for directory in json_data:
            if directory.get('rel') == 'dir':
                name = directory['rep'].get('name', '')
                if name == 'My documents':
                    my_docs_id = directory['href'].replace('/directory/', '')
                    logging.info(f'📂 Using My Documents ID: {my_docs_id}')
                    return my_docs_id

        shared_docs_id = json_data[0]['href'].replace('/directory/', '')
        logging.info(f'📂 Using Shared Documents ID: {shared_docs_id}')
        return shared_docs_id

    def _setup_folder(self):
        """Crea una carpeta 'SAP-SAM' en el directorio 'Shared Documents' si no existe"""
        auth_data = SignavioAuthenticator.authenticate()
        dir_url = system_instance + '/p/directory'
        # dir_url = system_instance + '/spm/v1/directory'
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id': auth_data['auth_token']}
        
        logging.info(f'📂 Fetching directory metadata from {dir_url}')
        
        get_dir_meta_request = requests.get(dir_url, cookies=cookies, headers=headers)
        if get_dir_meta_request.status_code != 200:
            logging.error(f'❌ Error fetching directories: {get_dir_meta_request.text}')
            return None

        dir_id = self._get_dir_id(get_dir_meta_request)

        if dir_id is None:
            logging.error("❌ No se pudo obtener el ID del directorio. Abortando...")
            return None        
        get_shared_docs_meta_request = requests.get(f'{dir_url}/{dir_id}', cookies=cookies, headers=headers)
        results = get_shared_docs_meta_request.json()
        
        folder_names_hrefs = [(result['rep']['name'], result['href']) for result in results if 'rep' in result and 'name' in result['rep']]
        sapsam_id = None
        
        for (name, href) in folder_names_hrefs:
            if name == 'SAP-SAM' and 'directory' in href:
                sapsam_id = href.replace('/directory/', '')

        if sapsam_id:
            logging.info(f'📂 Folder "SAP-SAM" found with ID {sapsam_id}')
            return sapsam_id
        else:
            logging.info(f'📂 Creating new folder "SAP-SAM" in {dir_id}')
            create_dir_request = requests.post(
                dir_url,
                cookies=cookies,
                headers=headers,
                data={'name': 'SAP-SAM', 'parent': f'/directory/{dir_id}'}
            )
            if create_dir_request.status_code != 201:
                logging.error(f'❌ Error creating directory: {create_dir_request.text}')
                return None

            new_folder_id = json.loads(create_dir_request.content)['href'].replace('/directory/', '')
            logging.info(f'📂 New folder created with ID {new_folder_id}')
            return new_folder_id

    def generate_representation(self, name, json_data, namespace, rep, deletes=True):
        """Sube un diagrama a Signavio y devuelve su representación."""
        
        auth_data = SignavioAuthenticator.authenticate()
        model_url = system_instance + '/p/model'
        # model_url = system_instance + '/spm/v1/model'
        cookies = {'JSESSIONID': auth_data['jsesssion_ID'], 'LBROUTEID': auth_data['lb_route_ID']}
        headers = {'Accept': 'application/json', 'x-signavio-id': auth_data['auth_token']}
        
        parent_folder = self._setup_folder()
        if not parent_folder:
            logging.error("❌ No se pudo obtener el ID del directorio.")
            return None

        data = {
            'name': name,
            'parent': f'/directory/{parent_folder}',
            'namespace': namespace,
            'json_xml': json.dumps(json_data)  # 💡 Asegurarse de que el JSON se envía correctamente
        }

        print("📤 JSON Enviado (truncado):", json.dumps(data)[:500])  # Muestra solo los primeros 500 caracteres

        # 🔍 Debugging: Verificar que los datos no están vacíos
        logging.debug(f"📤 Enviando datos al servidor: {json.dumps(data, indent=2)}")

        create_diagram_request = requests.post(model_url, cookies=cookies, headers=headers, data=data)

        # 🔍 Debugging: Ver respuesta HTTP
        logging.debug(f"📥 Respuesta HTTP {create_diagram_request.status_code}: {create_diagram_request.text}")


        ### ESTO ESTA CAMBIADO -> (if create_diagram_request.status_code != 201) != (if create_diagram_request.status_code != 200) 
        if create_diagram_request.status_code != 200:
            logging.error(f'❌ Error creando el modelo: {create_diagram_request.text}')
            return None  

        result = json.loads(create_diagram_request.content)
        model_id = result.get('href', '').replace('/model/', '')
        revision_id = result.get('rep', {}).get('revision', '').replace('/revision/', '')

        diagram_url = system_instance + '/p/revision'
        # diagram_url = system_instance + '/spm/v1/revision'
        rep_request = requests.get(f'{diagram_url}/{revision_id}/{rep}', cookies=cookies, headers=headers)

        if rep_request.status_code != 200:
            logging.error(f'❌ Error obteniendo la representación: {rep_request.text}')
            return None  

        if deletes:
            self._delete_diagram(model_id)

        return rep_request.content

    def generate_image(self, name, data, namespace, deletes=True):
        """Genera la imagen del modelo"""
        return self.generate_representation(name, data, namespace, 'png', deletes)


    def generate_bpmn_xml(self, name, data, namespace, deletes=True):
        """Genera un diagrama en formato BPMN 2.0 XML"""
        return self.generate_representation(name, data, namespace, 'bpmn2_0_xml', deletes)
