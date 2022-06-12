import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'spelling-correction';



  ngOnInit() {
    console.log("Finish Initialise")
  }

  ngAfterViewInit() {
    var charval = <HTMLTextAreaElement>document.getElementById("textarea")
    let totalCount = document.getElementById("total-conter") as HTMLSpanElement;
    let remainingCoutn = document.getElementById("remaining-counter") as HTMLSpanElement;

    let userChar = 0;

    // to update the character on screen
    const updateCounter = () => {
      userChar = charval.value.length;

      totalCount.innerText = userChar.toString();

      remainingCoutn.innerText = (500 - userChar).toString();
    };

    charval.addEventListener("keyup", () => updateCounter());

    // to copy the text
    const copyText = () => {
      charval.select();
      charval.setSelectionRange(0, 99999);
      navigator.clipboard.writeText(charval.value);
    };
  }

}
