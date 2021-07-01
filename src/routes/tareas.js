import { Router } from "express";
import { crearTarea, devolverTarea, listarTareas } from "../controllers/tareas";

export const tareas_router = Router();
// definir rutas cuando tengan diferentes endpoints
// tareas_router.post("/tareas", crearTarea);
// tareas_router.get("/tareas", listarTareas);

//definir rutas cuando varios metodos tengan el mismo endpoint
tareas_router.route("/tareas").get(listarTareas).post(crearTarea);

tareas_router.route("/tareas/:id").get(devolverTarea);
