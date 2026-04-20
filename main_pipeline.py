import subprocess
import sys
import time

def run_script(script_name):
    """Ejecuta un script de Python de forma asilada y verifica su estado."""
    print(f"\n{'='*50}")
    print(f"| RE | INICIANDO JOB: {script_name}")
    print(f"{'='*50}")
    
    start_time = time.time()
    
    # Ejecutamos aisladamente para que la memoria pesada de un Job 
    # se libere al 100% y no recargue al siguiente.
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    
    elapsed = time.time() - start_time
    
    if result.returncode != 0:
        print(f"\n[ERROR] El job {script_name} falló. Finalizando Pipeline.")
        sys.exit(1)
        
    print(f"[XITO] Job {script_name} completado en {elapsed:.2f} segundos.")

def main():
    print("*** BIENVENIDO AL ORQUESTADOR MAESTRO DE DATOS: MEDALLION PIPELINE ***")
    print("Este Pipeline ejecutará toda la Cadena de Suministro Analítica.")
    
    # Paso 1: Extracción cruda (Data Warehouse Ingestion)
    run_script('generador_bronze.py')
    
    # Paso 2: Limpieza y Joins (Data Quality)
    run_script('procesador_silver.py')
    
    # Paso 3: Agrupaciones y Datamarts (Business Intelligence / Marketing)
    run_script('procesador_gold.py')
    
    print("\n*** PIPELINE MAESTRO COMPLETADO EXITOSAMENTE ***")
    print("Puedes apuntar directamente tus herramientas de BI a los Datamarts en `/data/gold/`")

if __name__ == '__main__':
    main()
