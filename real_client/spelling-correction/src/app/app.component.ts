import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent{
  searchForm: any;
  title = 'spelling-correction';

  

  /*
  constructor(private formBuilder: FormBuilder){
    this.searchForm = this.searchForm.group({
      search: '',
    })
  }*/


  
  ngOnInit(): void {}

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
    
    // Search Function
    var input = <HTMLInputElement>document.getElementById('my-input')
    var inputValue = input.value.toUpperCase()
    var theUl = document.getElementById('corpus-ul')
    var theLi = theUl?.getElementsByTagName('li') as HTMLCollectionOf<HTMLElement>
    var button = <HTMLButtonElement>document.getElementById('search-but')

    button.addEventListener('click', function() {
      for (let i=0; i < theLi?.length; i++) {
        let textValue = theLi[i].textContent || theLi[i].innerHTML
        if (textValue.toUpperCase().indexOf(inputValue) > -1) {
          theLi[i].style.display = "";
        } else {
          theLi[i].style.display = "none";
        }
      }
    })
  }
  

}
