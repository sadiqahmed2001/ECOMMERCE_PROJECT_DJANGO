
function forwardPageLoader() {
    history.forward(); 
}


function backwardPageLoader() {
    history.back(); 
}

const switchCheckbox = document.querySelector('.switch-checkbox');
const body = document.body;

switchCheckbox.addEventListener('change', function() {
    if (this.checked) {
        body.classList.add('dark-mode');
    } else {
        body.classList.remove('dark-mode');
    }
});
