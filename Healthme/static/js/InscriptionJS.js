
function Afficher_InputText_Intolerance() {
    var select = document.getElementById("intolerance");
    var textbox = document.getElementById("InputText_Intolerance");
    var selectedValue = select.options[select.selectedIndex].value;

    if (selectedValue == "Autres") {
      textbox.style.display = "block";
    } else {
      textbox.style.display = "none";
    }
  }

function Afficher_InputText_Maladie(){
    var select = document.getElementById("maladie");
    var inputText = document.getElementById("InputText_Maladie");
    var selectedValue = select.options[select.selectedIndex].value;

    if (selectedValue == "Autres") {
      inputText.style.display = "block";
    } else {
      inputText.style.display = "none";
    }
}