import { tareas } from "../../tareas.json";
const tareas_temporales = [];

export const crearTarea = (req, res) => {
   //req.body, luego de haber declarado el parser, me retornara todo lo que el cliente me mando mediante el body
   console.log(req.body);
   const tarea = req.body;
   tarea.estado = true;
   console.log(tarea);
   tareas_temporales.push(tarea);
   res.json({
      success: true,
      content: tarea,
      message: "Tarea creada exitosamente",
   });
};

export const listarTareas = (req, res) => {
   console.log(tareas);
   console.log(tareas_temporales);
   //const tareas_totales = tareas.concat(tareas_temporales);
   //otro metodo
   const tareas_totales = [...tareas, ...tareas_temporales];
   res.json({
      success: true,
      content: tareas_totales,
      message: null,
   });
};

export const devolverTarea = (req, res) => {
   //req.params -> captura los valores pasados por la url
   const { id } = req.params;
   let tarea_filtrada = [...tareas, ...tareas_temporales].filter(
      (tarea) => tarea.id === +id
   );

   res.json({
      success: true,
      content: tarea_filtrada,
      message: null,
   });
};

export const buscarTarea = (req, res) => {
   console.log(req.query);
   //const { nombre, estado, id } = req.query;
   let resultado = [];
   // if (nombre) {
   //    resultado = [...tareas, ...tareas_temporales].filter(
   //       (tarea) => tarea.nombre === nombre
   //    );
   // }
   const filters = req.query;
   const tareas_filtradas = tareas.filter((tarea) => {
      let isValid = true;
      for (let key in filters) {
         console.log(key, tarea[key], filters[key]);
         isValid = isValid && tarea[key] == filters[key];
         console.log(isValid);
      }
      return isValid;
   });

   res.json({
      message: "ok",
      data: tareas_filtradas,
   });
};
