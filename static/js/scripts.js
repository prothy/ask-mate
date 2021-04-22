let sort = document.querySelectorAll('.sort-select');
let sortBtn = document.querySelector('#sort-button');
let tags = document.querySelectorAll('.tag-list .tag')
const url = window.location.href;

let getParamsStr = url.split("/").slice(3).join()  // removes 'http' and domain
    .split(/&|\?/).slice(1);
let getParams = getParamsStr.map((e) => e.split("=")); // splits parameters into key-value pairs

tags.forEach((element) => {
    if (getParams.filter((e) => e.includes(element.name)).length) {
        element.classList.add('unselect');
    }
})

// event listener for sort buttons
sortBtn.addEventListener('click', () => {
    let hrefString = ""
    let activeSort = []; //list of all selected sorting options

    for (let i = 0; i < sort.length; i++) {
        if (sort[i].value) {
            activeSort.push(sort[i]);
        }
    }

    // replaces 'sort' and 'order' values by filtering each first, then adding them again
    for (let i = 0; i < activeSort.length; i++) {
        getParams = getParams.filter((e) => !e.includes(activeSort[i].name));
        getParams.push([activeSort[i].name, activeSort[i].value]);

        getParamsStr = getParams.map((e) => e.join('='));
    }

    hrefString = '?' + getParamsStr.join('&');

    if (hrefString) {
        window.location.href = hrefString;
    }
});

document.addEventListener('click', (event) => {
    if (event.target.matches('.tag')) {
        filterSelectedTag(event.target);
    }
});

function filterSelectedTag(target) {
    let hrefString = '/';

    const tag_in_request = getParams.filter((e) => e.includes(target.name)).length
    const elementParam = ['tag', target.name]

    if (tag_in_request) {
        getParams.splice(getParams.indexOf(elementParam), 1);
    } else {
        getParams.push(elementParam);
    }

    if (getParams.length) {
        getParamsStr = getParams.map((e) => e.join('='));
        hrefString = '?' + getParamsStr.join('&');
    }

    window.location.href = hrefString;
}