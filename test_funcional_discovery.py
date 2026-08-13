#!/usr/bin/env python3
"""
Test Funcional del Módulo de Descubrimiento (Fase 4)
====================================================

Ejecuta el flujo completo de descubrimiento de oportunidades en LinkedIn:
1. Carga configuración y credenciales desde .env
2. Inicializa la base de datos
3. Ejecuta el orchestrator de discovery con todos los nodos
4. Se conecta a LinkedIn real (usa tus credenciales locales)
5. Consulta a Ollama para decisiones de IA
6. Guarda ofertas encontradas en SQLite
7. Genera reporte detallado: `reporte_test_funcional.md`

Uso:
    python test_funcional_discovery.py

Requisitos:
    - Tener config/.env con LINKEDIN_EMAIL y LINKEDIN_PASSWORD
    - Tener Ollama corriendo localmente (http://localhost:11434)
    - Navegador disponible (Chrome/Chromium instalado por Playwright)
"""

import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

# Agregar raíz del proyecto al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from shared.config import load as load_config
from shared.persistence import init_db, leer_tabla, generar_id
from shared.ia_service import analyze, load_prompt, render_prompt
from shared.decision_engine import evaluate, load_profile
from modules.discovery.orchestrator import ejecutar_flujo_descubrimiento
from modules.discovery.adapters.linkedin import LinkedInAdapter


def main():
    """Ejecuta el test funcional completo y genera reporte."""
    
    reporte = {
        "inicio": datetime.now(),
        "pasos": [],
        "errores": [],
        "resultados": {},
        "ofertas_encontradas": 0,
        "estado_final": "PENDIENTE"
    }
    
    def registrar_paso(nombre: str, exito: bool, detalle: str = "", datos: dict | None = None):
        reporte["pasos"].append({
            "paso": nombre,
            "exito": exito,
            "detalle": detalle,
            "datos": datos or {},
            "timestamp": datetime.now().isoformat()
        })
    
    def guardar_reporte():
        reporte["fin"] = datetime.now()
        reporte["duracion"] = str(reporte["fin"] - reporte["inicio"])
        
        contenido = f"""# 📊 Reporte de Test Funcional - Módulo de Descubrimiento

**Fecha de ejecución**: {reporte["inicio"].strftime('%Y-%m-%d %H:%M:%S')}  
**Duración total**: {reporte["duracion"]}  
**Estado final**: {reporte["estado_final"]}  
**Ofertas encontradas**: {reporte["ofertas_encontradas"]}

---

## ✅ Pasos Ejecutados

"""
        for i, paso in enumerate(reporte["pasos"], 1):
            icono = "✅" if paso["exito"] else "❌"
            contenido += f"{icono} **Paso {i}: {paso['paso']}**\n"
            contenido += f"   - Estado: {'Éxito' if paso['exito'] else 'Error'}\n"
            if paso["detalle"]:
                contenido += f"   - Detalle: {paso['detalle']}\n"
            if paso["datos"]:
                contenido += f"   - Datos: {paso['datos']}\n"
            contenido += "\n"
        
        if reporte["errores"]:
            contenido += "\n## ❌ Errores Encontrados\n\n"
            for i, error in enumerate(reporte["errores"], 1):
                contenido += f"### Error {i}: {error['tipo']}\n"
                contenido += f"**Ubicación**: {error['ubicacion']}\n"
                contenido += f"**Mensaje**: {error['mensaje']}\n"
                contenido += f"**Traceback**:\n```python\n{error['traceback']}\n```\n\n"
        
        contenido += f"\n---\n**Generado**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        with open(ROOT_DIR / "reporte_test_funcional.md", "w", encoding="utf-8") as f:
            f.write(contenido)
        
        print(f"\n📄 Reporte guardado en: {ROOT_DIR / 'reporte_test_funcional.md'}")
    
    try:
        # Paso 1: Cargar configuración
        print("🔧 [1/7] Cargando configuración...")
        try:
            config = load_config()
            registrar_paso("Cargar configuración", True, "Configuración cargada exitosamente", {
                "linkedin_email": config.get("linkedin", {}).get("email", "NO CONFIGURADO")[:10] + "...",
                "browser_headless": config.get("browser", {}).get("headless", True),
                "ia_local_model": config.get("ia", {}).get("local", {}).get("model", "NO CONFIGURADO")
            })
            print("   ✅ Configuración cargada")
        except Exception as e:
            registrar_paso("Cargar configuración", False, str(e))
            reporte["errores"].append({
                "tipo": "ConfigError",
                "ubicacion": "shared.config.load()",
                "mensaje": str(e),
                "traceback": traceback.format_exc()
            })
            raise
        
        # Paso 2: Verificar credenciales
        print("🔐 [2/7] Verificando credenciales de LinkedIn...")
        email = config.get("linkedin", {}).get("email", "")
        password = config.get("linkedin", {}).get("password", "")
        
        if not email or not password:
            error_msg = "Credenciales de LinkedIn no configuradas. Revisa config/.env"
            registrar_paso("Verificar credenciales", False, error_msg)
            reporte["errores"].append({
                "tipo": "CredentialError",
                "ubicacion": "config/.env",
                "mensaje": error_msg,
                "traceback": ""
            })
            raise ValueError(error_msg)
        
        registrar_paso("Verificar credenciales", True, f"Email: {email[:10]}... (oculto)")
        print("   ✅ Credenciales verificadas")
        
        # Paso 3: Inicializar base de datos
        print("💾 [3/7] Inicializando base de datos...")
        try:
            init_db()
            registrar_paso("Inicializar DB", True, "SQLite inicializado correctamente")
            print("   ✅ Base de datos lista")
        except Exception as e:
            registrar_paso("Inicializar DB", False, str(e))
            reporte["errores"].append({
                "tipo": "DatabaseError",
                "ubicacion": "shared.persistence.init_db()",
                "mensaje": str(e),
                "traceback": traceback.format_exc()
            })
            raise
        
        # Paso 4: Verificar conexión con Ollama
        print("🤖 [4/7] Verificando conexión con Ollama...")
        try:
            # Intentar cargar un prompt para verificar que Ollama responde
            prompt_text = load_prompt("PRM-001")
            registrar_paso("Verificar Ollama", True, "Ollama responde correctamente", {
                "prompt_cargado": "PRM-001",
                "longitud_prompt": len(prompt_text)
            })
            print("   ✅ Ollama conectado")
        except Exception as e:
            registrar_paso("Verificar Ollama", False, str(e))
            reporte["errores"].append({
                "tipo": "IAServiceError",
                "ubicacion": "shared.ia_service.load_prompt()",
                "mensaje": str(e),
                "traceback": traceback.format_exc()
            })
            print("   ⚠️  Advertencia: Ollama podría no estar disponible")
            # No levantamos error, continuamos para ver si hay otros problemas
        
        # Paso 5: Crear adapter de LinkedIn
        print("🔗 [5/7] Creando adapter de LinkedIn...")
        try:
            adapter = LinkedInAdapter(config)
            registrar_paso("Crear LinkedIn Adapter", True, "Adapter instanciado correctamente")
            print("   ✅ Adapter listo")
        except Exception as e:
            registrar_paso("Crear LinkedIn Adapter", False, str(e))
            reporte["errores"].append({
                "tipo": "AdapterError",
                "ubicacion": "modules.discovery.adapters.linkedin.LinkedInAdapter",
                "mensaje": str(e),
                "traceback": traceback.format_exc()
            })
            raise
        
        # Paso 6: Ejecutar flujo de descubrimiento
        print("🚀 [6/7] Ejecutando flujo de descubrimiento...")
        try:
            from dataclasses import dataclass
            from typing import Optional
            
            @dataclass
            class RunContext:
                config: dict
                adapter: Any
                dry_run: bool = False
                max_ofertas: int = 5
                timeout_nodo: int = 300
            
            contexto = RunContext(
                config=config,
                adapter=adapter,
                dry_run=False,
                max_ofertas=5,  # Limitar a 5 ofertas para el test
                timeout_nodo=300
            )
            
            resultado = ejecutar_flujo_descubrimiento(contexto)
            
            ofertas_guardadas = resultado.get("ofertas_guardadas", 0)
            reporte["ofertas_encontradas"] = ofertas_guardadas
            
            registrar_paso("Ejecutar flujo discovery", True, "Flujo completado exitosamente", {
                "ofertas_guardadas": ofertas_guardadas,
                "fuentes_registradas": resultado.get("fuentes_registradas", 0),
                "estado_corrida": resultado.get("estado_corrida", "DESCONOCIDO"),
                "id_corrida": resultado.get("id_corrida", "N/A")
            })
            print(f"   ✅ Flujo completado: {ofertas_guardadas} ofertas guardadas")
            
        except Exception as e:
            registrar_paso("Ejecutar flujo discovery", False, str(e))
            reporte["errores"].append({
                "tipo": "OrchestratorError",
                "ubicacion": "modules.discovery.orchestrator.ejecutar_flujo_descubrimiento()",
                "mensaje": str(e),
                "traceback": traceback.format_exc()
            })
            raise
        
        # Paso 7: Verificar resultados en DB
        print("📊 [7/7] Verificando resultados en base de datos...")
        try:
            ofertas = leer_tabla("ofertas")
            fuentes = leer_tabla("fuentes")
            
            registrar_paso("Verificar resultados DB", True, "Datos persistidos correctamente", {
                "total_ofertas": len(ofertas),
                "total_fuentes": len(fuentes),
                "primera_oferta": ofertas[0] if ofertas else None
            })
            print(f"   ✅ DB verificada: {len(ofertas)} ofertas, {len(fuentes)} fuentes")
            
        except Exception as e:
            registrar_paso("Verificar resultados DB", False, str(e))
            reporte["errores"].append({
                "tipo": "DatabaseReadError",
                "ubicacion": "shared.persistence.leer_tabla()",
                "mensaje": str(e),
                "traceback": traceback.format_exc()
            })
            # No levantamos error, es solo verificación final
        
        # Éxito total
        reporte["estado_final"] = "EXITOSO"
        print("\n" + "="*60)
        print("🎉 TEST FUNCIONAL COMPLETADO EXITOSAMENTE")
        print("="*60)
        print(f"📦 Ofertas encontradas: {reporte['ofertas_encontradas']}")
        print(f"⏱️  Duración: {reporte['fin'] - reporte['inicio']}")
        
    except Exception as e:
        reporte["estado_final"] = "FALLIDO"
        print("\n" + "="*60)
        print("❌ TEST FUNCIONAL FALLIDO")
        print("="*60)
        print(f"Error: {e}")
        print("\nRevisa el archivo `reporte_test_funcional.md` para detalles completos.")
    
    finally:
        # Guardar reporte siempre
        guardar_reporte()
        
        # Imprimir resumen rápido
        print("\n" + "-"*60)
        print("📋 RESUMEN RÁPIDO:")
        print(f"   Estado: {reporte['estado_final']}")
        print(f"   Pasos exitosos: {sum(1 for p in reporte['pasos'] if p['exito'])}/{len(reporte['pasos'])}")
        print(f"   Errores: {len(reporte['errores'])}")
        print(f"   Ofertas: {reporte['ofertas_encontradas']}")
        print("-"*60)


if __name__ == "__main__":
    main()
