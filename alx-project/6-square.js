export default class HolbertonCourse {
  constructor(name, length, students) {
    this.setName(name);
    this.setLength(length);
    this.setStudents(students);
  }

  getName () {
    return this._name;
  }

  setName (name) {
    if (name === '' || name === undefined) {
      throw 'name cannot be empty';
    }
    if (typeof(name) === 'string') {
      this._name = name;
    } else {
      throw 'name must be a string';
    }
  }

  getLength () {
    return this._length;
  }

  setLength (length) {
    if (length === undefined) {
      throw 'length cannot be empty';
    }
    if (typeof(length) === 'number') {
      this._length = length;
    } else {
      throw 'length must be a number';
    }
  }

  getStudents () {
    return this._students;
  }

  setStudents (students) {
    if (students === undefined) {
      throw 'students cannot be empty';
    }
    if (Array.isArray(students)) {
      this._students = students;
    } else {
      throw 'students must be a number';
    }
  }
}

export class Currency {
  constructor(code, name) {
    this.setCode(code);
    this.setName(name);
  }

  getName () {
    return this._name;
  }
  setName (name) {
    if (typeof(name) === '') throw 'name cannot be empty';
    if (typeof(name) === 'string') this._name = name;
    else throw 'name must be a string';
  }

  getCode () {
    return this._code;
  }
  setCode (code) {
    if (typeof(code) === '') throw 'code cannot be empty';
    if (typeof(code) === 'string') this._code = code;
    else throw 'code must be a string';
  }
  displayFullCurrency () {
    return `${this._name} (${this._code})`
  }
}