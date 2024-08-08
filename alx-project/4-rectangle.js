
function fetchData () {
    return fetch('url')
}

fetchData.then(res => res.json()).then(data => console.log(data));

(function getData(data) {
    getJson(data, function (json) {
        function getEployeeJson (employeeJson) {
            function getNames (name) {name}
        }
        function getDapartment () {}
    }, failureCallback)
})(fetchData)

doSomething(function (result) {
    doSomethingElse(result, function (newResult) {
      doThirdThing(newResult, function (finalResult) {
        console.log(`Got the final result: ${finalResult}`);
      }, failureCallback);
    }, failureCallback);
  }, failureCallback);

async function xyz () {
    const value1 = await getValue;
    const value2 = await getValue2(value1);
    const value3 = await getValue3(value2)
}
