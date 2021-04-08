const sort = document.querySelectorAll('.sort-select');
const sortBtn = document.querySelector('#sort-button');

sortBtn.addEventListener('click', (e) => {
    let hrefString = ""
    let activeSort = [];

    for (let i = 0; i < sort.length; i++) {
        if (sort[i].value) {
            activeSort.push(sort[i]);
        }
    }

    for (let i = 0; i < activeSort.length; i++) {
        i === 0 ? hrefString += "?" : hrefString += "&";
        hrefString += `${activeSort[i].name}=${activeSort[i].value}`;
    }

    if (hrefString) {
        window.location.href = hrefString;
    }
});
