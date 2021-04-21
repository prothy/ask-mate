const sort = document.querySelectorAll('.sort-select');
const sortBtn = document.querySelector('#sort-button');
const tag = document.querySelectorAll('.tag-list.tag')
const url = window.location.href;

let getParamsStr = url.split("/").slice(3).join()  // removes 'http' and domain
    .split(/&|\?/).slice(1);
let getParams = getParamsStr.map((e) => e.split("=")); // splits parameters into key-value pairs


// event listener for sort buttons
sortBtn.addEventListener('click', () => {
    let hrefString = ""
    let activeSort = []; //list of all selected sorting options

    console.log(getParamsStr)

    for (let i = 0; i < sort.length; i++) {
        if (sort[i].value) {
            activeSort.push(sort[i]);
        }
    }

    // replaces 'sort' and 'order' values by filtering each first, then readding them
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

    console.log(target.classList)

    if (tag_in_request) {
        getParams.splice(getParams.indexOf(elementParam), 1);
        target.classList.add('unselect');
    } else {
        getParams.push(elementParam);
        target.classList.remove('unselect')
    }

    console.log('after', getParams)

    if (getParams.length) {
        getParamsStr = getParams.map((e) => e.join('='));
        hrefString = '?' + getParamsStr.join('&');
    }

    window.location.href = hrefString;
}