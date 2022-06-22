import './App.css';
import Axios from 'axios'
import { useState, useEffect } from 'react'
import { HighlightWithinTextarea } from 'react-highlight-within-textarea'

function App() {
  const [corpus, setCorpus] = useState([]);
  const [searchList, setSearchList] = useState([]);
  const [isSearch, setIsSearch] = useState(false);
  const [value, setValue] = useState("Type...");
  const [wrongWord, setWrongWord] = useState([])

  const [suggestBox, setSuggestBox] = useState(false)

  const onChange = (value) => {
    setValue(value);
    var lastWord = value.slice(value.length - 1)
    if (lastWord === " "){
      console.log("I posted")
      postSpellCheck(value)
    }
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
      for (var key in spellObject) {
        if (spellObject.hasOwnProperty(key)) {
          wrongArray.push(parseInt(key))
        }
      }

      console.log(wrongArray)
      let wordArray = value.split(" ")
      let wrongWordArray = []
      wrongArray.map((wrong) => {
        wrongWordArray.push(wordArray[wrong])
      })
      console.log(wrongWordArray)
      setWrongWord(wrongWordArray)
    })
  }

  const searchInCorpus = (event) => {
    event.preventDefault()
    let value = document.getElementById('query').value
    let newArray = []
    corpus.map((word, key) => {
      if (word.includes(value)) {
        newArray.push(word.toLowerCase())
      }
    })
    setSearchList(newArray.slice(0, 999).sort())
    setIsSearch(true)
  }

  useEffect(() => {
    getCorpusList()
    document.addEventListener("contextmenu", (event) => {
      event.preventDefault();
    });

    let allWrongWord = document.querySelectorAll(".wrong-word")
    console.log(allWrongWord.length)

  }, [])

  return (
    <>
      <div className="container">
        <h2>Real Time Spelling Correction App</h2>
        <p className="main">
          Check your English text for grammar, spelling, and punctuation errors
          with our spelling correction app.
        </p>

        <div className="content-wrapper">
          <div>
            <div className="box-container">
              <HighlightWithinTextarea id="textarea" className="textareaas" maxLength="500"
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
              />
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
                  placeholder="Search..."
                  aria-label="Search through site content" />
                  <button className="search-button" id="search-but" onClick={searchInCorpus}>Search</button>
                </form>
              </div>
            </div>

            <button className='check-button' onClick={postSpellCheck}>Spell Check</button>

            <div className="counter-container">
              <p>Total character: <span id="total-conter">{value.length}</span></p>
              <p>
                Remaining:
                <span className="remaining-counter" id="remaining-counter">{500 - value.length}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
