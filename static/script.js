function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

window.onload = function () {

    let riskElement = document.getElementById('riskNumber');
    let riskFill = document.getElementById('riskFill');

    if (riskElement && riskFill) {

        let target = parseInt(riskFill.getAttribute("data-risk"));
        let current = 0;

        let timer = setInterval(() => {

            riskElement.innerText = current + '%';
            riskFill.style.width = current + '%';

            if (current >= target) {
                clearInterval(timer);
            }

            current++;

        }, 15);
    }
};