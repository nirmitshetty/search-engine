import React, {useState} from 'react';
import ReactDOM from "react-dom/client";
import App from "./App";
import './index.css';

const root = ReactDOM.createRoot(document.getElementById("root"));
var searchResult={};

function querySearch(query)
{

  return fetch('http://localhost:8000/querySearch/'+query)
          .then(response => response.json())
          .then(data => data);
}

function Header()
{
  const [status,setStatus]=useState(0);

  return (
    <div>
      <h1>Zot Search Engine</h1>
      <div>
        <input type="text" id="query"/>
        <button type="button" onClick={()=>
        {
          var query=document.getElementById('query').value;
          console.log('initiating hit');
          querySearch(query).then(res=>
            {
              if(typeof res == "string")
                searchResult=JSON.parse(res);
              else
                searchResult=res;
              setStatus(status+1);
            });
        }}>Search</button>
      </div>

      <Results results={searchResult} />
    </div>
  );
}

function Results({results})
{

  console.log(results)
  var indexArr=[];

  if(Object.keys(results).length!=0)
  {
    indexArr=Object.keys(results.index);
  }

  return(
    <>
      <table>
        <tbody>
        <tr><td>Index</td><td>Subject</td><td>Content</td><td>Score</td></tr>

        {indexArr.map(i=> (
          <tr key={i}><td>{parseInt(i)+1}</td><td>{results.Subject[i]}</td><td>{results.Content[i]}</td><td>{results.Score[i]}</td></tr>
        ))}

        </tbody>
      </table>
    </>
  )
}

root.render(
    <Header />
);
