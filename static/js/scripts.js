const sort = document.querySelectorAll('.sort-select');
const sortBtn = document.querySelector('#sort-button');
const tag = document.querySelectorAll('.tag-list.tag')
const url = window.location.href;

let getParamsStr = url.split("/").slice(3).join()  // removes 'http' and domain
    .split(/&|\?/).slice(1);
let getParams = getParamsStr.map((e) => e.split("=")); // splits parameters into key-value pairs
let paramsMap = new Map(getParams)

console.log(paramsMap)

// event listener for sort buttons
sortBtn.addEventListener('click', (e) => {
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
