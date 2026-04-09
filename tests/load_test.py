import asyncio
import httpx
import time

URL = "http://localhost:8000/order/save"
AUTH_COOKIE = None # Se podría pasar una cookie real aquí

async def create_order(client, i):
    data = {
        "vehicle_id": 1001,
        "diagnosis": f"Prueba de Carga #{i}"
    }
    try:
        # Nota: Esto podría fallar si no hay sesión, pero validamos la respuesta del servidor
        response = await client.post(URL, data=data)
        return response.status_code
    except Exception as e:
        return str(e)

async def main():
    print("Iniciando Prueba de Carga Beta (20 peticiones simultáneas)...")
    start = time.time()
    
    async with httpx.AsyncClient() as client:
        tasks = [create_order(client, i) for i in range(20)]
        results = await asyncio.gather(*tasks)
    
    end = time.time()
    success = [r for r in results if r == 200 or r == 302]
    errors = [r for r in results if r != 200 and r != 302]
    
    print(f"\n--- RESULTADOS ---")
    print(f"Tiempo Total: {end - start:.2f}s")
    print(f"Peticiones Exitosas: {len(success)}")
    print(f"Peticiones Fallidas/Bloqueadas: {len(errors)}")
    
    if len(errors) > 0:
        print(f"Muestra de Errores: {errors[:5]}")

if __name__ == "__main__":
    asyncio.run(main())
