## **Objetivo**

Explorar el uso de modelos de lenguaje (LLMs) para generar descripciones detalladas de modelos BPMN y comprobar si, a partir de dichas descripciones, se puede reconstruir un modelo BPMN similar al original.

---

## **1. Selección de Recursos**

Antes de comenzar, es necesario definir los recursos que utilizaremos:

### **1.1. Papers de referencia**

Los siguientes papers proporcionan el contexto y las técnicas necesarias para el enfoque basado en LLMs y agentes:

- 📄 **ProAgent**: [ArXiv 2311.10751](https://arxiv.org/pdf/2311.10751) | [Repositorio OpenBMB](https://github.com/OpenBMB/ProAgent)
- 📄 **MAO: Multi-Agent Orchestration**: [ArXiv 2408.01916](https://arxiv.org/pdf/2408.01916) | [Repositorio Anónimo](https://anonymous.4open.science/r/MAO-1074/README.md)

### **1.2. Dataset BPMN**

Para trabajar con modelos BPMN reales, se usará el **SAP Signavio Open Dataset**:

- 📂 Blog con información: [SAP Community](https://community.sap.com/t5/technology-blogs-by-sap/exploring-the-sap-signavio-open-dataset-with-hundreds-of-thousands-of/ba-p/13525392)
- 📥 Descarga del dataset: [SAP Signavio Academic Models](https://zenodo.org/records/7012043)

---

## **2. Flujo de Trabajo**

### **2.1. Selección de Modelos BPMN**

- Se extraerán algunos modelos BPMN representativos del dataset.
- Se analizarán las estructuras clave del modelo seleccionado.

### **2.2. Generación de Descripciones Detalladas con un LLM**

- Se usará un **modelo de IA generativa** (como GPT-4, Claude o Mistral) para describir el BPMN en texto natural.
- El prompt debe guiar al LLM para generar una descripción detallada, incluyendo:
    - Actividades
    - Decisiones y gateways
    - Eventos de inicio y fin
    - Roles de participantes
    - Flujo del proceso

### **2.3. Reconstrucción del BPMN desde la Descripción**

- Se probarán **MOE (Model Order Estimation)** o técnicas similares para evaluar si el LLM puede generar un modelo BPMN a partir de su propia descripción.
- La comparación entre el BPMN original y el reconstruido servirá para medir la **precisión** del proceso.

### **2.4. Visualización y Evaluación**

- Se utilizará [bpmn.io](https://demo.bpmn.io/) para visualizar los BPMN originales y generados.
- Se compararán las estructuras con métricas como:
    - Similitud estructural
    - Coherencia del flujo de trabajo
    - Precisión en la asignación de roles y eventos

---

## **3. Documentación del Proceso**

Para facilitar la replicación del experimento, se documentará cada paso en un **cuaderno Jupyter** con:

1. **Carga y exploración del dataset**
2. **Generación de descripciones con LLM**
3. **Reconstrucción de BPMN desde texto**
4. **Comparación y análisis de resultados**
5. **Conclusiones y mejoras posibles**

---

## **4. Herramientas y Tecnologías**

|**Recurso**|**Descripción**|
|---|---|
|🔹 **Python + Jupyter**|Para estructurar el experimento|
|🔹 **LLM API (OpenAI, Mistral, etc.)**|Para generar descripciones|
|🔹 **MOE u otras técnicas**|Para modelar BPMN desde texto|
|🔹 **bpmn.io**|Para visualizar modelos BPMN|
|🔹 **SAP Signavio Dataset**|Modelos reales de procesos BPMN|




---


    Este proyecto utiliza el dataset SAP Signavio Academic Models (SAP-SAM), publicado por SAP.
    Fuente: SAP-SAM en Zenodo
    DOI: 10.5281/zenodo.6964944
    Paper asociado: SAP Signavio Academic Models: A Large Process Model Dataset.


