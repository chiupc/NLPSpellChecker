import './App.css';
import Axios from 'axios'
import { useState, useEffect } from 'react'

function App() {
  const [corpus, setCorpus] = useState([]);
  const [searchList, setSearchList] = useState([]);
  const [isSearch, setIsSearch] = useState(false);

  const getCorpusList = () => {
    Axios.get("http://localhost:8000/api/corpustokens").then((response) => {
      console.log(response)
      console.log(response.data)
      setCorpus(response.data.result)
      console.log(corpus)
    })
  }

  const postSpellCheck = () => {
    
    Axios.post("http://localhost:8000/api/corpustokens")
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
              <textarea
                id="textarea"
                className="textarea"
                placeholder="Type Something..."
                maxLength="500"
              ></textarea>
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

            <button className='check-button'>Spell Check</button>

            <div className="counter-container">
              <p>Total character: <span id="total-conter"> 0</span></p>
              <p>
                Remaining:
                <span className="remaining-counter" id="remaining-counter">500</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
