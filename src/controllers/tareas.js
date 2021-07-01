import { tareas } from "../../tareas.json";

export const crearTarea = (req, res) => {
   res.json({
      success: true,
      content: null,
      message: "Tarea creada exitosamente",
   });
};
