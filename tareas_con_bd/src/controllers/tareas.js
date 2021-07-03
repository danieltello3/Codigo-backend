import { Tarea } from "../config/modelos";
import { Op } from "sequelize";

export const serializadorTarea = (req, res, next) => {
   //analizamos el body
   const { tareaNombre } = req.body;

   if (tareaNombre && tareaNombre.trim().length > 0) {
      next();
   } else {
      return res
         .json({
            success: false,
            content: "se necesita un nombre",
            message: "error al crear la nueva tarea",
         })
         .status(400);
   }
};
//CRUD
export const crearTarea = async (req, res) => {
   // para registrar una nueva tarea
   // si usamos .build() se tendra que realizar en dos pasos el guardado del registro, primero construye el objeto y luego llamaria al metodo save()
   // Tarea.build({tareaNombre: "nombre de tarea",...}).save()

   //el segundo metodo es con create() 1 solo paso.
   try {
      const { tareaId, tareaNombre, tareaEstado } = await Tarea.create(
         req.body
      );
      const datos = { tareaId, tareaNombre, tareaEstado };

      return res
         .json({
            success: true,
            content: datos,
            message: "Nueva tarea creada con exito",
         })
         .status(201);
   } catch (error) {
      return res
         .json({
            success: false,
            content: error,
            message: "error al crear la nueva tarea",
         })
         .status(400);
   }
};

export const listarTareas = async (req, res) => {
   const tareas = await Tarea.findAll({
      //attributes: ["tareaNombre", ["id", "id"]],
      attributes: {
         exclude: ["createdAt", "fecha_actualizacion"],
      },
   });
   return res.json({
      success: true,
      content: tareas,
      message: null,
   });
};

export const actualizarTarea = async (req, res) => {
   const { id } = req.params;
   // UPDATE TAREAS set col1=val1 Where id = 1
   const resultado = await Tarea.update(req.body, {
      where: {
         tareaId: id,
      },
   });
   console.log(resultado);
   if (resultado[0] === 1) {
      const data = await Tarea.findByPk(id, {
         attributes: {
            exclude: ["createdAt", "fecha_actualizacion"],
         },
      });
      return res.json({
         success: true,
         content: data,
         message: "se actualizo la tarea",
      });
   } else {
      return res
         .json({
            success: false,
            content: null,
            message: "no se encontro la tarea",
         })
         .status(400);
   }

   // return res.json({
   //    success: true,
   //    content: null,
   // });
};

export const eliminarTarea = async (req, res) => {
   const { id } = req.params;
   const resultado = await Tarea.destroy({ where: { tareaId: id } });
   console.log(resultado);
   if (resultado === 1) {
      return res.json({
         success: true,
         content: null,
         message: `se elimino la tarea con el id: ${id}`,
      });
   } else {
      return res
         .json({
            success: false,
            content: null,
            message: "no se encontro la tarea a eliminar",
         })
         .status(400);
   }
};

export const tareaBusqueda = async (req, res) => {
   //SELECT * FROM tareas WHERE nombre LIKE '%python%';
   const { nombre } = req.query;
   const resultado = await Tarea.findAll({
      where: {
         // [Op.and] : [
         //    {tareaNombre: {
         //    [Op.like]: `%${nombre}%`},
         //    {tareaId: id},
         // },
         // ]
      },
   });

   console.log(resultado.toJson());

   return res.json({
      success: true,
      content: null,
   });
};
