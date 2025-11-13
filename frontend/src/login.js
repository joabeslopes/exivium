async function loginSubmit(event){
    event.preventDefault();

    const email = document.getElementById("txtEmail");
    const senha = document.getElementById("txtSenha");

    const request = {
        "email": email.value,
        "senha": senha.value
    };

    const userData = await post("/token", request);

    if (userData){
        localStorage.setItem('token', userData.token);
        delete userData.token;
        localStorage.setItem('userData', JSON.stringify(userData));
        window.location.href = "index.html";
    } else {
        alert("Falha no login");
    };
};