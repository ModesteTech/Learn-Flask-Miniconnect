function togglePassword(id) {

    const passwordInput = document.getElementById(id);

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    }
}

function Confirm_password(){
    const confirm = document.getElementById("confirmation");
    const formulaire = document.getElementById("formulaire-inscription")
    const motDePasse = document.getElementById("mot_de_passe");
    const erreur = document.getElementById("message-erreur");
    
    formulaire.addEventListener("submit",function(event){
        if(confirm.value !== motDePasse.value){
            event.preventDefault();
            erreur.textContent="Les mots de passes ne correspondent pas";
        }else{
            erreur.textContent="";
        }
    })
}