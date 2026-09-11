"""Pruebas aisladas del contrato; NO crean informes ni afirman ejecuciones reales.

Las lecturas de archivos, imágenes y hashes son dobles de prueba explícitos.
Ejecutar con el Python documental bundled desde cualquier directorio.
"""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

RAIZ = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("reportes_curso", RAIZ / "scripts/reportes_curso.py")
reportes = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reportes)


def datos(numero):
    ids = {
        1: ["conversacion_8_turnos", "manejo_429", "repositorio"],
        2: ["ronda_1", "ronda_3", "cierre"],
        3: ["spec_manual", "flujo_speckit"],
        4: ["hook_bloqueando", "reporte_qa"],
    }[numero]
    valor = {
        "version": 1, "estado": "final",
        "practica": {"numero": numero, "titulo": "Solo fixture del validador"},
        "estudiante": {"nombre": "Persona ficticia de prueba"},
        "explicacion": "Datos sintéticos usados exclusivamente para probar guardias, nunca como informe académico.",
        "contenido_revisado": True,
        "evidencias": [{"id": eid, "tipo": "captura", "titulo": "Fixture de prueba",
                         "descripcion": "Doble de prueba sin ejecución académica.",
                         "imagen": "fixture.png", "fuente": "fixture.png", "verificada": True} for eid in ids],
        "reflexion": ["Respuesta ficticia uno", "Respuesta ficticia dos", "Respuesta ficticia tres"],
    }
    if numero != 2:
        valor["repositorio"] = {"url": "https://github.com/fixture-no-publicado/solo-prueba", "acceso_docente_verificado": True}
    if numero == 3:
        valor["secciones"] = [{"titulo": "Tabla de prueba", "tabla": {
            "columnas": ["Manual", "Spec Kit"], "filas": [["Fixture A", "Fixture B"]]}}]
    return valor


def cargar_fixture(valor):
    entrada = MagicMock(spec=Path)
    entrada.read_text.return_value = json.dumps(valor, ensure_ascii=False)
    entrada.parent = Path(".")
    def archivo_ficticio(base, value, campo):
        reportes.texto(value, campo)
        return Path("fixture-solo-test.png")
    with patch.object(reportes, "archivo_relativo", side_effect=archivo_ficticio), \
         patch.object(reportes, "sha256", return_value="0" * 64), \
         patch.object(reportes.PILImage, "open"):
        return reportes.cargar(entrada)


class GuardiasPorPractica(unittest.TestCase):
    def test_p2_final_sin_repositorio(self):
        d = cargar_fixture(datos(2))
        self.assertFalse(reportes.mostrar_repositorio(d))

    def test_p2_final_url_vacia_no_muestra_pendiente(self):
        d = datos(2)
        d["repositorio"] = {"url": "", "acceso_docente_verificado": False}
        self.assertFalse(reportes.mostrar_repositorio(cargar_fixture(d)))

    def test_p2_dos_rondas_distintas(self):
        d = datos(2)
        d["evidencias"] = [e for e in d["evidencias"] if e["id"] != "ronda_3"]
        with self.assertRaisesRegex(ValueError, "dos rondas distintas"):
            cargar_fixture(d)

    def test_p2_cierre_obligatorio(self):
        d = datos(2)
        d["evidencias"] = [e for e in d["evidencias"] if e["id"] != "cierre"]
        with self.assertRaisesRegex(ValueError, "cierre"):
            cargar_fixture(d)

    def test_p2_tres_reflexiones(self):
        d = datos(2)
        d["reflexion"] = d["reflexion"][:2]
        with self.assertRaisesRegex(ValueError, "tres respuestas"):
            cargar_fixture(d)

    def test_repo_opcional_p2_si_se_incluye_se_verifica(self):
        d = datos(2)
        d["repositorio"] = datos(1)["repositorio"]
        d["repositorio"]["acceso_docente_verificado"] = False
        with self.assertRaisesRegex(ValueError, "acceso docente"):
            cargar_fixture(d)

    def test_p1_p3_p4_exigen_repositorio(self):
        for numero in (1, 3, 4):
            with self.subTest(practica=numero):
                d = datos(numero)
                d.pop("repositorio")
                with self.assertRaisesRegex(ValueError, "acceso docente"):
                    cargar_fixture(d)

    def test_p1_p3_p4_completas_pasan_guardia(self):
        for numero in (1, 3, 4):
            with self.subTest(practica=numero):
                self.assertTrue(reportes.mostrar_repositorio(cargar_fixture(datos(numero))))

    def test_evidencias_especificas_p1_p3_p4(self):
        for numero in (1, 3, 4):
            with self.subTest(practica=numero):
                d = datos(numero)
                d["evidencias"].pop()
                with self.assertRaisesRegex(ValueError, "faltan las evidencias"):
                    cargar_fixture(d)

    def test_p3_tabla_obligatoria(self):
        d = datos(3)
        d["secciones"] = []
        with self.assertRaisesRegex(ValueError, "tabla comparativa"):
            cargar_fixture(d)

    def test_simulacion_se_rechaza_en_todas(self):
        for numero in (1, 2, 3, 4):
            with self.subTest(practica=numero):
                d = datos(numero)
                d["evidencias"][0]["tipo"] = "simulacion"
                with self.assertRaisesRegex(ValueError, "sin simulación"):
                    cargar_fixture(d)

    def test_sin_verificar_se_rechaza_en_todas(self):
        for numero in (1, 2, 3, 4):
            with self.subTest(practica=numero):
                d = datos(numero)
                d["evidencias"][0]["verificada"] = False
                with self.assertRaisesRegex(ValueError, "evidencia verificada"):
                    cargar_fixture(d)

    def test_borrador_conserva_pendientes(self):
        d = datos(2)
        d["estado"] = "borrador"
        d["evidencias"] = []
        d["reflexion"] = []
        self.assertFalse(reportes.mostrar_repositorio(cargar_fixture(d)))


def entrega_observada():
    d = datos(1)
    d["estado"] = "entrega_con_observaciones"
    for evidencia in d["evidencias"]:
        if evidencia["id"] == "manejo_429":
            evidencia["id"] = "ensayo_sin_429"
            evidencia["tipo"] = "registro_renderizado"
            evidencia["fuente"] = "fixture-ensayo.txt"
    d["observaciones"] = [{
        "requisito_id": "manejo_429", "tipo": "no_observado",
        "evidencia_ids": ["ensayo_sin_429"],
        "protocolo": "Fixture: dos ensayos acotados descritos por separado.",
        "resultado": "Fixture: ninguno observó un error 429.",
        "limite": "Fixture: no acredita el manejo de un error real del proveedor.",
    }]
    d["requisitos"] = [{"id": "manejo_429", "estado": "pendiente",
                        "descripcion": "Observar y manejar el 429 real",
                        "evidencia_ids": ["ensayo_sin_429"]}]
    return d


class EntregaConObservaciones(unittest.TestCase):
    def test_entrega_honesta_pasa_y_conserva_pendiente(self):
        d = cargar_fixture(entrega_observada())
        self.assertEqual(d["estado"], "entrega_con_observaciones")
        self.assertEqual(d["requisitos"][0]["estado"], "pendiente")
        self.assertNotIn("manejo_429", {e["id"] for e in d["evidencias"]})

    def test_observacion_completa_y_especifica_obligatoria(self):
        cambios = [
            ("tipo", "simulado"), ("requisito_id", "otro_requisito"),
            ("protocolo", ""), ("resultado", ""), ("limite", ""),
            ("evidencia_ids", []), ("evidencia_ids", ["inexistente"]),
            ("evidencia_ids", ["conversacion_8_turnos"]),
        ]
        for campo, valor in cambios:
            with self.subTest(campo=campo, valor=valor):
                d = entrega_observada()
                d["observaciones"][0][campo] = valor
                with self.assertRaises(ValueError):
                    cargar_fixture(d)
        for valor in ([], None, [{}, {}]):
            d = entrega_observada()
            d["observaciones"] = valor
            with self.assertRaisesRegex(ValueError, "observación explícita"):
                cargar_fixture(d)

    def test_sin_fuente_del_ensayo_no_pasa(self):
        d = entrega_observada()
        next(e for e in d["evidencias"] if e["id"] == "ensayo_sin_429").pop("fuente")
        with self.assertRaisesRegex(ValueError, "evidencias.fuente"):
            cargar_fixture(d)

    def test_repositorio_accesible_sigue_obligatorio(self):
        for repo in ({}, {"url": "https://github.com/fixture/repo", "acceso_docente_verificado": False},
                     {"url": "https://example.com/fixture", "acceso_docente_verificado": True}):
            with self.subTest(repo=repo):
                d = entrega_observada()
                d["repositorio"] = repo
                with self.assertRaises(ValueError):
                    cargar_fixture(d)

    def test_simulacion_o_evidencia_sin_verificar_no_pasan(self):
        for campo, valor in (("tipo", "simulacion"), ("verificada", False)):
            d = entrega_observada()
            next(e for e in d["evidencias"] if e["id"] == "ensayo_sin_429")[campo] = valor
            with self.assertRaisesRegex(ValueError, "evidencia verificada, sin simulación"):
                cargar_fixture(d)

    def test_autoria_revisada_sigue_obligatoria(self):
        d = entrega_observada()
        d["contenido_revisado"] = False
        with self.assertRaisesRegex(ValueError, "contenido_revisado"):
            cargar_fixture(d)

    def test_otro_pendiente_no_pasa(self):
        d = entrega_observada()
        d["requisitos"].append({"id": "repositorio", "estado": "pendiente", "descripcion": "Fixture pendiente"})
        with self.assertRaisesRegex(ValueError, "requisitos pendientes"):
            cargar_fixture(d)

    def test_requisito_no_puede_ocultarse_ni_declararse_cumplido(self):
        for estado in ("cumplido", "no_aplica", None):
            d = entrega_observada()
            if estado is None:
                d["requisitos"] = []
            else:
                d["requisitos"][0]["estado"] = estado
            with self.assertRaisesRegex(ValueError, "como pendiente"):
                cargar_fixture(d)
        d = entrega_observada()
        d["requisitos"][0]["evidencia_ids"] = []
        with self.assertRaisesRegex(ValueError, "vincular su evidencia"):
            cargar_fixture(d)

    def test_no_exime_otra_evidencia_obligatoria(self):
        for eid in ("conversacion_8_turnos", "repositorio", "ensayo_sin_429"):
            d = entrega_observada()
            d["evidencias"] = [e for e in d["evidencias"] if e["id"] != eid]
            with self.assertRaises(ValueError):
                cargar_fixture(d)

    def test_no_admite_observacion_contradictoria(self):
        d = entrega_observada()
        d["evidencias"].append(copy.deepcopy(datos(1)["evidencias"][1]))
        with self.assertRaisesRegex(ValueError, "contradice"):
            cargar_fixture(d)

    def test_solo_practica_uno(self):
        for numero in (2, 3, 4):
            d = entrega_observada()
            d["practica"]["numero"] = numero
            with self.assertRaisesRegex(ValueError, "solo está habilitado para práctica 1"):
                cargar_fixture(d)

    def test_final_estricto_sigue_exigiendo_429(self):
        d = entrega_observada()
        d["estado"] = "final"
        d.pop("observaciones")
        d["requisitos"] = []
        with self.assertRaisesRegex(ValueError, "faltan las evidencias exigidas: manejo_429"):
            cargar_fixture(d)
        d = entrega_observada()
        d["estado"] = "final"
        with self.assertRaisesRegex(ValueError, "observaciones solo se admite"):
            cargar_fixture(d)

    def test_aviso_y_observacion_entran_en_ambos_formatos_sin_generar_archivos(self):
        d = cargar_fixture(entrega_observada())
        with patch.object(reportes, "SimpleDocTemplate") as pdf, \
             patch.object(reportes, "Image"), \
             patch.object(reportes, "dimensiones", return_value=(100, 60)):
            self.assertEqual(reportes.pdf_bytes(d), b"")
        story = pdf.return_value.build.call_args.args[0]
        texto_pdf = "\n".join(p.getPlainText() for p in story if isinstance(p, reportes.Paragraph))
        doc = reportes.Document()
        with patch.object(reportes, "Document", return_value=doc), \
             patch.object(type(doc), "save"), \
             patch("docx.text.run.Run.add_picture"), \
             patch.object(reportes, "dimensiones", return_value=(100, 60)):
            self.assertEqual(reportes.docx_bytes(d), b"")
        texto_docx = "\n".join(p.text for p in doc.paragraphs)
        for contenido in (texto_pdf, texto_docx):
            for fragmento in ("INFORME DE ENTREGA CON OBSERVACIONES", "No declara cumplimiento total",
                              "manejo_429: pendiente", "no_observado", "ensayo_sin_429",
                              *[d["observaciones"][0][c] for c in ("protocolo", "resultado", "limite")]):
                self.assertIn(fragmento, contenido)
            self.assertNotIn("PRUEBA TÉCNICA DEL GENERADOR", contenido)

    def test_manifiesto_deja_explicito_que_no_hay_cumplimiento_total(self):
        d = cargar_fixture(entrega_observada())
        salida = MagicMock(spec=Path)
        salida.exists.return_value = False
        with patch.object(reportes, "pdf_bytes", return_value=b""), \
             patch.object(reportes, "docx_bytes", return_value=b""), \
             patch.object(reportes, "sha256", return_value="0" * 64):
            manifiesto = reportes.generar(d, salida)
        self.assertFalse(manifiesto["cumplimiento_total"])
        self.assertEqual(manifiesto["requisitos_pendientes"], ["manejo_429"])
        self.assertEqual(manifiesto["observaciones"][0]["tipo"], "no_observado")


if __name__ == "__main__":
    unittest.main(verbosity=2)
