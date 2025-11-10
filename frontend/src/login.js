async function loginSubmit(event){
    event.preventDefault();

    const login = document.getElementById("txtlogin");
    const senha = document.getElementById("txtsenha");

    const token = 'meu_token';

    localStorage.setItem('token', token);
    window.location.href = "index.html";
}