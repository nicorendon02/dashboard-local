import { Component, OnInit } from '@angular/core';
import { Device } from '../Device-class';
import { DataService } from '../data.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})

/* PAY ATTENTION: In  dashboard.component.html, when you are using ngx charts, if you use "" the library will search
in this file the variable u other part of the code of this file, if you use '' you are using a creating a object
directly in the html (no accesing the code of this file), but you can create a object in the html 
that then uses the code of this file
*/

//This Part of the code (all the entire class) will be like the "Object" (with his variables and functions) that can be accesible in the dahsboard.component.html
export class DashboardComponent implements OnInit {

  devices:  Device[] = []; //List of all devices
  currentDevice!: Device;  //Current device that was selected on the map

  startDate: string | null = null;  //start date and end date for the filter, start with null value and will be updated by the user
  endDate: string | null = null;
  historicBool: boolean= false; //Variable that says if the systems would load all the historic data or only the daily data, at the beggining is only the daily data, can be updated by the user

  selectedImageRote: string= "../assets/selectedRay.png" //Routes fo the images that the map will use to show the selected and diselected markers
  diselectedImageRote: string= "../assets/diselectedRay.png"

  constructor(private dataService: DataService) {  } //This is neccesary for be able to use the service and get the data we need

  ngOnInit() { //THE FUNCTION NGONINIT IS PREDEFINED AS A ANGULAR FUNCTION, SO IT WILL EXCECUTE AT THE BEGGINING EVEN IF YOU DON´T CALL THE FUNCTION
    //There are certain parts of the code that perfectly works here, but doesn´t works (give sinxis errors) outside this function
    this.getMeasurements();
  }

  filter() {  //function that uses the start and end date to filter all the data
    if (this.startDate && this.endDate) {
      const start = new Date(this.startDate); //parse the date in string format into a operable Date format
      const end = new Date(this.endDate);

      const filteredMeasurements = this.currentDevice.allMeasurements.map((measurement: any) => {
        return {
          ...measurement,
          measurementsValues: measurement.measurementsValues.filter((value: any) => { //.filter uses angular pre-defined function
            const date = new Date(value.name);
            return date >= start && date <= end;
          })
        };
      });
      this.currentDevice["allMeasurements"]= filteredMeasurements; /*this will delete the measurements that doesn´t
      match the filter, but only in the RAM copy that angular has. To recover the data of other dates is neccesary
      to call again the function getMeasurements, that call the python api*/
    } 
  }

  calculateAverage(measurementsValues: any[]){ //this function return the average of any measurements list
    let average: number=0;
    for (let i = 0; i < measurementsValues.length; i++) {
      average+= measurementsValues[i]["value"]
      }
    return average/measurementsValues.length
  }
  
  getMeasurements(){ //this function calls the service (wich will use http) to  obtain the data of daily Measurements
    this.devices= [] //Clean the devicesList to don´t repeat devices in case there exist devices already
    this.dataService.getData(this.historicBool).subscribe(receiptDevices => {
      for (let i = 0; i < receiptDevices.length; i++) {
        this.devices.push(receiptDevices[i])
      }
      this.updateCurrentDevice(this.devices[0]); //by default, the selected device is the first on the list
    });
  }

  MapOptions: google.maps.MapOptions = {   //Visual options of the google map
    mapId: "e87693c86192baae", //should be the same id that appears in google maps console (in your google account)
    center: { lat:40.428421, lng:-86.917492},
    zoom: 13,
  };

  public updateCurrentDevice(deviceClicked: any | null) { //This function is called by the map
    this.currentDevice= deviceClicked; //Update the current device, it implies that the voltage graphics and others are updated automatically too
    this.devices.forEach(device => device.icon = this.diselectedImageRote); // this line change all the markets colors to red  
    deviceClicked.icon = this.selectedImageRote; // This change the color of the selected marker
  }

  onDeviceSelect(event: Event) { //This function is called by the manual selector to update the current device
    const target = event.target as HTMLSelectElement;
    const selectedDevice = this.devices.find(device => device.name === target.value);
    if (selectedDevice) {this.updateCurrentDevice(selectedDevice);}
  }

  onCheckboxChange(event: Event) {//This function check if the checkbox is checked to update the historicBool Variable to know if is neccesary to load historic data or daily data only
    const checkbox= event.target as HTMLInputElement;
    this.historicBool= checkbox.checked; //checkbox.checked return true or false, depending of the user selection
    this.getMeasurements();
}
}
