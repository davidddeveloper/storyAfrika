function createIteratorObject(report) {
  const array = [];
  Object.values(report).forEach(value => array.push(...value));
  return array
}

function iterateThroughObject(reportWithIterator) {
  let employees = '';
  reportWithIterator.forEach((value, idx) => { employees += (idx !== 0 && idx !== (employees.length - 1) ? ' | ' : '') + `${value}` });
  return employees;
}

let xyz = { engineering: [ 'Bob', 'Jane' ], marketing: [ 'Sylvie' ] }
const iteratorobj = createIteratorObject(xyz);

for (const item of iteratorobj) {
  console.log(item);
}

console.log(iterateThroughObject(iteratorobj))