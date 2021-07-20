type TpaginationDto = {
   page: number;
   perPage: number;
};

export const paginatedHelper = (
   params: TpaginationDto
): {
   skip: number;
   limit: number;
} | void => {
   if (params.page && params.perPage) {
      return {
         skip: (params.page - 1) * params.perPage,
         limit: params.perPage,
      };
   }
};

export const paginationSerializer = (total: number, query: TpaginationDto) => {
   const { page, perPage } = query;
   const itemsPerPage = total >= perPage ? perPage : total;
   const totalPages = Math.ceil(total / itemsPerPage);
   const prevPage = page > 1 && page <= totalPages ? page - 1 : null;
   const nextPage = totalPages > 1 && page < totalPages ? page + 1 : null;

   return {
      perPage: itemsPerPage,
      total,
      page,
      prevPage,
      nextPage,
      totalPages,
   };
};
