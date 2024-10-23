export class Device {
    constructor(
        public id: number,
        public name: string,
        public latitude: number,
        public longitude: number,
        public icon: string,
        public allMeasurements: any[]
    ) {}

  }