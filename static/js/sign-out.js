document.addEventListener("DOMContentLoaded", () => {
    const signOutBtn = document.getElementById("signOutBtn")
    const signOutForm = document.getElementById("signOutForm")
    if(signOutBtn && signOutForm) {
        signOutBtn.addEventListener("click", () => signOutForm.submit())
    }
})