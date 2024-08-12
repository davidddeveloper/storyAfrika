import { Currency } from "./6-square";

class Pricing extends Currency {
    constructor(amount, currency) {
        this.setAmount(amount);
        this.setCurrency(currency);
    }

    getAmount(amount) {
        return this._amount;
    }

    setAmount(amount) {
        if (amount === undefined) throw 'amount cannot be empty';
        if (typeof(amount) === 'string') this._amount = amount;
        else throw 'amount must be a string';
    }

    setCurrency(currency) {
        if (currency === undefined) throw 'currency cannot be empty';
        //if (Currency.is)
    }

    displayFullPrice () {
        // amount currency_name (currency_code).
        return super.get
    }
}