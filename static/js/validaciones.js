
function validarFormulario() {
    var curp = document.getElementById('curp').value;
    var telefono = document.getElementById('telefono').value;

    if (curp.length < 18) {
        alert("Error: La CURP debe tener exactamente 18 caracteres.");
        return false; 
    }

    if (isNaN(telefono)) {
        alert("El teléfono solo debe contener números.");
        return false;
    }

    return true;
}

function mostrarCamposEspeciales(){
    const rol = document.getElementById('rol').value;

    //Ocultamos campos
    document.getElementById('campo-abogado').style.display= 'none'
    document.getElementById('campo-medico').style.display= 'none'
    document.getElementById('campo-psicologo').style.display= 'none'

    if (rol === 'abogado'){
        document.getElementById('campo-abogado').style.display= 'block'
    } else if(rol === 'medico') {
        document.getElementById('campo-medico').style.display= 'block'
    } else if (rol === 'psicologo') {
        document.getElementById('campo-psicologo').style.display= 'block'
    }
}