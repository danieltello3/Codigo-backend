const socket = io("http://127.0.0.1:8000");
const btnIngresar = document.getElementById("btnIngresar");
const chat = document.getElementById("chat");
const login = document.getElementById("login");
const username = document.getElementById("username");
const usuarios_conectados = document.getElementById("usuarios-conectados");
//mensajes
const mensaje = document.getElementById("mensaje");
const btnEnviar = document.getElementById("btnEnviar");
const listaMensajes = document.getElementById("listaMensajes");
const divUsers = document.getElementById("users");
const estado = document.getElementById("estado");

function timejs(number, index) {
   return [
      ["justo ahora", "en un rato"],
      ["hace %s segundos", "en %s segundos"],
      ["hace 1 minuto", "en 1 minuto"],
      ["hace %s minutos", "en %s minutos"],
      ["hace 1 hora", "en 1 hora"],
      ["hace %s horas", "en %s horas"],
      ["hace 1 día", "en 1 día"],
      ["hace %s días", "en %s días"],
      ["hace 1 semana", "en 1 semana"],
      ["hace %s semanas", "en %s semanas"],
      ["hace 1 mes", "en 1 mes"],
      ["hace %s meses", "en %s meses"],
      ["hace 1 año", "en 1 año"],
      ["hace %s años", "en %s años"],
   ][index];
}

socket.on("connect", () => {
   console.log(socket.id);
   console.log(socket.connected);
   if (socket.connected) {
      estado.classList.remove("bg-danger");
      estado.classList.add("bg-success");
      estado.innerText = "ONLINE";
   }
});

socket.on("disconnect", (reason) => {
   console.log(reason);
   estado.classList.remove("bg-success");
   estado.classList.add("bg-danger");
   estado.innerText = "OFFLINE";
});

timeago.register("es", timejs);

btnIngresar.addEventListener("click", (e) => {
   socket.emit("registrar", { username: username.value });
   chat.style.display = "block";
   login.style.display = "none";
   divUsers.style.display = "block";
});

socket.on("lista-usuarios", (usuarios) => {
   usuarios_conectados.innerText = "";
   usuarios.forEach((usuario) => {
      const usuarioLi = document.createElement("li");
      usuarioLi.classList.add("list-group-item");

      usuarioLi.innerText = usuario.username;
      usuarios_conectados.appendChild(usuarioLi);
   });
});

btnEnviar.addEventListener("click", (evento) => {
   console.log(mensaje.value);
   socket.emit("mensaje-nuevo", mensaje.value);
   mensaje.value = "";
});

socket.on("lista-mensajes", (mensajes) => {
   listaMensajes.innerText = "";
   mensajes.forEach((mensaje) => {
      const fecha = timeago.format(mensaje.fecha, "es");
      const mensajeLi = document.createElement("li");
      mensajeLi.classList.add("list-group-item");

      mensajeLi.innerText = `${mensaje.username}(${fecha}): ${mensaje.mensaje}`;
      listaMensajes.appendChild(mensajeLi);
   });
   console.log(mensajes);
});
