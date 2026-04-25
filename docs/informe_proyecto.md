# Proyecto Final: Arquitectura Medallón y Despliegue CI/CD Multi-Cloud

**Autor:** Maycol Lopez Gavino  
**Repositorio GitHub:** [https://github.com/maycolgavino/ProyectoIngeneiadeDatos](https://github.com/maycolgavino/ProyectoIngeneiadeDatos) *(Recuerda verificar que el link sea este)*  

---

## 1. Descripción del Problema
Una importante empresa del sector maderero peruano enfrentaba serios desafíos en la gestión y análisis de su información comercial. Sus datos operativos —incluyendo registros de ventas, catálogo de especies maderables (Cedro, Caoba, Huimba, etc.) y cartera de clientes— se encontraban dispersos, desestructurados y generados en formatos manuales o poco eficientes. 

Esta falta de un repositorio centralizado ("Single Source of Truth") impedía a los gerentes tener visibilidad en tiempo real sobre las métricas clave del negocio. Resultaba imposible determinar con precisión qué especies de madera generaban la mayor rentabilidad, cuál era el volumen exacto de piezas vendidas por temporada, o cómo plantear estrategias de promociones efectivas, lo cual impactaba negativamente en la toma de decisiones financieras y operativas.

## 2. Solución Propuesta
Para resolver esta problemática, se diseñó e implementó una **Arquitectura de Datos Medallón** (Bronze, Silver, Gold) completamente automatizada, escalable y desplegada en la nube mediante prácticas de DevOps.

### 2.1. Arquitectura de Datos (Data Pipeline)
* **Capa Bronze (Ingesta):** Se desarrolló un script generador y extractor que captura los datos transaccionales crudos (ventas, clientes, catálogo de maderas) y los almacena en su estado original, asegurando la preservación histórica.
* **Capa Silver (Limpieza y Estandarización):** Mediante el uso de Python y Pandas, se implementaron transformaciones para limpiar datos nulos, estandarizar formatos de fechas y monedas, y consolidar una única tabla de hechos (`fact_ventas_marketing`) unida a sus dimensiones. Los datos procesados se guardan en formato `Parquet` para garantizar altas velocidades de lectura.
* **Capa Gold (Datamarts de Negocio):** Se construyeron cubos analíticos altamente optimizados. Específicamente, se generó el **Datamart de Rentabilidad**, el cual agrupa los ingresos totales, el volumen de piezas y las transacciones por especie maderable a nivel mensual y trimestral.

### 2.2. Visualización e Inteligencia de Negocios (BI)
El Datamart Gold es consumido directamente por un **Dashboard interactivo desarrollado en Streamlit**. Esta aplicación web permite a los tomadores de decisiones filtrar datos por año y especie, visualizando KPIs financieros, gráficos de anillos para la cuota de mercado por madera, y curvas de tendencia mensual, todo bajo una interfaz con diseño moderno y "Dark Mode" premium.

### 2.3. Infraestructura y Despliegue (CI/CD Multi-Cloud)
El proyecto destaca por ser **Agnóstico a la Nube (Cloud Agnostic)**. Toda la solución (tanto el pipeline de datos como el dashboard web) fue empaquetada utilizando contenedores **Docker**. 
Se implementaron flujos de Integración y Despliegue Continuo (CI/CD) mediante **GitHub Actions** que permiten automatizar la subida y el despliegue del proyecto hacia las tres principales nubes del mercado:
* **Amazon Web Services (AWS):** Integración con Amazon Elastic Container Registry (ECR).
* **Google Cloud Platform (GCP):** Integración con Artifact Registry y despliegue en Cloud Run.
* **Microsoft Azure:** Integración con Azure Container Registry y App Service.

Este enfoque asegura un pase a producción seguro, sin intervención manual y manejando las credenciales de los proveedores de nube a través de GitHub Secrets, cumpliendo con los más altos estándares de la industria tecnológica.
