import { Model } from "sequelize";

export type TRespuesta = {
   success: boolean;
   message: string;
   content: Model | null | string | Model[] | undefined;
};
