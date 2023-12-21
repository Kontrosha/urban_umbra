type Listener<T> = (value: T) => void

export class Observable<T> {
    private listeners: Listener<T>[] = []

    public constructor(private _value: T) {}

    set value(newValue: T) {
        this._value = newValue
        this.listeners.forEach(l => l(newValue))
    }

    public addListener = (listener: Listener<T>) => {
        this.listeners.push(listener)
    }

    public removeListener = (listener: Listener<T>) => {
        this.listeners = this.listeners.filter(l => l !== listener)
    }
}