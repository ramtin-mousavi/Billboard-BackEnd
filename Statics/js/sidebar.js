function openPanel() {
document.getElementById("main").style.marginRight = "200px";
document.getElementById("rightPanel").style.width = "200px";
document.getElementById("rightPanel").style.display = "block";
document.getElementById("openNav").style.display = 'none';
// document.getElementById("footer").style.marginRight = "200px";

}
function closePanel() {
document.getElementById("main").style.marginRight = "0%";
// document.getElementById("footer").style.marginRight = "0%";
document.getElementById("rightPanel").style.display = "none";
document.getElementById("openNav").style.display = "inline-block";
}
