const sort = document.querySelectorAll('.sort-select');
const sortBtn = document.querySelector('#sort-button');

let activeSort = [];

sortBtn.addEventListener('click', (e) => {
    let hrefString = ""

    for (let i = 0; i < sort.length; i++) {
        if (sort[i].value) {
            activeSort.push(sort[i]);
        }
    }

    for (let i = 0; i < activeSort.length; i++) {
        i === 0 ? hrefString += "?" : hrefString += "&"
        hrefString += `${sort[i].name}=${sort[i].value}`
    }

    if (hrefString) {
        window.location.href = hrefString;
    }
});
