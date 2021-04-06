const sort = document.querySelectorAll('.sort-select');
const sortBtn = document.querySelector('#sort-button')

for (let i = 0; i < sort.length; i++) {
    sortBtn.addEventListener('click', (e) => {
        let hrefString = ""

        for (let i = 0; i < sort.length; i++) {
            if (sort[i].value) {
                i == 0 ? hrefString += "?" : hrefString += "&"
                hrefString += `${sort[i].name}=${sort[i].value}`
            }
        }

        if (hrefString) {
            window.location.href = hrefString;
        }
    });
}