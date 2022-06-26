import './App.css';
import Axios from 'axios'
import { useState, useEffect } from 'react'
import { HighlightWithinTextarea } from 'react-highlight-within-textarea'

function App() {
  const [corpus, setCorpus] = useState([]);
  const [searchList, setSearchList] = useState([]);
  const [isSearch, setIsSearch] = useState(false);
  const [value, setValue] = useState("...");
  const [wrongWord, setWrongWord] = useState([])
  const [suggestList, setSuggestList] = useState([])

  const onChange = (value) => {
    setValue(value);
  }

  const checkSpell = () => {
    setWrongWord([])
    setSuggestList([])
    console.log(wrongWord)
    console.log(suggestList)
    postSpellCheck(value)
  }

  const getCorpusList = () => {
    Axios.get("http://localhost:8000/api/corpustokens").then((response) => {
      console.log(response)
      console.log(response.data)
      setCorpus(response.data.result.sort())
      console.log(corpus)
    })
  }

  const postSpellCheck = (content) => {
    //event.preventDefault()
    const params = JSON.stringify({ 'input_text': content })
    Axios.post("http://localhost:8000/api/spellcheck", params, { headers: { "Content-Type": "application/json" } }).then((response) => {
      console.log(response)
      console.log(response.data)
      let spellObject = response.data
      var wrongArray = []
      var suggestionArray = []
      for (var key in spellObject) {
        if (spellObject.hasOwnProperty(key)) {
          wrongArray.push(parseInt(key))
          suggestionArray.push(spellObject[key])
        }
      }

      console.log(wrongArray)
      let wordArray = value.split(" ")
      let wrongWordArray = []
      wrongArray.map((wrong) => {
        wrongWordArray.push(wordArray[wrong])
      })
      console.log('WrongWordArray:',wrongWordArray)
      setWrongWord(wrongWordArray)
      setSuggestList(suggestionArray)

      setTimeout( () => {
        var allWrongWord = document.querySelectorAll(".wrong-word")
        console.log('allWrongWord:',  allWrongWord)
        allWrongWord.forEach(function(eachWrong, index) {
          console.log(eachWrong)
          var child = eachWrong.childNodes
          child.forEach(function(eachChild){
            eachChild.childNodes[0].className = `wrongspan-${index}`
            eachChild.addEventListener('contextmenu', event =>{
              event.preventDefault()
              console.log(event.target)
              var fireElemIndex = event.target.className.split('-')[1]
              console.log(fireElemIndex)
              document.getElementById('rmenu').className = "show"
              document.getElementById('rmenu').style.top = mouseY(event) + 'px';
              document.getElementById('rmenu').style.left = mouseX(event) + 'px';
              /*
              var suggestUl = document.getElementById('suggestul')
              suggestList[fireElemIndex].map((suggestWord) => {
                var li = document.createElement("li")
                li.innerHTML = suggestWord
                suggestUl.appendChild(li)
              })*/
              window.event.returnValue = false;
            })
          })
      },1000);
      },)
      //console.log(allWrongWord.length)

    })
  }

  const searchInCorpus = (event) => {
    event.preventDefault()
    let value = document.getElementById('query').value
    let newArray = []
    corpus.map((word, key) => {
      if (word.startsWith(value)) {
        newArray.push(word.toLowerCase())
      }
    })
    setSearchList(newArray.slice(0, 999).sort())
    setIsSearch(true)
  }
  
  function mouseX(evt) {
    if (evt.pageX) {
      return evt.pageX;
    } else if (evt.clientX) {
      return evt.clientX + (document.documentElement.scrollLeft ?
        document.documentElement.scrollLeft :
        document.body.scrollLeft);
    } else {
      return null;
    }
  }
  
  function mouseY(evt) {
    if (evt.pageY) {
      return evt.pageY;
    } else if (evt.clientY) {
      return evt.clientY + (document.documentElement.scrollTop ?
        document.documentElement.scrollTop :
        document.body.scrollTop);
    } else {
      return null;
    }
  }

  useEffect(() => {
    getCorpusList()
    document.addEventListener("contextmenu", (event) => {
      /*
      event.preventDefault();
      document.getElementById('rmenu').className = "show"
      document.getElementById('rmenu').style.top = mouseY(event) + 'px';
      document.getElementById('rmenu').style.left = mouseX(event) + 'px';
      window.event.returnValue = false;*/
    });
    console.log('testing')

    document.addEventListener("click", (event) => {
      document.getElementById('rmenu').className = "hide"
    })
  }, [])

  useEffect(() => {
    var allWrongWord = document.querySelectorAll(".wrong-word")
      console.log('allWrongWord:',  allWrongWord)
      allWrongWord.forEach(function(eachWrong, index) {
        console.log(eachWrong)
        var child = eachWrong.childNodes
        child.forEach(function(eachChild){
          eachChild.childNodes[0].className = `wrongspan-${index}`
          
          eachChild.addEventListener('contextmenu', event =>{
            event.preventDefault()
            
            console.log(event.target)
            var fireElemIndex = event.target.className.split('-')[1]
            console.log(fireElemIndex)
            document.getElementById('rmenu').className = "show"
            document.getElementById('rmenu').style.top = mouseY(event) + 'px';
            document.getElementById('rmenu').style.left = mouseX(event) + 'px';
            var suggestUl = document.getElementById('suggestul')
            removeAllChild(suggestUl)
            
            suggestList[fireElemIndex].map((suggestWord) => {
              var p = document.createElement("p")
              console.log(eachChild.childNodes[0].innerHTML)
              p.className = `s-${eachChild.childNodes[0].innerHTML}`
              p.innerHTML = suggestWord
              p.addEventListener("click", function(event){
                replaceWord(event.target.className.split('-')[1], event.target.innerHTML)
                console.log(event.target.innerHTML)
                console.log(event.target.className)
              })
              suggestUl.appendChild(p)
            })
            window.event.returnValue = false;
          })
        })
      },);
  }, [suggestList, value])

  const removeAllChild = (parent) => {
    while (parent.firstChild) {
      parent.removeChild(parent.firstChild)
    }
  }

  const replaceWord = (wrongWord, correctWord) => {
    console.log(wrongWord)
    console.log(correctWord)
    var wrongRegex = new RegExp(wrongWord, "g")
    var newValue = value.replace(wrongRegex, correctWord)
    console.log(newValue)
    setValue(newValue)
  }


  return (
    <>
      <div className="container">
        <h2>NLP Spelling Correction App</h2>
        <p className="main">
          Check your English text for grammar, spelling, and punctuation errors
          with our spelling correction app.
        </p>

        <div className="content-wrapper">
          <div>
            <div className="box-container">
              <HighlightWithinTextarea id="textarea" className="textareaas" maxLength="500"
                maxlength = "500"
                placeholder = ""
                value = {value}
                onChange= {onChange}
                highlight = {[
                  wrongWord.map((each, index) => {
                    return {
                      highlight: each,
                      className: `green wrong-word wrong-${index}`,
                      id: `wrong-${index}`
                    }
                  })
                ]}
              ></HighlightWithinTextarea>
              {/*<textarea
                  id="textarea"
                  className="textarea"
                  placeholder="Type Something..."
                  maxLength="500"
                ></textarea>*/}
              <div className="corpus-list">
                <ul className="scroll" id="corpus-ul">
                  {!isSearch ?
                    corpus.slice(0, 999).map((word, key) => {
                      return <li id={key}>{word}</li>
                    })
                    : searchList.slice(0, 99).map((word, key) => {
                      return <li id={key}>{word}</li>
                    })
                  }
                </ul>
                <form className="search-form" id="form" role="search" >
                  <input className='search-input' type="search" id="query" name="q"
                  placeholder="Search Corpus..."
                  aria-label="Search through site content" />
                  <button className="search-button" id="search-but" onClick={searchInCorpus}>Search</button>
                </form>
              </div>
            </div>

            <button className='check-button' onClick={checkSpell}>Spell Check</button>

            <div className="counter-container">
              <p className='word text' id='tester'>Total character: <span id="total-conter">{value.length}</span></p>
              <p className='word text'>
                Remaining:
                <span className="remaining-counter" id="remaining-counter">{500 - value.length}</span>
              </p>
            </div>

            <div className='hide' id='rmenu'>
              <div className='show ul-list' id='suggestul'>
              </div>
            </div>

          </div>
        </div>
      </div>
    </>
  );
}

export default App;
