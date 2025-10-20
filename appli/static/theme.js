let dark = window.matchMedia("(prefers-color-scheme: dark)");

function updateTheme() {
    if (dark.matches) {
        document.body.setAttribute("data-bs-theme", "dark");
        document.getElementById("navbar-main").classList.remove("navbar-light", "bg-light");
        document.getElementById("navbar-main").classList.add("navbar-dark", "bg-dark");
    } else {
        document.body.setAttribute("data-bs-theme", "light");
        document.getElementById("navbar-main").classList.remove("navbar-dark", "bg-dark");
        document.getElementById("navbar-main").classList.add("navbar-light", "bg-light");
    }
}

dark.addEventListener("change", updateTheme);
updateTheme();
