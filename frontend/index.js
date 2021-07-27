const socket = io("http://127.0.0.1:8000");
const btnIngresar = document.getElementById("btnIngresar");
const username = document.getElementById("username");
const listaUsuarios = document.getElementById("listaUsuarios");

btnIngresar.addEventListener("click", (e) => {
   e.preventDefault();
   socket.emit("registrar", { username: username.value });
});

socket.on("lista-usuarios", (usuarios) => {
   console.log(usuarios);
   usuarios.forEach((usuario) => {
      let userLi = document.createElement("li");
      let userContent = document.createTextNode(`${usuario.username}`);
      userLi.appendChild(userContent);
      listaUsuarios.appendChild(userLi);
   });
});
